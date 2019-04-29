#coding:utf-8
from django.db import models
from datetime import date
from datetime import timedelta
from decimal import Decimal

class DailyStats(models.Model):
    date = models.DateField(primary_key=True)
    median_close = models.DecimalField(default=0, max_digits=6,decimal_places=3)

    def __str__(self):
        return 'DailyStats %s (mc: %s)' % (self.date, self.median_close)
