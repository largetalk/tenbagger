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
    tail_no = models.CharField(max_length=10)
    lines = models.PositiveIntegerField(default=0, help_text="额度")
    bill_day = models.PositiveSmallIntegerField()
    card_type = models.CharField(max_length = 5, choices=_CARD_TYPE_CHOICES, default=_DUE_DAY_PAY)
    due_day = models.PositiveSmallIntegerField(null=True, blank=True)
    due_period = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return '%s(%s)' % (self.name, self.tail_no)

    @property
    def unpay_count(self):
        return CashOut.objects.filter(card=self, isRepaid=False).count()

    @property
    def total_fee(self):
        return sum([ x.fee for x in CashOut.objects.filter(card=self) ])

    @property
    def next_due_day(self):
        return self.find_next_due_day()

    @property
    def stats(self):
        co_list = CashOut.objects.filter(card=self, isRepaid=False).order_by("due_day")
        unpay_count = co_list.count()
        unpay_amount = sum([x.balance for x in co_list])
        oldest_day = None
        if unpay_count > 0:
            oldest_day = co_list[0].due_day
        now = date.today()
        overdue = any([ now > co.due_day for co in co_list])
        return {
            'swipe_count': CashOut.objects.filter(card=self).count(),
            'unpay_count': unpay_count,
            'unpay_amount': unpay_amount,
            'available_line': self.lines - unpay_amount,
            'oldest': oldest_day,
            'overdue': overdue,
            'name': str(self)
        }


    def find_next_due_day(self, day=date.today()):
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

    def __str__(self):
        return '%s/%s' % (self.amount, self.card)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.fee = self.amount * Decimal(self.pos_rate) / 100
            self.due_day = self.card.find_next_due_day(self.swipe_day)

        super().save(*args, **kwargs)

    @property
    def hasInstallment(self):
        if self.installment_set.count() > 0:
            return True
        return False

    @property
    def balance(self):
        installment = self.installment_set.first()
        if installment:
            return installment.balance
        return self.amount

_LOANS_TYPE = (('EPI', '等额本息'), ('EP', '等额本金'))
_LOANS_TYPE_DIC = dict(_LOANS_TYPE)
class Loans(BaseModel):
    bank = models.CharField(max_length=100)
    loan_day = models.DateField(default=date.today, help_text='借款日')
    amount = models.DecimalField(max_digits=11, decimal_places=2, help_text='金额')
    loan_type = models.CharField(max_length = 5, choices=_LOANS_TYPE, default='EPI')
    due_day = models.DateField(help_text='到期日')
    debit_day = models.PositiveSmallIntegerField(null=True, blank=True)
    apr = models.FloatField(null=True, blank=True) #年利率
    isRepaid = models.BooleanField(default=False)

    def __str__(self):
        return '%s(%s)' % (self.bank, self.amount)

    @property
    def loan_type_show(self):
        return _LOANS_TYPE_DIC[self.loan_type]

    @property
    def balance(self):
        installment = self.installment_set.first()
        if installment:
            return installment.balance
        return self.amount

class Installment(BaseModel):
    cashOut = models.ForeignKey(CashOut, models.SET_NULL, blank=True, null=True)
    loan = models.ForeignKey(Loans, models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2, help_text='金额')
    stage_count = models.PositiveSmallIntegerField(help_text="分期期数")
    charge_rate = models.FloatField(null=True, blank=True, default=0.35) #for cashOut
    lend_rate = models.FloatField(null=True, blank=True) #for loans
    first_repay_day = models.DateField(help_text="第一次还款日")
    balance = models.DecimalField(max_digits=11, decimal_places=2, help_text='余额')

    def __str__(self):
        if self.loan:
            return str(self.loan)
        if self.cashOut:
            return str(self.cashOut)
        return 'null'

    @property
    def next_repay_day(self):
        stagings = Staging.objects.filter(installment=self, isRepaid=False).order_by("pay_day")
        if len(stagings) > 0:
            return stagings[0].pay_day
        return None

    @property
    def name(self):
        if self.loan:
            return self.loan.bank
        if self.cashOut:
            return self.cashOut.card.name
        return 'null'

    @property
    def rate(self):
        if self.lend_rate:
            return self.lend_rate
        if self.charge_rate:
            return self.charge_rate
        return '100'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.balance = self.amount
        super().save(*args, **kwargs)

class Staging(BaseModel):
    installment = models.ForeignKey(Installment, on_delete=models.CASCADE)
    no = models.PositiveSmallIntegerField(help_text='第几期')
    principal = models.DecimalField(max_digits=11, decimal_places=2, help_text='本金')
    pay_amount = models.DecimalField(max_digits=11, decimal_places=2, help_text='金额')
    pay_day = models.DateField(help_text='还款日')
    isRepaid = models.BooleanField(default=False)

    def __str__(self):
        return '%s_%s(%s)' % (self.installment.name, self.pay_amount, self.no)

    def save(self, *args, **kwargs):
        if self.isRepaid and self.pk:
            orig = Staging.objects.get(pk=self.pk)
            if orig.isRepaid != self.isRepaid:
                self.installment.balance -= self.principal
                self.installment.save()
        super().save(*args, **kwargs)
