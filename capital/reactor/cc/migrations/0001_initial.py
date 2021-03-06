# Generated by Django 2.0.2 on 2018-02-24 03:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ct', models.DateTimeField(auto_now_add=True)),
                ('ut', models.DateTimeField(auto_now=True)),
                ('swipe_day', models.DateField(default=datetime.date.today)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('pos_rate', models.FloatField(default=0.6)),
                ('fee', models.DecimalField(decimal_places=2, max_digits=9)),
                ('due_day', models.DateField()),
                ('isRepaid', models.BooleanField(default=False)),
                ('pay_day', models.DateField()),
                ('apr', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ct', models.DateTimeField(auto_now_add=True)),
                ('ut', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('tail_no', models.IntegerField()),
                ('bill_day', models.PositiveSmallIntegerField()),
                ('card_type', models.CharField(choices=[('A', 'A'), ('B', 'B')], default='A', max_length=5)),
                ('due_day', models.PositiveSmallIntegerField(null=True)),
                ('due_period', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(default=0.6)),
            ],
        ),
        migrations.AddField(
            model_name='cashout',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cc.CreditCard'),
        ),
    ]
