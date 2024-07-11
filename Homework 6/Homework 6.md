## `CROSS APPLY`/`LATERAL JOIN`
- `JOIN` operator 
- `CROSS APPLY`/`LATERAL JOIN` ≈ `INNER JOIN`
- `OUTER APPLY`/`LATERAL LEFT JOIN` ≈ `LEFT JOIN`
- Functions similarly to `JOIN` but have join condition use correlated subquery (?) (`HAVING`, etc.)
- `APPLY` always run a nested loop, take each row from the **left** table and scan for a set of rows from the **right** table that would satisfy the condition for that row (with a subquery or a function)
- Why do we use `APPLY`/`LATERAL JOIN` over `JOIN`?
	- `APPLY` works better on things that have no easy `JOIN` condition (correlated join).
	- `APPLY` could enable table functions with parameters to be executed once per row and then joined to the results
- Limitations:
	- Readability: If the same results could replace with a simple `JOIN`, use `JOIN` (to spare someone's sanity)[^1]
	- Performance: If the subquery is not optimised, it could cost a lot of time and resources (Unoptimised search, lots of join, etc.)
![|500](Images/Pasted%20image%2020240711091041.png)
e.g. Get the top 3 products for each orders
1. `CROSS APPLY`/`LATERAL JOIN`
- The query:
```sql
select order_id, order_item_product_id
from (select * from orders limit 100) as orders
left join lateral (select order_item_product_id
			  from order_items 
			  where order_id = order_item_order_id
			  order by order_item_product_id
			  limit 3) as top_3_item on true;
```
- The query plan:
![](Images/Pasted%20image%2020240711102533.png)
2. `INNER JOIN`:
- The query:
```sql
select order_id, order_item_product_id
from (select * from orders limit 100) as orders
join (select * 
	  from (
		  select order_item_order_id, order_item_product_id, row_number() over (partition by order_item_order_id order by order_item_product_id) as rn
		  from order_items
	  ) as order_items
where rn <= 3) as top_3_order_item on order_id = order_item_order_id
order by order_id;
```
- The query plan:
![](Images/Pasted%20image%2020240711102909.png)

3. Conclusion
- Some observations for the queries:
	- `INNER JOIN` has to sequential scan, sort and calculate `ROW_NUMBER()` for the whole right table (`order_items`) and then merge join it with the left table (`orders`)
	- `INNER JOIN`'s complexity in this query is approximately $O(2n\log n)$  
	- `APPLY`/`LATERAL JOIN` despite not having to calculate `ROW_NUMER()` for the whole right table, it spends too much time on the subquery (sequential scan and filter)
	- If we improve the search performance in the subquery by using index, the performance would *significantly* improve and it would yield even better result than `INNER JOIN`
	- `APPLY`/`LATERAL JOIN`'s complexity in this query is $O(n^2)$ if without index, $O(n\log n)$ with index
- Thus, you should use `APPLY` with intention

![](Images/Pasted%20image%2020240711093541.png)



[^1]: [SQL Server CROSS APPLY and OUTER APPLY](https://www.mssqltips.com/sqlservertip/1958/sql-server-cross-apply-and-outer-apply/)
[^2]: [sql - When should I use CROSS APPLY over INNER JOIN? - Stack Overflow](https://stackoverflow.com/questions/1139160/when-should-i-use-cross-apply-over-inner-join)
[^3]: [SQL Server CROSS APPLY and OUTER APPLY](https://www.mssqltips.com/sqlservertip/1958/sql-server-cross-apply-and-outer-apply/)