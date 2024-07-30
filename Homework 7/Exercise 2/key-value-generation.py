from random import randint, shuffle

pairs = []
count = 0
for i in range(1, 10):
    n_pair = randint(1, 10000000)
    for j in range(1, n_pair+1):
        pairs.append((i, randint(1, 1000000000)))
        count += 1
        if (count == 10000000):
            break
    if (count == 10000000):
        break
        
shuffle(pairs)

with open('key-value-10m-3.txt', 'w') as file:
    try:
        for pair in pairs:
            file.write(str(pair[0]) + ' ' + str(pair[1]) + '\n')
    finally:
        file.close()