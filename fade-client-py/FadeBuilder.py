import dill as pickle
from uuid import uuid4


def serialize(fn, *args, **kwargs):
    name = uuid4().hex
    with open(name, "wb") as f:
        pickle.dump([fn.__name__, args, kwargs], f)
    return name


def deserialize(key):
    with open(key, "rb") as f:
        des = pickle.load(f)
        return des
