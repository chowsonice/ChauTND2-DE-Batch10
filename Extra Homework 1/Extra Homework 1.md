## What is Index
- Data structure
- Used to improve speed of read operations at the cost of additional writes and storage space
## Types of Index
- Clustered Index
- Non-clustered Index
## When to use Index
## Advantages and Disadvantages
### Advantages
- Improve performance for search, join, sort, group, etc.
### Disadvantages
- Bad practices could easily lead to worse performance
- Consume disk space
- Performance overhead for Write operations
- Index management and maintenance

## How Indices work
### A. B-tree 
- Main components [^1] [^2]:
	- Leaf pages contain many index rows. An index row contains:
		- Indexed data (Key)
		- Reference to table row (TIDs - Tuple IDs)
	- Non-leaf pages, or internal pages: Reference a child page of the index with the minimum value in this page
- B-tree is suitable for data that can be sorted [^2]
- Average case complexity of search operations on this data structure is $O(\log n)$
![](Pasted%20image%2020240717152117.png)
![](Pasted%20image%2020240717134141.png)
Search operation on B-tree Index:
e.g. `select * from table where value >=24 and value <= 65`
- It searches `value = 24` first. If there is no match, it gets the closest greater value to 24
- Similarly, it searches `value = 65`. If there is no match, it gets the closest lesser value to 65
![](Pasted%20image%2020240717145248.png)
![](SCR-20240717-tcee-2.gif)
### B. Hash
- Any data type
- Suitable for data with only equality comparison (id, etc.)
- Main components:
	- Bucket page: store data as `hash_code - TID` pairs
	- Overflow page - Bitmap page: When a bucket overflows (out of the page), overflow page stores the `hash_code - TID` and bitmap pages store information on spare overflow pages
e.g. We want to search for the row with `id=102`
![](Pasted%20image%2020240717213800.png)
### C. Bitmap
- Suitable for data with limited distinct values
- Bitmap index includes rows with NULL values
e.g.  We have the CUSTOMER table like this:
![](Pasted%20image%2020240718084509.png)
- We want to query on `marital_status`, `region=west` and `region=central`
	- Each bit in the bitmap corresponds to a single row of the CUSTOMER table
	- The bitmap index would be like:
	  ![](Pasted%20image%2020240718084525.png)
- Query: Count number of *married* customers living in the *central or west regions*
  ```sql
  SELECT COUNT(*) 
  FROM customer  
  WHERE marital_status = 'married' 
  AND region IN ('central','west');
  ```

![](Pasted%20image%2020240718084718.png)
- It executes some bitwise operations and count the number of 1 in the final result

|                    | B-tree                                                                                               | Hash                                                                                                | Bitmap                                                                                                                                                                                    |
| ------------------ | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Structure          | Tree with balanced nodes                                                                             | Hash table                                                                                          | Bitmap                                                                                                                                                                                    |
| Best for           | - Range searches<br>- Operations on sorted data<br>e.g. Find all rows with value between 100 and 200 | - Point queries (look up matches)<br>- Data with high cardinality<br>e.g. Find employee with id=123 | - Operations on data with low cardinality (few distinct values, like categorical attributes)<br>- Complex queries with multiple conditions<br>e.g. Count employee with state='is_working' |
| Advantages         | Range queries                                                                                        | Equality queries                                                                                    | Complex queries                                                                                                                                                                           |
| Limitations        | Equality queries                                                                                     | Range queries<br>Queries with low cardinality                                                       | High cardinality                                                                                                                                                                          |
| Insertion/Deletion | Costly, due to rebalancing                                                                           | Simple and fast                                                                                     | Simple, but can degrade with frequent updates                                                                                                                                             |
| Use Cases          | Ordered data, range searches                                                                         | Unique key lookups                                                                                  | Read-heavy environments                                                                                                                                                                   |

## D. Other Data Structure
- [GiST](https://postgrespro.com/blog/pgsql/4175817): Generalised Search Tree
- [SP-GiST](https://postgrespro.com/blog/pgsql/4220639): Space-partitioned Generalised Search Tree
- [GIN](https://postgrespro.com/blog/pgsql/4261647): Generalised Inverted Index
- [RUM](https://postgrespro.com/blog/pgsql/4262305): Improved GIN
- [BRIN](https://postgrespro.com/blog/pgsql/4262305): Block Range Index
- Other functionality-based index, specialised for that operations
- Some DBMS allow you to specify the type of index you want to create, some don't but they will evaluate your data and query and choose suitable index

--- 
## Index in SQL Server
- Clustered index
- Non-clustered index
- Multi-key index

## Index in PostgreSQL
- Create index *only* on what you need, maybe for operations that would be frequently used
- Index - Row ratio needs to be taken into consideration. Too large index table only takes more time
- Index scan - Index-only scan
- Hiện tượng:
	- Khi có index lại chậm hơn, tại sao?

## Index in MySQL
- R-tree
- Multi-column indexing
- Sử dụng index trên những cột đa dạng, high cardinality

Bảng luôn cần update data, vậy thì có nên index không? Cân bằng giữa hiệu suất search và hiệu suất update, cân bằng các phép search trên các cột hay bị sửa đổi
Join mà có index, update mà có index (?)

Nên trình bày ví dụ sơ qua trước khi nói về điều rút được

[^1]: [B-trees - CS Cornell](https://www.cs.cornell.edu/courses/cs3110/2012sp/recitations/rec25-B-trees/rec25.html)
[^2]: [Indexes in PostgreSQL — 4 (B-tree) : Postgres Professional](https://postgrespro.com/blog/pgsql/4161516)
[^3]: [Indexes in PostgreSQL — 3 (Hash) : Postgres Professional](https://postgrespro.com/blog/pgsql/4161321)
[^4]: [Indexes](https://docs.oracle.com/cd/A83908_02/NT816EE/DOC/server.816/a76994/indexes.htm)