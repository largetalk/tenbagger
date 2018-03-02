#coding=utf-8
from django import forms
from django.forms import ValidationError
from datetime import date

from .models import CashOut


class CashPayForm(forms.Form):
    amount = forms.DecimalField(label=u'金额')
    due_day = forms.DateField(label=u'到期日')
    pay_day = forms.DateField(label=u'还款日', required=True)

    def __init__(self,*args,**kwargs):
        super(CashPayForm, self).__init__(*args, **kwargs)

        co_id = self.initial.get('co_id')
        if co_id:
            self.co = CashOut.objects.filter(pk=co_id).first()
            if self.co:
                self.fields['amount'].initial = self.co.amount
                self.fields['amount'].widget.attrs['readonly'] = True
                self.fields['due_day'].initial = self.co.due_day
                self.fields['due_day'].widget.attrs['readonly'] = True
                self.fields['pay_day'].initial = date.today()
        else:
            self.co = None

    def save(self):
        if self.co:
            data = self.cleaned_data
            self.co.pay_day = data['pay_day']
            delta = self.co.pay_day - self.co.swipe_day
            if delta.days > 2:
                self.co.apr = (self.co.fee * 365 * 100) / (delta.days - 2) / self.co.amount
            else:
                self.co.apr = 1000
            self.co.save()

