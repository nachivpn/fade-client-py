import pickle as dill
import importlib
import sys


def load(ser_file, module_name):
    client_module = importlib.import_module(module_name)

    des = dill.load(ser_file)

    return client_module, des


def run(client_module, des):
    function_name = des[0]
    args = des[1]
    kwargs = des[2]

    try:
        function = client_module.__dict__[function_name]
        res = function(*args, **kwargs)
    except BaseException as e:
        res = e

    return res


def save(res_file, res):
    with open(res_file, "wb") as h:
        dill.dump(res, h)


def main():
    """ Expects:
            arg1 - module where target function is.
            arg2 - file where serialized data is.
            arg3 - file where to serialize output.
    """

    with open(sys.argv[2], "rb") as f:
        client_module, des = load(f, sys.argv[1])

        res = run(client_module, des)

        save(sys.argv[3], res)


if __name__ == "__main__":
    main()
