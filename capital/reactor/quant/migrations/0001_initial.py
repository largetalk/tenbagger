# Generated by Django 2.0.2 on 2019-04-29 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyStats',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('median_close', models.FloatField(default=0)),
            ],
        ),
    ]


## copy data from avgp
# insert into quant_dailystats(date, median_close) select date, median_close from avgp.daily_stats;