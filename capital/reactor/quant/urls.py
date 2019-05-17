from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('test/', views.echarts_test, name='echarts_test'),
    path('test2/', views.echarts_test2, name='echarts_test2'),
    path('mc/', views.fetch_median_close, name='fetch_median_close'),
]
