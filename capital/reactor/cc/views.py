from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date
from datetime import timedelta

from .models import CreditCard
from .models import CashOut


def card_list(request):
    cards = CreditCard.objects.all()
    total = cards.count()
    paginator = Paginator(cards, 20)
    page = request.GET.get('page')
    try:
        card_list = paginator.get_page(page)
    except PageNotAnInteger:
        card_list = paginator.get_page(1)
    except EmptyPage:
        card_list = paginator.get_page(paginator.num_pages)
    return render(request, 'card.html', locals())

def swipe_card(request, card_id):
    pass

def calendar(request):
    now = date.today()
    _b = date(now.year, now.month, 1)
    _e = _b + timedelta(31)
    cashOut_list = CashOut.objects.filter(due_day__gt=_b, due_day__lt=_e)

    return render(request, 'calendar.html', locals())
