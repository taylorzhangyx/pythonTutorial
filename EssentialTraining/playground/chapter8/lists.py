#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/

def main():
    game = ['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
    del game[0]
    
    print_list('.'.join(game))

def print_list(o):
    for i in o: print(i, end=' ', flush=True)
    print()

if __name__ == '__main__': main()
