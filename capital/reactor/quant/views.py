from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from datetime import timedelta
from json import dumps

from .models import DailyStats


def echarts_test(request):
    return render(request, 'test.html', locals())

def echarts_test2(request):
    return render(request, 'test2.html', locals())


def fetch_median_close(request):
	ds = DailyStats.objects.all()
	data = []
	for d in ds:
		data.append([d.date.strftime("%Y-%m-%d"), float(d.median_close)])
	return HttpResponse(dumps(data), "text/json")