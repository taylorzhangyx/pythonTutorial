#!/usr/bin/env python3

import platform

def main():
    message()

def message():
    print('This is python version {}'.format(platform.python_version()))
    
    # a blank line will not break the method. Only the indentation will define the method.
    print('line 2')

if __name__ == '__main__': main()
