# Generated by Django 2.0.2 on 2018-02-24 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashout',
            name='apr',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cashout',
            name='pay_day',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='card_type',
            field=models.CharField(choices=[('A', '指定还款日'), ('B', '定长还款期')], default='A', max_length=5),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='due_day',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='due_period',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
