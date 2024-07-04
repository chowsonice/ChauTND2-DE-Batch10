## Find functions that can be used with subquery and learn how these functions are executed logically and explain performance differences

### Functions that can be used with a single-row subquery
- Comparison operators like =, >, <, >=, <=
- After processing the subquery, it executes like a ordinary conditional query
- Query:
```sql
select *
from order_items
where order_item_subtotal >= (select max(order_item_subtotal)
							  from order_items
							  as sub_order_items) ;
```
- Query finishes in 
- Query plan:
![](Images/Pasted%20image%2020240704094911.png)
### Functions that can be used with a single-column subquery
#### ANY / SOME, ALL
```sql
where comparison_operator all / any / some ( subquery )
```
##### ALL
- `ALL` returns `TRUE / FALSE`, `TRUE` if condition is met with *all* of the subquery values
- Logically, it takes the value and compares it to every row of the subquery result:
	- If it doesn't satisfy, it stops immediately and returns false
	- Else it runs till the final row of the result and returns true
e.g.
- Query:
```sql
select *
from order_items
where order_item_subtotal >= all (select (order_item_subtotal)
								  from order_items
								  as sub_order_items) ;
```
- Query finishes in 16.162s
- Query plan:
![](Images/Pasted%20image%2020240704094240.png)
 - We can see that a sequential scan on table order_items is executed
- Each row of order_items go through a second sequential scan to compare if the value of `order_items.order_item_subtotal >= sub_order_items.order_item_subtotal`. 
- Materialise is used to optimise the query by storing the result temporarily so that it could be accessed multiple times without re-running the subquery
 
##### ANY / SOME
- `ANY` returns TRUE if the condition is met with *any* of the subquery values
- Logically, it takes the value and compares it to every row of the subquery result:
	- If it satisfies, it stops immediately and returns true
	- Else it runs till the final row of the result and returns false
 e.g.
 - We can see that there is a join between order_items and sub_order_items, join condition is `order_items.order_item_subtotal >= sub_order_items.order_item_subtotal`
- Then we get the values of the order_items table left after the filter
- Query:
```sql
select *
from order_items
where order_item_subtotal >= any (select (order_item_subtotal)
								  from order_items
								  as sub_order_items) ;
```
- Query finishes in 273msec
- Query plan:
![](Images/Pasted%20image%2020240704094651.png)
##### ALL vs COMPARISON OPERATOR + MAX/MIN
- `ALL` includes two nested loop sequential scan, thus the complexity of `ALL` is $O(N^2)$
- `COMPARISON OPERATOR + MAX/MIN` comprises of two sequential scan, one to get the max value and one to filter the row satisfying the condition, thus the complexity is $O(N)$
- In conclusion, if you need to find the max/min of a table, use `COMPARISON OPERATOR + MAX/MIN`, otherwise if you need to do some other operation like `LIKE`, use `ALL`

#### EXISTS, IN
##### EXISTS
- `EXISTS` is used when you need to check if a query return *any* results and you want something more efficient than counting
- Since it's a predicate, not a `JOIN` condition, the rows can only be returned at most once
- Logically, think of it as having the subquery run once for every row in the main query to be determined if a row exists. [^3]
	- Right when the subquery finds a row, it exits immediately and the return value is true. 
	- Else, it is false. 
	- The selected column(s) of the subquery **does not matter** as the result is tied only to the existence or non-existence of a resulting row based on the FROM/JOIN/WHERE clauses in the subquery.
- `EXISTS` is also used to implement a semi-join
e.g. We have this query to get list of customers who had at least an order in January 2014:
```SQL
select *
from customers
where exists(select 1
			 from orders
			 where customer_id = order_customer_id and to_char(order_date, 'yyyy-MM') = '2014-01');
```
Query finishes running in **160 msec**.
Query plan:
![](Images/Pasted%20image%2020240703212844.png)
##### IN
- `IN` is used when we need to compare a value to another set of value
- `IN` predicate (unlike `EXISTS`) can return `TRUE`, `FALSE` or `NULL`:
	- `TRUE` is returned when the non-`NULL` value in question is found in the list
	- `FALSE` is returned when the non-`NULL` value is not found in the list **and** the list does not contain `NULL` values
	- `NULL` is returned when the value is `NULL`, **or** the non-`NULL` value is not found in the list and the list contains at least one `NULL` value
- Logically, think of it as having every row in the main query scan the result list from the subquery. [^3]
	- If a matching value is found and it is not `NULL`, the return value is true. 
	- If a matching value is not found and the list does not contain `NULL` value, the return value is false
	- If the matching value is not found and there is a `NULL` value in the list, the return value is `NULL`
	- If the value is `NULL`, the return value is `NULL`
- `IN` does not give a definitive answer to whether or not the value is in the list as long as there are `NULL` values on either side of the expression, returning `NULL` instead. [^2]
- `column IN [value1, value2]` is the same as multiple `OR` conditions `column=value1 OR column=value2` [^2]
e.g. We have this query to get list of customers who had at least an order in January 2014:

