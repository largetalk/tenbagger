from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('test/', views.echarts_test, name='echarts_test'),
    path('mc/', views.fetch_median_close, name='fetch_median_close'),
]
