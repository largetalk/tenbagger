#coding:utf-8
from gevent.pool import Pool
from gevent.subprocess import Popen, PIPE
import os
import sys
import gevent

POOL_NUM = 2
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STOCK_FILE = os.path.join(BASE_DIR, "stock.txt")
DATA_DIR = os.path.join(BASE_DIR, 'data')
WGET_URL = 'http://table.finance.yahoo.com/table.csv?s='

pool = Pool(POOL_NUM)

def judgeMarket(code):
    if str(code).startswith('6'):
        return 'ss'
    else:
        return 'sz'

def worker(code):
    m = judgeMarket(code)
    print 'start process %s.%s' % (code, m)
    target_file = os.path.join(DATA_DIR, '%s.csv' % code)
    if os.path.exists(target_file):
        print '%s quote file already exists'
    else:
        cmd = "wget %s%s.%s -O %s" % (WGET_URL, code, m, target_file)
        print 'fetch data : %s' % cmd
        sub = Popen([cmd], stdout=PIPE, shell=True)
        out, err = sub.communicate()
        print out.rstrip()

def run():
    with open(STOCK_FILE, 'rb') as f:
        for code in f:
            pool.spawn(worker, code.strip())
    pool.join()


if '__main__' == __name__:
    import time
    start_at = time.time()
    print 'begin at: %s' % start_at
    run()
    print 'end at:% %s and used %s' %s (time.time(), time.time() - start_at)
