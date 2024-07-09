## TL;DR

Creating a comparison table for different types of objects used in SQL like Common Table Expressions (CTE), Views, Temporary Tables, Table Variables, and Inline Table-Valued Functions (TVF) can help illustrate their differences:

| Feature                 | CTE                | View              | Temporary Table                                   | Table Variable                      | Inline TVF                        |
| ----------------------- | ------------------ | ----------------- | ------------------------------------------------- | ----------------------------------- | --------------------------------- |
| **Scope**               | Statement-specific | Database-wide     | Session-specific or Transaction-specific          | Function-specific or batch-specific | Function-specific                 |
| **Storage**             | None (Virtual)     | Stored (as query) | Disk (TempDB)                                     | Disk (TempDB)                       | None (Virtual)                    |
| **Usage**               | Reusable within    | Reusable          | Storing intermediate results                      | Holding small intermediate results  | Reusable within                   |
| **Modifiability**       | Static             | Dynamic           | Dynamic                                           | Dynamic                             | Dynamic                           |
| **Performance**         | Depends on query   | Pre-compiled      | Generally faster                                  | Faster than temp tables             | Inline execution context-specific |
| **Indexing**            | No                 | Yes               | Yes                                               | No                                  | No                                |
| **Transaction control** | Follows query      | Follows database  | Yes                                               | Yes                                 | Follows query                     |
| **As parameters**       | No                 | No                | No                                                | Yes                                 | No                                |
| **Takes parameters**    | No                 | No                | No                                                | No                                  | Yes                               |
| **Visibility**          | Only within CTE    | Database-wide     | Session-specific (Local) or Session-wide (Global) | Function or batch scope             | Only within the function          |

## CTE (Common Table Expression)
```sql
WITH cte_name AS (QUERY)
```
- A temporary result set that you can reference within a query using `SELECT`, `INSERT`, `UPDATE`, `DELETE`, etc.
- Defined using `WITH` clause
- Why do we use CTEs over Subquery/Derived Table:
	- Readable and maintainable: CTEs allow you to define and name the complex part of the query first, separate them from the rest
	- Recursive CTEs
