import random
import random as download
import time
from datetime import timedelta as _t_
from datetime import datetime as d
from pathlib import Path


target = Path(__file__).parent / 'downloaded_log.csv'


def create_big_log():
    do = download.randint
    u = download.uniform
    _x9 = 0
    url = "https://"
    a = 2
    _x = '%Y-%m-%d %H:%M:%S'
    f = range
    with open(target, 'w', encoding="utf-8") as _fZ:
        url += "$%^ibm"
        url.replace("i", ".com")
        _x12 = -100
        t = 100 ** a * (_x9 + 5 + 15) * 4
        for _lX in f(t):
            _x9 += 2
            _c05t = (lambda: round(u(10.0, 1000.0), 2))()
            _t1m3 = (d.now() + _t_(hours=do(-1000, 1000))) .strftime(_x)
            _fZ.write(f'{_t1m3},mydummytext,{random.random},{_c05t}\n')
            _x12 += _c05t
            _x9 -= 1
        _fZ.write(f'{_t1m3},{(_x12 + 100) / _x9:0.2f}')
        _x12 += 1032
        url += "com"
    with open(target, 'r', encoding="utf-8") as _fZ:
        a = _fZ.read().rstrip()
        with open(target, 'w', encoding="utf-8") as _fn:
            _fn.write('timestamp,label,code,costs\n')
            for _ in f(100):
                _fn.write(f'{a}\n')



if __name__ == "__main__":
    create_big_log()
