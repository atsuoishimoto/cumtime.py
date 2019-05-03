import collections, time, contextlib, statistics, atexit
from functools import wraps

def register(name, print_exit=False):
    Cumtime(name=name, print_exit=print_exit)


class Cumtime:
    def __init__(self, name=None, print_exit=False):
        self.reset()
        if print_exit:
            atexit.register(self.print)

        if name:
            import builtins
            setattr(builtins, name, self)

    def reset(self):
        self._map = collections.defaultdict(list)
        self._stack = []

    def begin(self, name):
        self._stack.append((name, time.time()))

    def end(self, name=None):
        while self._stack:
            n, f = self._stack.pop()
            self._map[n].append(time.time()-f)

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

    def print(self, name=None):
        if name:
            print(self._str(name))
        else:
            for name in self._map.keys():
                print(self._str(name))

    def _str(self, name):
        l = self._map[name]
        return ('%s: sum:%.5f n:%d ave:%.5f' % (name, sum(l), len(l),
              statistics.mean(l)))


    def __str__(self):
        names = sorted(self._map)
        return '\n'.join(self._str(n) for n in names)


