#!/usr/bin/env python3

def main():
    infile = open('berlin.jpg', 'rb')
    outfile = open('berlin-copy.jpg', 'wb')
    count = 0
    while True:
        buf = infile.read(11240)
        if buf:
            outfile.write(buf)
            print(f'.', end='', flush=True)
        else: break
    outfile.close()
    print('\ndone.')

if __name__ == '__main__': main()
