#!/usr/bin/env python3

import time

def elapsed_time(f):
    def wrapper():
        t1 = time.time()
        f()
        t2 = time.time()
        print(f'Elapsed time: {(t2 - t1) * 1000} ms')
    return wrapper

def executingLog(f):
    def wrapper():
        print(f'function {f.__name__} is executing')
        f()
        print(f'function {f.__name__} is executed')
    return wrapper

@elapsed_time
@executingLog
def big_sum():
    num_list = []
    for num in (range(0, 10000)):
        num_list.append(num)
    print(f'Big sum: {sum(num_list)}')

def main():
    big_sum()

if __name__ == '__main__': main()
