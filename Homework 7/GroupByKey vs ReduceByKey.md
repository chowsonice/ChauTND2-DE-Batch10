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