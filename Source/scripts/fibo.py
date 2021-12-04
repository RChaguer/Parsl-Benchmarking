from time import perf_counter
import pandas as pd
from parsl.app.app import python_app, join_app
from parsl import load
from algos import fibonacci_i, fibonacci_r, benchFunc
import configs as cfg

outputFolder = "bench_outputs/"

def benchParslFunc(f, e, label="algo"):
    t1 = perf_counter()
    r = f(e).result()
    p = perf_counter() - t1
    print("{0} result : {1} | time : {2}".format(label, r, p))
    return p, r


@python_app
def add(*args):
    acc = 0
    for v in args:
        acc += v
    return acc


@join_app
def fibonacci(n):
    if n == 0:
        return add()
    elif n == 1:
        return add(1)
    else:
        return add(fibonacci(n - 2), fibonacci(n - 1))
        
def test_py_fibonacci(n, saveFile=None):
    p_r, r_r = benchFunc(fibonacci_r, n, "rec normal")

    p_i, r_i = benchFunc(fibonacci_i, n, "iter normal")

    if saveFile is not None:
        column_names = ["c", "n", "r", "t"]
        df = pd.DataFrame([
                            ['py_rec', n, p_r, r_r],
                            ['py_iter', n, p_i, r_i],
                        ], columns=column_names)
        df.to_csv(f'{outputFolder}{saveFile}.csv', mode='a', index=False, header=False)


def test_parsl_fibonacci(n, saveFile=None, c=""):

    p_c, r_p = benchParslFunc(fibonacci, n, f"rec parsl {c}")

    if saveFile is not None:
        column_names = ["c", "n", "r", "t"]
        df = pd.DataFrame([
                            [f'parsl_{c}', n, p_c, r_p]
                        ], columns=column_names)
        df.to_csv(f'{outputFolder}{saveFile}.csv', mode='a', index=False, header=False)

if __name__ == '__main__':
    import sys
    arg_names = ['command', 't', 'n', 'c', 's']
    args = dict(zip(arg_names, sys.argv))
    if str(args.get('n', "")).isdigit():
        n = int(args['n'])
    else:
        n = 10

    if args.get('c', "") == 'htex':
        c = "htex"
        # from parsl.configs.htex_local import config
        load(cfg.h_config)
    elif args.get('c', "") == 'thread':
        c = "thread"
        # from parsl.configs.local_threads import config
        load(cfg.t_config)
    else:
        c = ""

    if args.get('s', "") != "":
        saveFile = args.get('s')
    else:
        saveFile = None

    if args.get('t', "all") == "all":
        test_py_fibonacci(n, saveFile)
        test_parsl_fibonacci(n, saveFile, c)
    elif args.get('t') == "py":
        test_py_fibonacci(n, saveFile)
    elif args.get('t') == "parsl":
        test_parsl_fibonacci(n, saveFile, c)