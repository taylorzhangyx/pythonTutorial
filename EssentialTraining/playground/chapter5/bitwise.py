#!/usr/bin/env python3

x = 1 <<2
y = 99999
z = x | y

print(f'(hex) x is {x:02x}, y is {y:02x}, z is {z:02x}')
print(f'(bin) x is {x:010b}, y is {y:08b}, z is {z:08b}')

