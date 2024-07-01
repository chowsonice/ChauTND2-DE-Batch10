## Find functions that can be used with subquery and learn how these functions are executed logically and explain performance differences

### Functions that can be used with a subquery that returns a value
- Operators like =, >, <, >=, <=
- After processing the subquery, it executes like a ordinary conditional query
### Functions that can be used with a subquery that returns a column
#### ANY, ALL
##### ALL
`ALL` returns TRUE if condition is met with *all* of the subquery values
> e.g.
> - We can see that a sequential scan on table order_items is executed
> - Each row of order_items go through a second sequential scan to compare if the value of order_items.order_item_subtotal >= sub_order_items.order_item_subtotal. 
> - Materialize is used to optimize the query by storing the result temporarily so that it could be accessed multiple times without re-running the subquery

![](Pasted%20image%2020240701163440.png)
 ![](Pasted%20image%2020240701155639.png)
##### ANY
`ANY` returns TRUE if the condition is met with *any* of the subquery values
> e.g.
> - We can see that there is a join between order_items and sub_order_items, join condition is order_items.order_item_subtotal >= sub_order_items.order_item_subtotal
> - Then we get the values of the order_items table left after the filter

![](Pasted%20image%2020240701183741.png)
![](Pasted%20image%2020240701183019.png)
#### EXISTS, IN
- `EXISTS` returns TRUE if the subquery returns at least one record meeting the condition
- `column IN [value1, value2, ...]` is the same as multiple `OR` conditions `column=value1 OR column=value2` 
- `EXISTS` has more use cases than `IN` as `IN` only check if there is any match in value (equal condition)
### Functions that can be used with a subquery that returns a table