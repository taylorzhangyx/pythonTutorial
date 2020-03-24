#!/usr/bin/env python3

sequence = [ 1, 2, 3, 4, 5 ]
tup = (1, 2, 3, 4, 5)
diction = {1:'one', 2:'two'}
for i in sequence:
    print('i is {}'.format(i))
    print(f'types are {type(i)} id is {id(i)}')

for i in tup:
    print(f'i is {i}')

for i,j in diction.items():
    print(f'i is {i}, j is {j}')

str1 = 'string'
str2 = 'string'
print(f'type of tup is {type(tup)}')
print(f'type of sequence is {type(sequence)}')
print(f'{id(str1)}, {isinstance(str1, str)}')