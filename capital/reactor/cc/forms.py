#coding=utf-8
from django import forms
from django.forms import ValidationError

from .models import CashOut


class CashPayForm(forms.Form):
    amount = forms.DecimalField(label=u'金额')
    due_day = forms.DateField(label=u'到期日')
    pay_day = forms.DateField(label=u'还款日', required=True, widget=forms.SelectDateWidget())

    def __init__(self,*args,**kwargs):
        super(CashPayForm, self).__init__(*args, **kwargs)

        co_id = self.initial.get('co_id')
        if cid:
            self.co = CashOut.objects.filter(pk=co_id).first()
            if self.co:
                self.fields['amount'].initial = self.co.amount
                self.fields['amount'].widget.attrs['readonly'] = True
                self.fields['due_day'].initial = self.co.due_day
                self.fields['due_day'].widget.attrs['readonly'] = True
        else:
            self.case = None

    def save(self):
        pass
        #data = self.cleaned_data
        #if self.case:
        #    self.case.name = data['name']
        #    self.case.cp = data['cp']
        #    self.case.save()
        #else:
        #    case = Case(name=data['name'], cp=data['cp'])
        #    case.save()

