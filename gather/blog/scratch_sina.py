#coding:utf-8
import gevent
import gevent.monkey

gevent.monkey.patch_socket()

from gevent.pool import Pool
from gevent.subprocess import Popen, PIPE
from gevent.queue import Queue
import os
import sys
import urllib2
import gevent
import time
import json
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Tag
#from pyquery import PyQuery as pq

POOL_NUM = 2
SLEEP_SEC = 1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICAL_FILE = os.path.join(BASE_DIR, "sjcyp.txt")
URL_FILE = os.path.join(BASE_DIR, "url.txt")
FAIL_LOG = os.path.join(BASE_DIR, 'fail.log')
START_URL = 'http://blog.sina.com.cn/s/articlelist_1576966507_0_%s.html'
START_IDX = 12


REFER_URL = 'http://xueqiu.com'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
COOKIE = "bid=a035a6b006ec49f7f248a63a965693a9_i52hgmsa; s=qfx112w4tb; last_account=largetalk%40gmail.com; xq_a_token=20c1d5317ac17b0eab6552e85284b960876be91d; xq_r_token=43362ebbe2c45cf7fb176cef9765031df7e53415; __utmt=1; __utma=1.902613933.1421581010.1442409028.1442416328.224; __utmb=1.1.10.1442416328; __utmc=1; __utmz=1.1440922786.211.11.utmcsr=weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/u/3820776504; Hm_lvt_1db88642e346389874251b5a1eded6e3=1440922786,1442156845,1442409028; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1442416328"

pool = Pool(POOL_NUM)
queue = Queue()
log = open(FAIL_LOG, 'w')

def crawl_url():
    furl = open(URL_FILE, 'w')
    for idx in range(START_IDX, 0, -1):
        gevent.sleep(SLEEP_SEC)
        url = START_URL % idx
        print 'start  fetch url %s' % url
        try:
            headers = {'User-Agent': UA, 'Referer': REFER_URL, "Cookie": COOKIE}
            req = urllib2.Request(url, headers=headers)
            resp = urllib2.urlopen(req, timeout=10)
            status = resp.code
            content = resp.read()
            print 'crawl idx %s status: %s' % (idx, status)
            if status != 200:
                log_fail("craw idx %s failed, status is %s" % (idx, status))
                log_fail(content)
                continue
            process_list_page(content, furl)
        except Exception, e:
            print 'crawl %s err: %s' % (idx, str(e))
            log_fail(e.message)
    furl.close()

regs = [re.compile("<!\xe2\x80\x93\[if.*\]>"), re.compile("<!\[endif\]\xe2\x80\x93>")]

def clean_err_tag(content):
    for reg in regs:
        for s in reg.findall(content):
            content = content.replace(s, '')
    return content

def process_list_page(content, furl):
    content = clean_err_tag(content)
    soup = BeautifulSoup(content)
    blocks = soup.findAll(name='span', attrs={'class': 'atc_title'})
    if len(blocks) < 1:
        log_fail("can't parse span.atc_title")
        return
    for block in reversed(blocks):
        url = block.find('a').get('href')
        furl.write('%s\n' % url)
        queue.put(url)

def log_fail(msg):
    if msg:
        log.write(msg)
        log.write('\n')

def crawl_page():
    fw = open(ARTICAL_FILE, 'a+')
    try:
        while True:
            gevent.sleep(SLEEP_SEC)
            url = queue.get(timeout=10)
            headers = {'User-Agent': UA, 'Referer': REFER_URL, "Cookie": COOKIE}
            req = urllib2.Request(url, headers=headers)
            resp = urllib2.urlopen(req, timeout=10)
            status = resp.code
            content = resp.read()
            print 'crawl page %s status: %s' % (url, status)
            if status != 200:
                log_fail("craw url %s failed, status is %s" % (url, status))
                log_fail(content)
                continue
            process_page(content, fw)
    except Exception, e:
        print e
    fw.close()

def process_page(content, fw):
    content = clean_err_tag(content)
    soup = BeautifulSoup(content)
    title_tag = soup.find('h2', attrs={'class': 'titName SG_txta'})
    zw_tag = soup.find('div', attrs={'class': 'articalContent   '})
    if zw_tag is None:
        zw_tag = soup.find('div', attrs={'class': 'articalContent   newfont_family'})
        if zw_tag is None:
            log_fail("can't find content for %s" % title_tag)
            return

    title = title_tag.text.encode('utf8') if title_tag else ''
    print title
    zw_lst = zw_tag.contents
    zw = ''.join([t.text.encode('utf8') if isinstance(t, Tag) else str(t) for t in zw_lst])

    fw.write('Title:%s\n----------\n\n\n' % title)
    fw.write('Body:%s\n' % zw)
    fw.write("=================================================================================================\n\n")


def run():
    pool.spawn(crawl_url)
    pool.spawn(crawl_page)
    pool.join()

if '__main__' == __name__:
    import time
    start_at = time.time()
    print 'begin at: %s' % start_at
    run()
    print 'end at: %s and used %s' % (time.time(), time.time() - start_at)
