from django.contrib import admin

from .models import CreditCard
from .models import Pos
from .models import CashOut
from .models import Loans
from .models import Installment
from .models import Staging


class CreditCardAdmin(admin.ModelAdmin):
        list_display = ('name', 'tail_no', 'lines', 'bill_day', 'card_type', 'due_day', 'due_period')

class PosAdmin(admin.ModelAdmin):
        fields = ['rate']
        list_display = ('id', 'rate')

class CashOutAdmin(admin.ModelAdmin):
        fields = ['card', 'swipe_day', 'amount', 'pos_rate', 'isRepaid']
        list_display = ('card', 'swipe_day', 'amount', 'fee', 'due_day', 'isRepaid', 'pay_day', 'apr')

class LoansAdmin(admin.ModelAdmin):
        fields = ['bank', 'loan_day', 'amount', 'loan_type', 'due_day', 'debit_day', 'apr']
        list_display = ('bank', 'loan_day', 'amount', 'loan_type', 'due_day', 'debit_day', 'apr')

class InstallmentAdmin(admin.ModelAdmin):
        fields = ['cashOut', 'loan', 'amount', 'stage_count', 'charge_rate', 'lend_rate', 'first_repay_day']
        list_display = ('name', 'amount', 'stage_count', 'rate', 'first_repay_day', 'balance')

class StagingAdmin(admin.ModelAdmin):
        fields = ['no']
        list_display = ('installment', 'no', 'pay_amount', 'pay_day', 'isRepaid')

admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Pos, PosAdmin)
admin.site.register(CashOut, CashOutAdmin)
admin.site.register(Loans, LoansAdmin)
admin.site.register(Installment, InstallmentAdmin)
admin.site.register(Staging, StagingAdmin)
