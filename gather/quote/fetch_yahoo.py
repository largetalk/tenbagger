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
        print '%s quote file already exists' % code
    else:
        cmd = "wget -t 10 %s%s.%s -O %s" % (WGET_URL, code, m, target_file)
        print 'fetch data : %s' % cmd
        sub = Popen([cmd], stdout=PIPE, shell=True)
        out, err = sub.communicate()
        print out.rstrip()

def clean_empty():
    for f in os.listdir(DATA_DIR):
        if f.endswith('.csv') and os.path.getsize(os.path.join(DATA_DIR, f)) < 10:
            print 'clean emtpy file ', f
            os.remove(os.path.join(DATA_DIR, f))

def run():
    with open(STOCK_FILE, 'rb') as f:
        for code in f:
            pool.spawn(worker, code.strip())
    pool.join()
    clean_empty()


if '__main__' == __name__:
    import time
    start_at = time.time()
    print 'begin at: %s' % start_at
    run()
    print 'end at: %s and used %s' % (time.time(), time.time() - start_at)