- Limitations:
	- Their scope is one *statement* (not one query, as multiple queries can use the same CTE: if nested, in other CTEs, etc.). If you want to reference a result set multiple times, you should use [temp table](#Temp%20Table) [^1]
	- Performance(?)
- Recursive CTE:
	- Structured in two parts:
		- Anchor member (Base case)
		- Recursive member (Recursive loop + Quit condition)
	- Tips for writing Recursive CTEs [^3]:
		- Start with anchor
		- Ensure the number of columns match
		- Always `UNION ALL`
		- Beware Infinite Loops (Pay attention to quit condition and anchor)
- Recursive CTE in PostgreSQL:
```sql
WITH RECURSIVE recursive_cte_name AS (
	(anchor)
	UNION ALL
	(recursive_logic WHERE exit_condition)
)
```
e.g.
1. Normal CTE
```sql
WITH class_monitor AS (
	SELECT *
	FROM students
	WHERE is_class_monitor = True
)
SELECT *
FROM class_monitor
```
2. Recursive CTE [^2]
```sql
WITH RECURSIVE cte (n, factorial) AS (
	VALUES (0, 1) --f0, f1
	UNION ALL
	SELECT n+1, (n+1)*factorial FROM cte WHERE n<9
)
```
Step by step execution:
![|250](Pasted%20image%2020240709161456.png)

3. Recursive CTE to get hierarchy of staff [^3]
```sql
WITH employee_manager_cte AS (
	SELECT id, name, manager_id, 1 as level
	FROM employees e1
	WHERE manager_id IS NULL -- get the topmost employee i.e. the director
	UNION ALL
	SELECT
	FROM employees AS employee
	INNER JOIN employee_manager_cte manager ON employee.manager_id = manager.id
)
SELECT level, id, name, manager_id
FROM employee_manager_cte
```
The hierarchy is like this:
![|300](Pasted%20image%2020240709163334.png)
And the result

| level | id  | name        | manager_id |
| ----- | --- | ----------- | ---------- |
| 1     | 91  | Sarah Smith | NULL       |
| 2     | 92  | Jane Miller | 91         |
| 3     | 93  | John Doe    | 92         |

## View
```sql
CREATE VIEW view_name AS (QUERY);
```
- Virtual table retrieves data from tables when queried
- Does not store the data itself [^4]
- Does not take storage space but rather use memory and processing power
- How does view work? Two ways [^4] [^5]
	- Any query referring to the view is rewritten to include the query defined in the view
	- View is executed alone and the result set is stored in a [temporary table](#Temp%20Table) 
- Can you update data through a view?
	- The view must not certain SQL functions (like aggregate functions, `DISTINCT`, etc.)
	- The view must reference a single base table
	- All the columns do not allow NULLs and no default values
- Why do we use view?
	- Organising and structuring data
	- Simplifying complex queries: Encapsulate complex queries into something table-like (but not taking up storage space)
	- Security: Restrict access to specific columns or rows, exposing only the necessary data to users or applications i.e. Some users could see certain columns in a view, but does not have the access to the whole table
	- Data Abstraction: Provide an abstraction layer, allowing underlying table schema changes without affecting dependent queries
- Limitations:
	- Non-updatable views, update with a lot of restrictions
	- No indexing, making it less efficient compared to indexed base tables
	- If schema changes, the views referencing it have to be updated as well
		- Hard to manage dependencies
		- Cascading effects if views referencing views
- Materialised View:
	- Materialised views precompute and store the results of a query physically on disk
	- Used to improve performance for frequently executed queries by avoiding rerunning resource-intensive queries multiple times
	- Why not just use temporary table? (?)
## Temporary Table
```sql
CREATE TEMP TABLE temp_table_name (TABLE DEFINITION)
```
- Store results temporarily or isolating subsets of data for processing
- For local temporary table, theirs scope is one session or one transaction. Global temporary table is accessible by any session. (PostgreSQL does not support local/global. SQL Server does)
- Temporary tables are stored in a database for temporary objects
- Why do we use Temporary Table?
	- Store intermediate results
	- Break down complex queries into smaller steps
	- Isolate subsets of data for specific operations without affecting the base tables
	- Processing large datasets [^7]
	- If data needs to be shared across sessions, use global temporary tables (?) [^7]
- Limitations:
	- Consume significant memory and storage space if not managed properly
	- Temporary tables are disposed of before you can debug theirs content (?) [^7]
	- (Global temporary table) No isolation as these tables are accessible by other sessions [^7]
- When to use Temporary Table over Table Variable? [^6] [^7]
	- Indexing
	- Adding and deleting large numbers of rows
	- Large dataset (Millions of bytes)
	- Transaction
## Table Variable
```sql
DECLARE @table_variable_name TABLE (TABLE DEFINITION)
```
- A variable that holds a set of data like a table, but it's scoped to the batch, stored procedure, or function in which it's declared
- theirs scope is one routine (batch, stored procedure, function, etc.) where they are declared
- Table variables are not affected by transaction rollbacks, as they do not participate in transaction *explicitly* (?)
- Better performance for small to medium-sized dataset compared to temporary tables due to theirs reduced overhead and simpler structure
- Why do we use Table Variable?
	- Store intermediate results
	- Transaction rollback passerby: TVs are not affected by rollback operations
	- Processing small to medium-sized datasets [^7]
- Limitations:
	- Cannot alter the structure of a table variable after declaration
	- Statistics are not maintained on table variables, leading to less efficient query plans for large datasets (?)
- When to use Table Variable over Temporary Table?
	- Small, less complex datasets
	- Few locking resources (?) [^8]
	- Limited to scope, reducing side effects on system (?) [^8]
	- Free memory early [^7]
## Inline TVFs (Inline Table-Valued Function)
```sql
  CREATE FUNCTION function_name (@param datatype)
  RETURNS TABLE
  AS RETURN (QUERY)
```
- A function that returns a table
- Returns an entire result set, which can be used in queries much like a regular table or view
- Why do we use inline TVFs?
	- Simplifying complex queries
	- Allow parameters and return table value
- Limitations:
	- Cannot contain control flow statements like `IF`, `CASE`, `WHILE`
	- Security: You have to grant `SELECT` permission to the users who need to query it

[^1]: [sql - Use one CTE many times - Stack Overflow](https://stackoverflow.com/questions/10196808/use-one-cte-many-times)
[^2]: [Common Table Expressions (WITH Queries)](https://www.cockroachlabs.com/docs/stable/common-table-expressions)
[^3]: [How to Write a Recursive CTE in SQL Server | LearnSQL.com](https://learnsql.com/blog/recursive-cte-sql-server/)
[^4]: [do MYSQL views occupy physical space? - Database Administrators Stack Exchange](https://dba.stackexchange.com/questions/39924/do-mysql-views-occupy-physical-space)
[^5]: [PostgreSQL: Documentation: 16: 41.2. Views and the Rule System](https://www.postgresql.org/docs/current/rules-views.html)
[^6]: [t sql - What's the difference between a temp table and table variable in SQL Server? - Database Administrators Stack Exchange](https://dba.stackexchange.com/questions/16385/whats-the-difference-between-a-temp-table-and-table-variable-in-sql-server)
[^7]: [When should I use a table variable vs temporary table in sql server? - Stack Overflow](https://stackoverflow.com/questions/11857789/when-should-i-use-a-table-variable-vs-temporary-table-in-sql-server)
[^8]: [Temporary Tables in SQL Server - Simple Talk](https://www.red-gate.com/simple-talk/databases/sql-server/t-sql-programming-sql-server/temporary-tables-in-sql-server/)