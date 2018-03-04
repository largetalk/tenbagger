from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from datetime import date
from datetime import timedelta
from json import dumps

from .models import CreditCard
from .models import CashOut
from .forms import CashPayForm


@login_required
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
    _e = _b + timedelta(61)
    cashOut_list = CashOut.objects.filter(isRepaid=False, due_day__gt=_b, due_day__lt=_e)

    return render(request, 'calendar.html', locals())

def stats(request):
    cards = CreditCard.objects.all()
    stats_list = []
    total_swipe_count = 0
    total_unpay_count = 0
    total_unpay_amount = 0
    total_available_line = 0
    overdue = False
    for card in cards:
        info = card.stats
        stats_list.append(info)
        total_swipe_count += info['swipe_count']
        total_unpay_count +=  info['unpay_count']
        total_unpay_amount += info['unpay_amount']
        total_available_line += info['available_line']
        if info['overdue']:
            overdue = True

    return render(request, 'stats.html', locals())

@login_required
def card_co(request, card_id):
    card = CreditCard.objects.get(pk=card_id)
    co_list = CashOut.objects.filter(card=card, isRepaid=False)
    
    return render(request, 'card_co.html', locals())

@login_required
def cash_pay(request, co_id):
    form = CashPayForm(request.POST or None,initial={'co_id':co_id or None})
    if request.method == "POST":
        if form.is_valid():
            form.save()
        return HttpResponse(dumps({'status':0}), "text/application")
    return render(request, 'cash_pay_form.tpl', {'form': form})
