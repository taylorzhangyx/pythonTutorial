#!/usr/bin/env python3

secret = 'psword'
pw = None
maxAttempt = 4
count = 0
while pw != secret:
    count += 1
    if count == maxAttempt:
        break
    if count == 3:
        print('One last chance')
    pw = input("What's the secret word? ")
else:
    print(f'Password is matched')
