# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from colors import getRandomColors

Aguojin = {
    u'民生银行': 44512,
    u'浦发银行': 1287,
    u'宝钢股份': 12705,
    u'保利地产': 45315,
    u'兴业银行': 15678,
    u'工商银行': 13064,
    u'中国建筑': 10080,
    u'建设银行': 39216,
    u'秦港股份': 2340,
    u'双汇发展': 36261,
    u'白云山': 34924.12,
    u'澳博控股': 51061.47,
    u'cash': 40002.8 + 2947.38,
}

Yguojin = {
    u'浦发银行': 34749,
    u'cash': 28223.34,
}

Htai = {
    u'民生银行': 18832,
    u'恒生ETF': 15150,
    u'兴业银行': 12194,
    u'华宝油气': 5280,
    u'50ETF': 3486.6,
    u'广发医药': 2911.8,
    u'创业ETF': 1381.8,
    u'万家强债': 981,
    u'cash': 11065.7 + 1039.1,
}

Ttjj = {
    u'广发养老': 6497.72,
    u'广发医药': 5956.2,
    u'中证红利': 4675.99,
    u'国开债': 4227.35,
    u'广发环保': 3062.32,
    u'德国30': 1286.36,
    u'中证500': 1200.84,
    u'信用债': 1101.15,
    u'创业板ETF': 1081.48,
    u'建信500': 1030.16,
}

usd_rate = 6.87
Bmy = {
    u'老凤祥': 3024,
    u'cash': 9.12,
}

hkd_rate = 0.87
Bgb = {
    u'粤高速': 51903,
    u'长安B': 44333,
    u'cash': 496.74,
}

###################################################################

Bmy_real = dict([ (x, Bmy[x] * usd_rate) for x in Bmy ])
Bgb_real = dict([ (x, Bgb[x] * hkd_rate) for x in Bgb ])

total = {}

for dic in [Aguojin, Yguojin, Htai, Ttjj, Bmy_real, Bgb_real]:
    for k, v in dic.iteritems():
        if k in total:
            v += total[k]
        total[k] = v


labels = total.keys()
X = total.values()


fig = plt.figure()
plt.pie(X,labels=labels, colors=getRandomColors(len(labels)), autopct='%2.1f%%', pctdistance=0.8) #画饼图（数据，数据对应的标签，百分数保留两位小数点）
plt.title(int(sum(X)))
plt.axis('equal')
plt.legend()

plt.show()
plt.savefig("AllPie.png")
