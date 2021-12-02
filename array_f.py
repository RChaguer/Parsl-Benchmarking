from time import perf_counter, sleep
from threading import Thread
from multiprocessing import Process
import pandas as pd
from parsl.app.app import python_app
from parsl import load
import configs as cfg

def benchFunc(f, e, dur=None, label="algo"):
    t1 = perf_counter()
    f(e, dur)
    p = perf_counter() - t1
    print("{0} | time : {1}".format(label, p))
    return p


def benchFunc_t(f, e, t_h, dur=None, label="algo"):
    t1 = perf_counter()
    f(e, t_h, dur)
    p = perf_counter() - t1
    print("{0} | time : {1}".format(label, p))
    return p


@python_app
def array_apply_p(f, x, s, e, dur=None):
    from time import sleep
    for i in range(s, e):
        if dur is not None:
            sleep(dur)
        x[i] = f(x[i])
    return x


def array_apply(f, x, s, e, dur=None):
    for i in range(s, e):
        if dur is not None:
            sleep(dur)
        x[i] = f(x[i])
    return x


def array_square(x, dur=None):
    array_apply(lambda a: a * a, x, 0, len(x), dur)


def array_square_p(x, t_h=64, dur=None):
    l_f = []
    for l in range(0, len(x), t_h):
        l_f.append(array_apply_p(lambda a: a * a, x, l, l + t_h, dur))
    for f in l_f:
        f.result()


def array_square_t(x, t_h=64, dur=None):
    l_t = []
    for l in range(0, len(x), t_h):
        l_t.append(Thread(target=array_apply, args=(lambda a: a * a, x, l, l + t_h, dur)))
    for t in l_t:
        t.start()
    for t in l_t:
        t.join()


def array_square_mp(x, t_h=64, dur=None):
    l_mp = []
    for l in range(0, len(x), t_h):
        l_mp.append(Process(target=array_apply, args=(lambda a: a * a, x, l, l + t_h, dur)))
    for p in l_mp:
        p.start()
    for p in l_mp:
        p.join()


def test_py_array_square(n, dur=None, saveFile=None):
    p_i = benchFunc(array_square, n, dur, "normal")
    if saveFile is not None:
        column_names = ["c", "n", "t_h", "dur", "t"]
        df = pd.DataFrame([
                            ['py', len(n), t_h, dur, p_i],
                        ], columns=column_names)
        df.to_csv(f'{saveFile}.csv', mode='a', index=False, header=False)


def test_parsl_array_square(n, t_h, dur=None, saveFile=None, c=""):

    p_c = benchFunc_t(array_square_p, n, t_h, dur, f"parsl {c}")

    if saveFile is not None:
        column_names = ["c", "n", "t_h", "dur", "t"]
        df = pd.DataFrame([
                            [f'parsl_{c}', len(n), t_h, dur, p_c]
                        ], columns=column_names)
        df.to_csv(f'{saveFile}.csv', mode='a', index=False, header=False)


def test_threading_array_square(n, t_h, dur=None, saveFile=None, c=""):

    p_c = benchFunc_t(array_square_t, n, t_h, dur, "threading")

    if saveFile is not None:
        column_names = ["c", "n", "t_h", "dur", "t"]
        df = pd.DataFrame([
                            ['threading', len(n), t_h, dur, p_c]
                        ], columns=column_names)
        df.to_csv(f'{saveFile}.csv', mode='a', index=False, header=False)


def test_multiprocess_array_square(n, t_h, dur=None, saveFile=None, c=""):

    p_c = benchFunc_t(array_square_mp, n, t_h, dur, "multiprocess")

    if saveFile is not None:
        column_names = ["c", "n", "t_h", "dur", "t"]
        df = pd.DataFrame([
                            ['multiprocess', len(n), t_h, dur, p_c]
                        ], columns=column_names)
        df.to_csv(f'{saveFile}.csv', mode='a', index=False, header=False)


if __name__ == '__main__':
    import sys
    arg_names = ['command', 't', 'n', 'c', 't_h', 'dur', 's']
    args = dict(zip(arg_names, sys.argv))
    if str(args.get('n', "")).isdigit():
        n = int(args['n'])
    else:
        n = 10

    if str(args.get('t_h', "")).isdigit():
        t_h = int(args['t_h'])
    else:
        t_h = 64

    try:
        dur = float(args['dur'])
    except ValueError:
        dur = None

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
        x = [2.] * (1024 * n)
        test_py_array_square(x, dur, saveFile)
        x = [2.] * (1024 * n)
        test_parsl_array_square(x, t_h, dur, saveFile, c)
        x = [2.] * (1024 * n)
        test_threading_array_square(x, t_h, dur, saveFile, c)
    elif args.get('t') == "py":
        x = [2.] * (1024 * n)
        test_py_array_square(x, dur, saveFile)
    elif args.get('t') == "parsl":
        x = [2.] * (1024 * n)
        test_parsl_array_square(x, t_h, dur, saveFile, c)
    elif args.get('t') == "t":
        x = [2.] * (1024 * n)
        test_threading_array_square(x, t_h, dur, saveFile, c)
    elif args.get('t') == "mp":
        x = [2.] * (1024 * n)
        test_multiprocess_array_square(x, t_h, dur, saveFile, c)
