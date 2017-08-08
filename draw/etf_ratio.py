# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from colors import getRandomColors

Htai = {
    u'恒生ETF': 15150,
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


total = {}
for dic in [ Htai, Ttjj ]:
    for k, v in dic.iteritems():
        if k in total:
            v += total[k]
        total[k] = v


X = sorted(total.values())
labels = sorted(total, key=total.get)

fig = plt.figure()
plt.pie(X,labels=labels, colors=getRandomColors(len(labels)), autopct='%2.1f%%', pctdistance=0.8) #画饼图（数据，数据对应的标签，百分数保留两位小数点）
plt.title(int(sum(X)))
plt.axis('equal')
plt.legend()

plt.show()
plt.savefig("EtfPie.png")
