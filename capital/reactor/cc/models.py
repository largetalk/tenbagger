#coding:utf-8
from django.db import models
from utils.bm import BaseModel
from datetime import date
from datetime import timedelta
from decimal import Decimal

_DUE_DAY_PAY = 'A'
_DUE_PERIOD_PAY = 'B'
_CARD_TYPE_CHOICES = ((_DUE_DAY_PAY, '指定还款日'), (_DUE_PERIOD_PAY, '定长还款期'))
class CreditCard(BaseModel):
    name = models.CharField(max_length=100)
    tail_no = models.IntegerField()
    bill_day = models.PositiveSmallIntegerField()
    card_type = models.CharField(max_length = 5, choices=_CARD_TYPE_CHOICES, default=_DUE_DAY_PAY)
    due_day = models.PositiveSmallIntegerField(null=True, blank=True)
    due_period = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return '%s(%s)' % (self.name, self.tail_no)


    def find_next_due_day(self, day=date.today):
        bill_day = date(day.year, day.month, self.bill_day)
        if bill_day < day:
            if bill_day.month != 12:
                bill_day = date(day.year, day.month + 1, self.bill_day)
            else:
                bill_day = date(day.year + 1, 1, self.bill_day)

        if self.card_type == _DUE_PERIOD_PAY:
            return bill_day + timedelta(days=self.due_period)
        if self.card_type == _DUE_DAY_PAY:
            if self.due_day > self.bill_day:
                return date(bill_day.year, bill_day.month, self.due_day)
            else:
                if bill_day.month != 12:
                    return date(bill_day.year, bill_day.month + 1, self.due_day)
                else:
                    return date(bill_day.year + 1, 1, self.due_day)


class Pos(models.Model):
    rate = models.FloatField(default=0.6)


class CashOut(BaseModel):
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    swipe_day = models.DateField(default=date.today, help_text='刷卡日')
    amount = models.DecimalField(max_digits=11, decimal_places=2, help_text='金额')
    pos_rate = models.FloatField('rate', default=0.6, help_text='刷卡费率')
    fee = models.DecimalField(max_digits=9, decimal_places=2, help_text='手续费')
    due_day = models.DateField() #到期日
    isRepaid = models.BooleanField(default=False)
    pay_day = models.DateField(null=True, blank=True) #实际还款日
    apr = models.FloatField(null=True, blank=True) #年利率


    def save(self, *args, **kwargs):
        if self.pk is None:
            self.fee = self.amount * Decimal(self.pos_rate) / 100
            self.due_day = self.card.find_next_due_day(self.swipe_day)

        super().save(*args, **kwargs)