- Query:
```sql
select *
from customers
where customer_id in (select order_customer_id
					  from orders
					  where to_char(order_date, 'yyyy-MM') = '2014-01');
```
- Query finishes running in **103 msec**.
- Query plan:
![](Images/Pasted%20image%2020240703212704.png)
###### LEFT JOIN
- Query:
```SQL
select customers.*
from customers
join (select distinct order_customer_id
	  from orders 
	  where to_char(order_date, 'yyyy-MM') = '2014-01') as orders on order_customer_id = customer_id
```
- Query finishes in **125msec**
- Query plan:
![](Images/Pasted%20image%2020240703213921.png)
We can see that the query plan isn't very different from `EXISTS` and `JOIN` besides the sort and unique steps.

##### EXISTS vs IN vs LEFT JOIN
- From the examples above, we can see that `EXISTS` and `IN` produce the exact query plan, based on the number of actual rows scanned in each steps. Thus, `EXISTS` and `IN` basically are the same in terms of performance. The `JOIN` is pretty much the same except for the Sort and Unique steps. The worst case complexity is $O(M+N)$ (Hash Inner Join)
- In conclusion, we can see that there isn't much difference between `EXISTS`, `IN` and `JOIN` in checking the existence of a value, as the DBMS has already optimised and chose the best query plan to execute for us already.[^1]
- However, that is only the case if the query is well written in order for the performance to be good, as a badly-written query would be badly interpreted, thus results in bad performance. [^4]
```SQL
select *
from customers
where exists(select 1
			 from orders
			 where customer_id - order_customer_id = 0 and to_char(order_date, 'yyyy-MM') = '2014-01');
```
![](Images/Pasted%20image%2020240703211423.png)
#### NOT EXISTS, NOT IN
##### NOT EXISTS
- The `NOT EXISTS` functions mostly the same as the `EXISTS`. Since it's a predicate, not a `JOIN` condition, the rows from the subquery can only be returned at most once too. `NOT EXISTS` always returns `TRUE` or `FALSE`, it will return `FALSE` as soon as it finds only a single matching row from the subquery, or `TRUE`, if it find none. Logically, `NOT EXISTS` would have the subquery run once for every row in the main query to be determined if a row **do not** exist. 
	- Right when the subquery finds a row, it exits immediately and the return value is false. 
	- Else, it is true. 
	- The selected column(s) of the subquery **does not matter** as the result is tied only to the existence or non-existence of a resulting row based on the FROM/JOIN/WHERE clauses in the subquery.
- Query:
```sql
select *
from customers
where not exists(select 1
			 from orders
			 where customer_id = order_customer_id and to_char(order_date, 'yyyy-MM') = '2014-01');
	
```
- Query finishes in 87msec
- Query plan:
![](Images/Pasted%20image%2020240703222320.png)
##### NOT IN
- However, `NOT IN` is not the same as `IN` as `NOT NULL` is still `NULL`, which is not an escape condition. Logically, think of it as having every row in the main query scan the result list from the subquery
	- If a matching value is found and it is not `NULL`, the return value is false. 
	- If a matching value is not found and the list does not contain `NULL` value, the return value is true
	- If the matching value is not found and there is a `NULL` value in the list, the return value is `NULL`
	- If the value is `NULL`, the return value is `NULL`
- Query:
```sql
select *
from customers
where customer_id not in (select order_customer_id
					  from orders
					  where to_char(order_date, 'yyyy-MM') = '2014-01');
```
- Query finishes in 132msec
- Query plan:
![](Images/Pasted%20image%2020240703222549.png)
##### LEFT JOIN / IS NULL
- Query:
```sql
select *
from customers
left join (select distinct order_customer_id
	  from orders 
	  where to_char(order_date, 'yyyy-MM') = '2014-01') as orders on order_customer_id = customer_id
where order_customer_id is null
```
- Query finishes in 120msec
- Query plan:
![](Images/Pasted%20image%2020240703223610.png)
##### NOT EXISTS vs NOT IN vs LEFT JOIN / IS NULL

- `NOT EXISTS` and `LEFT JOIN / IS NULL` have similar query plans, both utilising Hash Anti Join (worst case $O(M+N)$), while `NOT IN` (for a non-`NULL` query) performs two nested sequential scans ($O(MN)$), which can potentially lead to worse performance in a large database.
- In summary, one should use `NOT EXISTS` or `LEFT JOIN / IS NULL` to check for the absence of a value from a list. However, if you need to perform the same task while distinguishing `NULL` values, you should use `NOT IN`.
## References

[^1]: [Difference between EXISTS and IN in SQL? - Stack Overflow](https://stackoverflow.com/questions/24929/difference-between-exists-and-in-in-sql)
[^2]: [NOT IN vs. NOT EXISTS vs. LEFT JOIN / IS NULL: SQL Server at EXPLAIN EXTENDED](https://explainextended.com/2009/09/15/not-in-vs-not-exists-vs-left-join-is-null-sql-server/)
[^3]: [SQL EXISTS vs IN vs JOIN Performance Comparison](https://www.mssqltips.com/sqlservertip/6659/sql-exists-vs-in-vs-join-performance-comparison/)
[^4]: [IN vs. JOIN vs. EXISTS at EXPLAIN EXTENDED](https://explainextended.com/2009/06/16/in-vs-join-vs-exists/)