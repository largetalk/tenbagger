from django.contrib import admin

from .models import CreditCard
from .models import Pos
from .models import CashOut


class CreditCardAdmin(admin.ModelAdmin):
        list_display = ('name', 'tail_no', 'bill_day', 'card_type', 'due_day', 'due_period')

class PosAdmin(admin.ModelAdmin):
        fields = ['rate']
        list_display = ('id', 'rate')

class CashOutAdmin(admin.ModelAdmin):
        list_display = ('card', 'swipe_day', 'amount', 'due_day', 'isRepaid')

admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Pos, PosAdmin)
admin.site.register(CashOut, CashOutAdmin)
