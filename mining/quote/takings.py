#coding:utf-8
import os, sys
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import time
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'gather/quote')
STOCK_FILE = os.path.join(SOURCE_DIR, "stock.txt")
PROFIT_DIR = os.path.join(SOURCE_DIR, "profit")
PIC_DIR = os.path.join(BASE_DIR, 'takings')


def autolabel(rects): 
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '%s' % float(height))

def produce_pic(code):
    print 'product %s netprofit' % code
    profit_file = os.path.join(PROFIT_DIR, "%s.csv" % code)
    raw = []
    with open(profit_file, 'rb') as f:
        for line in f:
            _js = json.loads(line)
            for dic in _js['list']:
                raw.append((dic['reportdate'], int(dic['netprofit']) / 10000))
    data = sorted(raw, key=lambda x:x[0])
    print data
    dates = [datetime.strptime(x[0], '%Y%m%d') for x in data]
    values = [x[1] for x in data]
    plt.plot_date(dt.date2num(dates), values, linestyle='-', label='NP', color='red')
    plt.xlabel('date')
    plt.ylabel('netprofit')
    plt.title('history')
    plt.grid()
    plt.legend()

    plt.autoscale(enable=True)
    plt.savefig(os.path.join(PIC_DIR, '%s.png' % code))


def run():
    with open(STOCK_FILE, 'rb') as f:
        for code in f:
            produce_pic(code.strip())


if '__main__' == __name__:
    import time
    start_at = time.time()
    print 'begin at: %s' % start_at
    run()
    print 'end at: %s and used %s' % (time.time(), time.time() -start_at)




#plt.xlabel('x')
#plt.ylabel('y')
#plt.xticks((0,1), ('man', 'woman'))
#plt.title('man and woman')
#rect = plt.bar(left = (0, 1), height = (1, 0.5), width=0.35, align='center', yerr=0.000001)
#
#plt.legend((rect,), ('tuli',))
#autolabel(rect)
#
#plt.savefig('000.png')
#plt.show()
