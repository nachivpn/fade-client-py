import dill


def serialize(fn, *args, **kwargs):
    ser = lambda: fn(*args, **kwargs)
    with open("ser" + fn.__name__) as f:
        dill.dump(ser, f)


def deserialize(key):
    with open(key) as f:
        des = dill.load(f)
        return des
