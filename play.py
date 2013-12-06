__author__ = 'root'

from multiprocessing import Pool
from time import sleep
import os

def f(x):
    print(x,os.getpid())
    return x*x
    sleep(1000)


if __name__ == '__main__':
    print(os.getpid())
    pool = Pool(processes=4)              # start 4 worker processes
    result = pool.apply_async(f, [10000])    # evaluate "f(10)" asynchronously
    print result.get(timeout=1)           # prints "100" unless your computer is *very* slow
    print pool.map(f, range(50))          # prints "[0, 1, 4,..., 81]"
    sleep(10000)
