#!/usr/bin/env python3

def main():
    x= [1,2,3,4]
    # print(f'{map}, type: {type(map)}')
    kitten(*x) # x is unpacked here to be a list of arguments that are passed into the function

def kitten(*args):
    # It's expecting a list of args to be passed in
    if len(args):
        for s in args:
            print(s)
    else: print('Meow.')

if __name__ == '__main__': main()
