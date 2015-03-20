# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20150315_0720'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostelLeavingInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.IntegerField()),
                ('start_date', models.CharField(max_length=6, db_column='start_Date')),
                ('end_date', models.CharField(max_length=6, db_column='end_Date')),
                ('laptop', models.CharField(max_length=3)),
                ('destination', models.CharField(max_length=30)),
                ('reason', models.TextField()),
                ('hostel', models.IntegerField()),
                ('roll', models.CharField(max_length=8)),
                ('mobile', models.IntegerField()),
            ],
            options={
                'db_table': 'hostel_leaving_information',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
