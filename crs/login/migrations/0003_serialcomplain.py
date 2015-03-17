# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20150315_0720'),
    ]

    operations = [
        migrations.CreateModel(
            name='serialComplain',
            fields=[
                ('cid', models.IntegerField(serialize=False, primary_key=True)),
                ('uid', models.IntegerField(db_column='UID')),
                ('time', models.DateTimeField()),
                ('hostel', models.IntegerField()),
                ('type', models.IntegerField()),
                ('subject', models.TextField()),
                ('detail', models.TextField()),
                ('history', models.TextField()),
                ('comments', models.IntegerField()),
                ('serial', models.IntegerField()),
                ('studID', models.IntegerField()),
            ],
            options={
                'db_table': 'complain',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
