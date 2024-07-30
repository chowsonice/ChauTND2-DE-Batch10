from pyspark import SparkConf, SparkContext
from math import sqrt, floor

conf = SparkConf().setMaster("local") \
                    .setAppName("Prime number from 10m")
sc = SparkContext(conf=conf)

def parseNumbers(line):
    numbers = []
    number_texts = line.split(' ')
    for number_text in number_texts:
        try:
            numbers.append(int(number_text))
        except:
            print(number_text)
    return numbers

def check_if_prime(number):
    for i in range(2, floor(sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True

line = sc.textFile("./numbers-10m.txt")
numbers = line.flatMap(parseNumbers)
prime_numbers = numbers.filter(check_if_prime)
results = prime_numbers.collect()

with open('./prime-numbers-10m.txt', 'w') as file:
    for result in results:
        file.write(str(result) + ' ')
