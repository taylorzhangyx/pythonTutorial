import random


def putNumInCounter(number, set, max=1000000):
    leng = len(set)
    # print(f'i is {leng}, number is {number}')
    i = number//(max//leng)
    set[i] += 1
    return set


counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(99999999):
    counter = putNumInCounter(random.randint(1, 999999), counter)

print(f'random count: {counter}')
