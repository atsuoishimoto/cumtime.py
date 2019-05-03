from cumtime import Cumtime, register
import time, re

def test_cum():
    c = Cumtime()

    c.begin('t1')
    time.sleep(0.01)
    c.end()

    with c('t1'):
        time.sleep(0.01)

    assert re.match(r't1: sum:[\d.]+ n:2 ave:[\d.]+$', str(c))


def test_cum2():

    register('cum')
    cum.begin('t1')
    cum.begin('t2')
    time.sleep(0.01)
    cum.end('ttt1')

    assert re.search(r't1: sum:[\d.]+ n:1 ave:[\d.]+\n'
                     r't2: sum:[\d.]+ n:1 ave:[\d.]+', str(cum))


def test_deco():
    c = Cumtime()

    @c('func1_deco')
    def func1():
        pass

    func1()
    assert re.match(r'func1_deco: sum:[\d.]+ n:1 ave:[\d.]+$', str(c))

    c = Cumtime()
    @c
    def func2():
        pass

    func2()
    assert re.match(r'test_deco.<locals>.func2: sum:[\d.]+ n:1 ave:[\d.]+$', str(c))
