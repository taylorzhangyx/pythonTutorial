
def main():
    kwargs = {'k1': 1, 'k2': 2}

    func(**kwargs)

def func(**kwargs): # ** wrap all the keyward arguments into a dictionary
    for k in kwargs:
        print(k)

if __name__ == "__main__":
    main()