import re, collections, time, contextlib, statistics, atexit
from functools import wraps

__version__ = '0.3.0'

def register(name, print_exit=False):
    Cumtime(name=name, print_exit=print_exit)


class Cumtime:
    def __init__(self, name=None, print_exit=False):
        self.suspended = False
        self.reset()
        if print_exit:
            atexit.register(self.print)

        if name:
            import builtins

            setattr(builtins, name, self)

    def reset(self):
        self._map = collections.defaultdict(list)
        self._stack = []

    def suspend(self):
        self.suspended = True

    def resume(self):
        self.suspended = False

    def begin(self, name):
        if not self.suspended:
            self._stack.append((name, time.time()))

    def end(self, name=None):
        if not self.suspended:
            while self._stack:
                n, f = self._stack.pop()
                self._map[n].append(time.time() - f)

                if (not name) or (n == name):
                    break

    def __call__(self, name_or_func):
        c = self

        if callable(name_or_func):

            @wraps(name_or_func)
            def wrapper(*args, **kwargs):
                c.begin(name_or_func.__qualname__)
                try:
                    return name_or_func(*args, **kwargs)
                finally:
                    c.end(name_or_func.__qualname__)

            return wrapper

        class cumcontext:
            def __enter__(self):
                c.begin(name_or_func)

            def __exit__(self, exc_type, exc_value, traceback):
                c.end(name_or_func)

            def __call__(self, func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    c.begin(name_or_func)
                    try:
                        return func(*args, **kwargs)
                    finally:
                        c.end(name_or_func)

                return wrapper

        return cumcontext()

    def _calc(self, name=None):
        l = self._map.get(name, None)
        if l is None:
            return (0, 0, 0)
        else:
            return (sum(l), len(l), statistics.mean(l))

    FMT = "{name}:\tsum:{_sum:.5f} n:{_len} ave:{_ave:.5f}"

    def get_lines(self, name=None, sort_sum=True):
        if name:
            names = [n for n in self._map if re.match(name, str(n))]
        else:
            names = self._map.keys()

        all = [(name, *self._calc(name)) for name in names]
        if sort_sum:
            all.sort(key=lambda e: (e[1], e[0]))
        else:
            all.sort(key=lambda e: e[0])

        ret = []
        for name, _sum, _len, _ave in all:
            ret.append(self.FMT.format(name=name, _sum=_sum, _len=_len, _ave=_ave))

        return "\n".join(ret)

    def print(self, name=None, sort_sum=True):
        print(self.get_lines(name, sort_sum))

    def __str__(self):
        return self.get_lines(sort_sum=False)
