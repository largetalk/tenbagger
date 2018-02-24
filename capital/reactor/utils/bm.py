#coding:utf-8
from django.db import models
import datetime

class BaseModel(models.Model):
    ct = models.DateTimeField(auto_now_add=True)
    ut = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
