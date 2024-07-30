from random import randint

with open('numbers-10m.txt', 'w') as file:
    try:
        for i in range (1, 10000001):
            file.write(str(randint(1, 1000000000)) + ' ')
    finally:
        file.close()