from time import perf_counter


def fibonacci_r(n):
    if n < 2:
        return n
    return fibonacci_r(n - 1) + fibonacci_r(n - 2)


def fibonacci_i(n):
    if n < 2:
        return n
    a, b = 1, 0
    for _ in range(n - 1):
        a, b = a + b, a
    return a


def benchFunc(f, e, label="algo"):
    t1 = perf_counter()
    r = f(e)
    p = perf_counter() - t1
    print("{0} result : {1}  | time : {2}".format(label, r, p))
    return p, r


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        n = int(sys.argv[1])
    else:
        n = 10

    p_r, r_r = benchFunc(fibonacci_r, n, "rec")
    p_i, r_i = benchFunc(fibonacci_i, n, "ite")
