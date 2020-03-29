#!/usr/bin/env python3

def main():
    f0 = open('lines.txt', 'rt');
    f = open('lines_1.txt','at')
    for line in f0:
        print(line.rstrip(), file=f)
    f.writeline('something good')
    f.close()
if __name__ == '__main__': main()
