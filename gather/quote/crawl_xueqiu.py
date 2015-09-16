#coding:utf-8
import gevent.monkey

gevent.monkey.patch_socket()

from gevent.pool import Pool
from gevent.subprocess import Popen, PIPE
import os
import sys
import gevent
from pyquery import PyQuery as pq

POOL_NUM = 2
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STOCK_FILE = os.path.join(BASE_DIR, "stock.txt")
COMPANY_DIR = os.path.join(BASE_DIR, 'company')
COMPANY_URL = 'http://xueqiu.com/S/'

pool = Pool(POOL_NUM)


def judgeMarket(code):
    if str(code).startswith('6'):
        return 'SH'
    else:
        return 'SZ'

def crawl_company(code):
    m = judgeMarket(code)
    print 'start process %s%s' % (m, code)
    target_file = os.path.join(COMPANY_DIR, '%s.csv' % code)
    if os.path.exists(target_file):
        print '%s company file already exists' % code
    else:
        url = '%s%s%s' % (COMPANY_URL, m, code)
        print 'crawl url : %s' % url
        try:
            req = urllib2.Request(url)
            resp = urllib2.urlopen(req, timeout=10)
            status = resp.code
            content = resp.read()
            print 'crawl %s status: %s' % (code, status)
            pool.spawn(extract, target_file, content)
        except Exception, e:
            print 'crawl %s err: %s' % (code, str(e))


def extract(target_file, data):
    pass

def clean_empty():
    for f in os.listdir(COMPANY_DIR):
        if f.endswith('.csv') and os.path.getsize(os.path.join(COMPANY_DIR, f)) < 10:
            print 'clean emtpy file ', f
            os.remove(os.path.join(COMPANY_DIR, f))

def run():
    with open(STOCK_FILE, 'rb') as f:
        for code in f:
            pool.spawn(crawl_company, code.strip())
    pool.join()
    clean_empty()


if '__main__' == __name__:
    import time
    start_at = time.time()
    print 'begin at: %s' % start_at
    run()
    print 'end at: %s and used %s' % (time.time(), time.time() - start_at)
