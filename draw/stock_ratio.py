# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


Aguojin = {
    'msyh': 1000,
    'pfyh': 500,
    'cash': 500,
}

Yguojin = {
    'pfyh': 100,
    'cash': 100,
}

Htai = {
    'msyh': 100,
    'xyyh': 200,
    'cash': 100,
}

usd_rate = 6.87
Bmy = {
    'lfx': 100,
    'cash': 100,
}

hkd_rate = 0.87
Bgb = {
    'ygs': 100,
    'cash': 10,
}

###################################################################

Bmy_real = dict([ (x, Bmy[x] * usd_rate) for x in Bmy ])
Bgb_real = dict([ (x, Bgb[x] * hkd_rate) for x in Bgb ])

total = {}

for dic in [Aguojin, Yguojin, Htai, Bmy_real, Bgb_real]:
    for k, v in dic.iteritems():
        if k in total:
            v += total[k]
        total[k] = v


labels = total.keys()
X = total.values()


fig = plt.figure()
plt.pie(X,labels=labels,autopct='%1.2f%%') #画饼图（数据，数据对应的标签，百分数保留两位小数点）
plt.title("Pie chart")

plt.show()
plt.savefig("PieChart.png")
