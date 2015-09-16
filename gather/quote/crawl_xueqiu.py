#coding:utf-8
import gevent.monkey

gevent.monkey.patch_socket()

from gevent.pool import Pool
from gevent.subprocess import Popen, PIPE
import os
import sys
import urllib2
import gevent
import time
import json
from pyquery import PyQuery as pq

POOL_NUM = 2
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STOCK_FILE = os.path.join(BASE_DIR, "stock.txt")
COMPANY_DIR = os.path.join(BASE_DIR, 'company')
COMPANY_URL = 'http://xueqiu.com/stock/f10/compinfo.json?symbol=%s&page=1&size=4&_=%s'

FINANCE_URL = 'http://xueqiu.com/stock/f10/finmainindex.json?symbol=%s&page=%s&size=4&_=%s'
PROFIT_DIR = os.path.join(BASE_DIR, 'profit')

REFER_URL = 'http://xueqiu.com/S/%s/GSJJ'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
COOKIE = "bid=a035a6b006ec49f7f248a63a965693a9_i52hgmsa; s=qfx112w4tb; last_account=largetalk%40gmail.com; xq_a_token=20c1d5317ac17b0eab6552e85284b960876be91d; xq_r_token=43362ebbe2c45cf7fb176cef9765031df7e53415; __utmt=1; __utma=1.902613933.1421581010.1442409028.1442416328.224; __utmb=1.1.10.1442416328; __utmc=1; __utmz=1.1440922786.211.11.utmcsr=weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/u/3820776504; Hm_lvt_1db88642e346389874251b5a1eded6e3=1440922786,1442156845,1442409028; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1442416328"

pool = Pool(POOL_NUM)
extract_pool = Pool(POOL_NUM)


def judgeMarket(code):
    if str(code).startswith('6'):
        return 'SH'
    else:
        return 'SZ'

def crawl_company(code):
    m = judgeMarket(code)
    print 'start process company %s%s' % (m, code)
    target_file = os.path.join(COMPANY_DIR, '%s.csv' % code)
    if os.path.exists(target_file):
        print '%s company file already exists' % code
    else:
        url = COMPANY_URL % (m + code, int(time.time() * 1000))
        print 'crawl url : %s' % url
        try:
            headers = {'User-Agent': UA, 'Referer': REFER_URL % (m+code), "Cookie": COOKIE}
            req = urllib2.Request(url, headers=headers)
            resp = urllib2.urlopen(req, timeout=10)
            status = resp.code
            content = resp.read()
            print 'crawl %s status: %s' % (code, status)
            dumps_company(code, target_file, content)
        except Exception, e:
            print 'crawl %s err: %s' % (code, str(e))

def dumps_company(code, file, data):
    try:
        print 'dumps %s file' % code
        #dic = json.loads(data)
        with open(file, 'w') as f:
            f.write(data)
    except Exception, e:
        print 'dumps %s error: %s' % (code, str(e))

def crawl_profit(code):
    m = judgeMarket(code)
    print 'start process profit %s%s' % (m, code)
    target_file = os.path.join(PROFIT_DIR, '%s.csv' % code)
    if os.path.exists(target_file):
        print '%s profit file already exists' % code
    else:
        page = 1
        headers = {'User-Agent': UA, 'Referer': REFER_URL % (m+code), "Cookie": COOKIE}
        while True:
            url = FINANCE_URL % (m + code, page, int(time.time() * 1000))
            print 'crawl url : %s' % url
            try:
                req = urllib2.Request(url, headers=headers)
                resp = urllib2.urlopen(req, timeout=10)
                status = resp.code
                content = resp.read()
                if len(content) > 20:
                    print 'dumps %s profit page %s' % (code, page)
                    dumps_profit(code, target_file, content)
                    page += 1
                else:
                    print 'crawl %s profit end, page %s' % (code, page)
                    break
            except Exception, e:
                print 'crawl %s err: %s' % (code, str(e))
                break

def dumps_profit(code, file, data):
    try:
        with open(file, 'a') as f:
            f.write(data)
            f.write('\r\n')
    except Exception, e:
        print 'dumps %s profit error: %s' % (code, str(e))

def clean_empty():
    for f in os.listdir(COMPANY_DIR):
        if f.endswith('.csv') and os.path.getsize(os.path.join(COMPANY_DIR, f)) < 10:
            print 'clean emtpy company file ', f
            os.remove(os.path.join(COMPANY_DIR, f))
    for f in os.listdir(PROFIT_DIR):
        if f.endswith('.csv') and os.path.getsize(os.path.join(PROFIT_DIR, f)) < 10:
            print 'clean emtpy profit file ', f
            os.remove(os.path.join(PROFIT_DIR, f))

def run():
    with open(STOCK_FILE, 'rb') as f:
        for code in f:
            pool.spawn(crawl_company, code.strip())
            pool.spawn(crawl_profit, code.strip())
    pool.join()
    clean_empty()

if '__main__' == __name__:
    import time
    start_at = time.time()
    print 'begin at: %s' % start_at
    run()
    print 'end at: %s and used %s' % (time.time(), time.time() - start_at)
