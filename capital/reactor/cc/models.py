#coding:utf-8
from django.db import models
from utils.bm import BaseModel
from datetime import date


_CARD_TYPE_CHOICES = (('A', 'A'), ('B', 'B'))
class CreditCard(BaseModel):
    name = models.CharField(max_length=100)
    tail_no = models.IntegerField()
    bill_day = models.PositiveSmallIntegerField()
    card_type = models.CharField(max_length = 5, choices=_CARD_TYPE_CHOICES, default='A')
    due_day = models.PositiveSmallIntegerField(null=True)
    due_period = models.PositiveSmallIntegerField(null=True)


class Pos(models.Model):
    rate = models.FloatField(default=0.6)


class CashOut(BaseModel):
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    swipe_day = models.DateField(default=date.today)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    pos_rate = models.FloatField(default=0.6)
    fee = models.DecimalField(max_digits=9, decimal_places=2)
    due_day = models.DateField() #到期日
    isRepaid = models.BooleanField(default=False)
    pay_day = models.DateField() #实际还款日
    apr = models.FloatField() #年利率

