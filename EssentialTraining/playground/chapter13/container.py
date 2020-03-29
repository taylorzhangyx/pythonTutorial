#!/usr/bin/env python3
x = (1,3,4,5,6)
y = (2,33,54)
z = zip(y,x)
print(f'z - {z}')

for a,b in z:
    print(f'a-{a} b-{b}')


m = ('game','life', 'tada')
for i, string in enumerate(m):
    print(f'{i}, {string}')
