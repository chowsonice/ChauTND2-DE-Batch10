## Exercise 1: Compare Filter Before and After Join
### RDD

Unfiltered Join with RDD: 29.78 seconds
Execution plan:
![|400](Pasted%20image%2020240808084222.png)
Filtered Join with RDD: 2.51 seconds
Stages:
![](Pasted%20image%2020240808090127.png)
Lineage graph:
![|400](Pasted%20image%2020240808084449.png)

### Dataframe 


### Filter before Join
Parsed Logical Plan
```sql
== Parsed Logical Plan ==
Join Inner
:- Filter order_status IN (COMPLETE,CLOSED)
:  +- Project 
:     +- Relation csv
+- Filter (order_item_product_id= 127)
   +- Project 
      +- Relation csv
```

Optimized Logical Plan
```sql
== Optimized Logical Plan ==
Join Inner
:- Project 
:  +- Filter 
:     +- Relation csv
+- Project 
   +- Filter 
      +- Relation csv
```

Physical Plan
```sql
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=true
+- == Final Plan ==
   *(2) BroadcastHashJoin 
   :- ShuffleQueryStage 
   :  +- Exchange SinglePartition
   :     +- *(1) Project 
   :        +- *(1) Filter
   :           +- FileScan csv 
   +- *(2) Project 
      +- *(2) Filter
         +- FileScan csv 
```

## Exercise 2: Multi-worker and Partitions
1 worker 1 partition
![](Pasted%20image%2020240806212653.png)
![](Pasted%20image%2020240806212704.png)

1 worker 2 partitions
![](Pasted%20image%2020240806214816.png)
![](Pasted%20image%2020240806214751.png)

1 worker 40 partitions
![](Pasted%20image%2020240806212203.png)
![](Pasted%20image%2020240806212138.png)

4 workers 2 partitions
![](Pasted%20image%2020240806214702.png)
![](Pasted%20image%2020240806214726.png)


4 workers 40 partitions
![](Pasted%20image%2020240806211552.png)
![](Pasted%20image%2020240806211705.png)
![](Pasted%20image%2020240806211724.png)

|                                 |     |
| ------------------------------- | --- |
| <b>1 worker, 2 partitions</b>   |     |
| <b>1 worker, 2 partitions</b>   |     |
| <b>4 workers, 40 partitions</b> |     |
| <b>1 worker, 40 partitions</b>  |     |
