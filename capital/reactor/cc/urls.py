"""reactor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('card/', views.card_list, name='card_list'),
    #path('swipe/<int:card_id>/', views.swipe_card, name='swipe_card'),
    path('calendar/', views.calendar, name='calendar'),
    path('stats/', views.stats, name='stats'),
    path('loans/', views.loans, name='loans'),
    path('co/<int:card_id>/', views.card_co, name='card_co'),
    path('co/pay/<int:co_id>/', views.cash_pay, name='cash_pay'),
    path('co/installment/<int:co_id>/', views.cash_installment, name='cash_installment'),
    path('installment/', views.installment, name='installment'),
    path('staging/<int:installment_id>/', views.ins_staging, name='ins_staging'),
    path('staging/repay/<int:staging_id>/', views.staging_repay, name='staging_repay'),
]
