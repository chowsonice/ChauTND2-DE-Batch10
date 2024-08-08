from pyspark import SparkConf, SparkContext
from time import sleep

conf = SparkConf().setMaster("local[4]") \
                .setAppName("Average by key") \
                .set("spark.executor.instances", "4") \
                .set("spark.executor.cores", "4") \
                .set("spark.executor.memory", "8g") \
                .set("spark.dynamicAllocation.enabled", "true") \
                .set("spark.dynamicAllocation.minExecutors", "1") \
                .set("spark.dynamicAllocation.maxExecutors", "10") \

sc = SparkContext(conf=conf)

print(sc.uiWebUrl)

def parseLine(line):
    fields = line.split(' ')
    key = int(fields[0])
    value = int(fields[1])
    return (key, value)

lines = sc.textFile('./key-value-10m-3.txt')
rdd = lines.map(parseLine)


        
# ######### use reduceByKey()

def reduceByKeyJob(rdd):
    rdd.toDebugString()
    averages = rdd.mapValues(lambda x : (x, 1)) \
                    .reduceByKey(lambda x, y : (x[0] + y[0], x[1] + y[1])) \
                    .mapValues(lambda x : x[0] / x[1]) \
                    .sortByKey() \
                    .collect()

    with open('key-value-average-3.txt', 'w') as file:
        for average in averages:
            file.write(str(average[0]) + ' ' + str(average[1]) + '\n')

reduceByKeyJob(rdd)


