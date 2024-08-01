10 keys, 30mil values

|                          | GroupByKey                               | ReduceByKey                              |
| ------------------------ | ---------------------------------------- | ---------------------------------------- |
| 1 core, 14 partitions    | Duration: 33s<br>Shuffle Write: 187.0MiB | Duration: 43s<br>Shuffle Write: 10.3KiB  |
| 4 cores, 1 partitions    | Duration: 31s<br>Shuffle Write: 187.0MiB | Duration: 29s<br>Shuffle Write: 224.0B   |
| 4 cores, 14 partitions   | Duration: 12s<br>Shuffle Write: 187.0MiB | Duration: 14s<br>Shuffle Write: 10.3KiB  |
| 4 cores, 100 partitions  | Duration: 6s<br>Shuffle Write: 187.0MiB  | Duration: 8s<br>Shuffle Write: 72.5KiB   |
| 4 cores, 200 partitions  | Duration: 18s<br>Shuffle Write: 187.1MiB | Duration: 9s<br>Shuffle Write: 144.1KiB  |
| 4 cores, 1000 partitions | Duration: 18s<br>Shuffle Write: 187.5MiB | Duration: 23s<br>Shuffle Write: 718.8KiB |
![](Pasted%20image%2020240730213813.png)
10000 keys, 50mil values

|                          | GroupByKey                               | ReduceByKey                              |
| ------------------------ | ---------------------------------------- | ---------------------------------------- |
| 1 core, 22 partitions    | Duration: 46s<br>Shuffle Write: 240.7MiB | Duration: 53s<br>Shuffle Write: 2.9MiB   |
| 4 cores, 1 partitions    | Duration: 55s<br>Shuffle Write: 238.9MiB | Duration: 44s<br>Shuffle Write: 144.8KiB |
| 4 cores, 22 partitions   | Duration: 17s<br>Shuffle Write: 240.7MiB | Duration: 20s<br>Shuffle Write: 2.8MiB   |
| 4 cores, 100 partitions  | Duration: 12s<br>Shuffle Write: 248.3MiB | Duration: 20s<br>Shuffle Write: 13.6MiB  |
| 4 cores, 200 partitions  | Duration: 23s<br>Shuffle Write: 258.9MiB | Duration: 27s<br>Shuffle Write: 29.1MiB  |
| 4 cores, 1000 partitions | Duration: 27s<br>Shuffle Write: 410.0MiB | Duration: 38s<br>Shuffle Write: 215.0MiB |
![](Pasted%20image%2020240730213800.png)
Observations:
- `groupByKey` shuffles data a lot, on average 10 times more than `reduceByKey`
- The duration of `groupByKey` and `reduceByKey` don't have much difference
- `groupByKey` groups all the values according to their key
	- It returns an RDD of `(key, Iterable[values])` pairs 
	- Shuffle → RDD of `(key, Iterable[values])` → Aggregate
	- `groupByKey` can cause out of disk problems as data is sent over the network and collected on the reduced workers. [^1]
- `reduceByKey` groups the values according to their key, applies a specified reduction function to combine them into a single value per key. 
	- It returns an RDD of `(key, reducedValue)` pairs
	- Aggregate on each partition → RDD of `(key, reducedValue)` → Shuffle → Aggregate
	- `reduceByKey` combines data at each partition, with only one output for one key at each partition to send over the network

`groupByKey`
Initial data
```
1: (a, 1), (b, 4), (c, 3), (a, 4), (c, 3)
2: (a, 5), (b, 2), (a, 2), (c, 3)
3: (b, 4), (c, 1), (c, 3)
```
Shuffle
```
1: (a, [1, 4, 5, 2])
2: (b, [4, 2, 4])
3: (c, [3, 3, 3, 1, 3])
```
Aggregate
```
1: (a, 12)
2: (b, 10)
3: (c, 13)
```

`reduceByKey`
Initial data
```
1: (a, 1), (b, 4), (c, 3), (a, 4), (c, 3)
2: (a, 5), (b, 2), (a, 2), (c, 3)
3: (b, 4), (c, 1), (c, 3)
```
Aggregate
```
1: (a, 5), (b, 4), (c, 6)
2: (a, 7), (b, 2), (c, 3)
3: (b, 4), (c, 4)
```
Shuffle
```
1: (a, 5), (a, 7)
2: (b, 4), (b, 2), (b, 4)
3: (c, 6), (c, 3), (c, 4)
```
Aggregate
```
1: (a, 12)
2: (b, 10)
3: (c, 13)
```
