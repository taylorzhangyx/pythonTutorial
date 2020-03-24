#!/usr/bin/env python3

class Duck:
    count = 0

    def quack(self):
        print('Quaaack!')

    def walk(self):
        print('Walks like a duck.')

def main():
    donald = Duck()
    donald.quack()
    donald.walk()
    donald.count = 9
    print(f'donald count {donald.count}')

    drill = Duck() # so Duck() is equal to new a class
    print(f'drill count {drill.count}')
    drill.count = 3
    print(f'drill count {drill.count}')

if __name__ == '__main__': main()
