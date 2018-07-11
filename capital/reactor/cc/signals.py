import math
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import date, timedelta
from .models import Installment
from .models import Staging

@receiver(post_save, sender=Installment)
def create_stagings(sender, instance, created, **kwargs):
    if not created:
        if instance.balance < 10:
            status = [ s[0] for s in instance.staging_set.values_list('isRepaid') ]
            if all(status):
                if instance.cashOut:
                    instance.cashOut.isRepaid = True
                    instance.cashOut.save()
                if instance.loan:
                    instance.loan.isRepaid = True
                    instance.loan.save()
        return
    amount = instance.amount
    count = instance.stage_count
    fDay = instance.first_repay_day
    principal = amount / count
    if instance.cashOut:
        pay_amount = float(amount / count) + (float(amount) * instance.charge_rate /100)
        for i in range(count):
            stags = Staging(installment=instance, no=i+1, principal=principal, pay_amount=pay_amount, pay_day=find_after_month_day(fDay, i))
            stags.save()
    elif instance.loan:
        m_rate = instance.lend_rate / 12 / 100
        p = math.pow(1 + m_rate, count)
        pay_amount = float(amount) * m_rate * p / (p -1)
        for i in range(count):
            stags = Staging(installment=instance, no=i+1, principal=principal, pay_amount=pay_amount, pay_day=find_after_month_day(fDay, i))
            stags.save()
    else:
        print('error: no cashOut and loan')

def find_after_month_day(cur, m):
    if m == 0:
        return cur
    newM = cur.month + m
    yAdd = int(newM / 12)
    while newM > 12:
        newM -= 12
    d = cur.day
    while True:
        try:
            return date(cur.year + yAdd, newM, d)
        except ValueError:
            d -= 1
