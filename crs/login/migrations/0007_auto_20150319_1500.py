# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_faculty_iswarden'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaptchaCaptchastore',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('challenge', models.CharField(max_length=32)),
                ('response', models.CharField(max_length=32)),
                ('hashkey', models.CharField(unique=True, max_length=40)),
                ('expiration', models.DateTimeField()),
            ],
            options={
                'db_table': 'captcha_captchastore',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Complainid',
            fields=[
                ('sno', models.IntegerField(serialize=False, primary_key=True)),
                ('hostel', models.IntegerField()),
                ('type', models.IntegerField()),
                ('date', models.DateField()),
                ('id', models.IntegerField(db_column='ID')),
            ],
            options={
                'db_table': 'complainID',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fooditems',
            fields=[
                ('fid', models.IntegerField(serialize=False, primary_key=True, db_column='FID')),
                ('name', models.CharField(unique=True, max_length=100)),
                ('vitamins', models.IntegerField()),
                ('proteins', models.IntegerField()),
                ('fat', models.IntegerField()),
                ('nutritions', models.DecimalField(max_digits=10, decimal_places=3)),
            ],
            options={
                'db_table': 'foodItems',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meals',
            fields=[
                ('mid', models.IntegerField(serialize=False, primary_key=True, db_column='MID')),
                ('items', models.CharField(unique=True, max_length=100)),
                ('avgnutrition', models.DecimalField(decimal_places=0, max_digits=10, db_column='avgNutrition')),
            ],
            options={
                'db_table': 'meals',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to='documents/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='faculty',
            options={'managed': False},
        ),
    ]
