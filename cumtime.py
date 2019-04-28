import collections, time, contextlib, statistics, atexit


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

    @contextlib.contextmanager
    def __call__(self, name):
        self.begin(name)
        yield self
        self.end(name)
        return

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
        return '\n'.join(self._str(n) for n in self._map)


