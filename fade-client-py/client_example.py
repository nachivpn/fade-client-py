import pickle as dill


def x(a, b): return [a + b, a - b]


def main():
    args = ["x", 5, 3]
    dill.dump(args, open("ser", "wb"))

if __name__ == "__main__":
    main()
