#!/usr/bin/env python3

x = '''
multiline string {1:<012}
seven {0:>23}
'''.format(11,22)
print('x is {}'.format(x))
print(type(x))

a = 1
print('a is {}'.format(a))
print(type(a))

b = 2.2
print('b is {}'.format(b))
print(type(b))

c = .1+ .1+ .1- .3
d = 11 / 3
e = 11 //3
print(f'c is {c}, d is {d}, e is {e}')
print(f'{type(c)} {type(d)} {type(e)}')
