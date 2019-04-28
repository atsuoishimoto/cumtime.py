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

    assert re.search(r't2: sum:[\d.]+ n:1 ave:[\d.]+\n'
                     r't1: sum:[\d.]+ n:1 ave:[\d.]+', str(cum))
