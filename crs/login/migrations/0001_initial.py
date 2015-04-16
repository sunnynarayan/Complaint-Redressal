# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentid', models.IntegerField(serialize=False, primary_key=True, db_column='commentId')),
                ('cid', models.CharField(max_length=19, db_column='cid')),
                ('name', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'comment',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('cid', models.CharField(max_length=19, serialize=False, primary_key=True)),
                ('uid', models.IntegerField(db_column='UID')),
                ('time', models.DateTimeField()),
                ('hostel', models.IntegerField(db_column='hostel')),
                ('type', models.IntegerField()),
                ('subject', models.TextField()),
                ('detail', models.TextField()),
                ('history', models.TextField()),
                ('comments', models.IntegerField()),
                ('status', models.IntegerField(null=True, blank=True)),
                ('picid', models.CharField(max_length=100, db_column='picID')),
            ],
            options={
                'db_table': 'complain',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Complainid',
            fields=[
                ('sno', models.IntegerField(serialize=False, primary_key=True)),
                ('hostel', models.IntegerField(db_column='hostel')),
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
            name='Complainlink',
            fields=[
                ('cid', models.CharField(max_length=19, serialize=False, primary_key=True, db_column='CID')),
                ('studid', models.IntegerField(null=True, db_column='studID', blank=True)),
                ('secid', models.IntegerField(null=True, db_column='secID', blank=True)),
                ('woid', models.IntegerField(null=True, db_column='woID', blank=True)),
                ('wardenid', models.IntegerField(null=True, db_column='wardenID', blank=True)),
            ],
            options={
                'db_table': 'complainLink',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('docfile', models.ImageField(upload_to='documents/%Y/%m/%d')),
                ('cid', models.CharField(max_length=19, db_column='cid')),
            ],
            options={
                'db_table': 'document',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('fid', models.IntegerField(serialize=False, primary_key=True, db_column='FID')),
                ('name', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=1)),
                ('mobile', models.CharField(max_length=10)),
                ('off_ph', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=128)),
                ('key_value', models.CharField(max_length=4)),
                ('email', models.CharField(max_length=50)),
                ('iswarden', models.IntegerField(db_column='isWarden')),
            ],
            options={
                'db_table': 'faculty',
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
                ('nutritions', models.FloatField()),
            ],
            options={
                'db_table': 'foodItems',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'hostel',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HostelLeavingInformation',
            fields=[
                ('sno', models.IntegerField(serialize=False, primary_key=True)),
                ('studid', models.IntegerField(db_column='studid')),
                ('start_date', models.DateTimeField(db_column='start_Date')),
                ('end_date', models.DateTimeField(db_column='end_Date')),
                ('destination', models.CharField(max_length=1000)),
                ('reason', models.TextField()),
                ('hostel', models.IntegerField(db_column='hostel')),
                ('mobile', models.TextField()),
                ('time', models.CharField(max_length=8)),
                ('status', models.IntegerField()),
                ('submittime', models.TimeField(db_column='submitTime')),
            ],
            options={
                'db_table': 'hostel_leaving_information',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mealitems',
            fields=[
                ('sno', models.IntegerField(serialize=False, primary_key=True)),
                ('mid', models.IntegerField(db_column='MID')),
                ('fid', models.IntegerField(db_column='FID')),
            ],
            options={
                'db_table': 'mealItems',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meals',
            fields=[
                ('mid', models.IntegerField(serialize=False, primary_key=True, db_column='MID')),
                ('items', models.IntegerField()),
                ('fid', models.CharField(unique=True, max_length=100, db_column='FID')),
            ],
            options={
                'db_table': 'meals',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pollmenu',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('meal', models.TextField()),
                ('hostel', models.IntegerField(db_column='hostel')),
                ('type', models.IntegerField()),
                ('protein', models.IntegerField()),
                ('vitamin', models.IntegerField()),
                ('fat', models.IntegerField()),
                ('nutritions', models.DecimalField(max_digits=4, decimal_places=2)),
            ],
            options={
                'db_table': 'pollMenu',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pollresult',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('hostel', models.IntegerField()),
                ('type', models.IntegerField()),
                ('meal', models.IntegerField()),
                ('vote', models.IntegerField()),
                ('protein', models.IntegerField()),
                ('vitamin', models.IntegerField()),
                ('fat', models.IntegerField()),
                ('nutritions', models.DecimalField(max_digits=4, decimal_places=2)),
            ],
            options={
                'db_table': 'pollResult',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pollvoting',
            fields=[
                ('idx', models.IntegerField(serialize=False, primary_key=True)),
                ('id', models.IntegerField(db_column='id')),
                ('uid', models.IntegerField(db_column='UID')),
            ],
            options={
                'db_table': 'pollVoting',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Secretary',
            fields=[
                ('uid', models.IntegerField(serialize=False, primary_key=True, db_column='UID')),
                ('type', models.IntegerField()),
                ('hostel', models.IntegerField(db_column='hostel')),
                ('rating', models.DecimalField(max_digits=4, decimal_places=2)),
            ],
            options={
                'db_table': 'secretary',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Secretaryrating',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('secid', models.IntegerField(db_column='secID')),
                ('studid', models.IntegerField(db_column='studID')),
                ('rating', models.IntegerField()),
            ],
            options={
                'db_table': 'secretaryRating',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Studcomplainlink',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('cid', models.CharField(max_length=19, db_column='cid')),
                ('studid', models.IntegerField(db_column='studid')),
            ],
            options={
                'db_table': 'studComplainlink',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('uid', models.IntegerField(serialize=False, primary_key=True, db_column='UID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=128, blank=True)),
                ('key_value', models.CharField(max_length=128, blank=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('sex', models.CharField(max_length=1, blank=True)),
                ('padd', models.TextField(blank=True)),
                ('mobile', models.CharField(max_length=10, blank=True)),
                ('email', models.CharField(max_length=50, blank=True)),
                ('roll', models.CharField(max_length=8, blank=True)),
                ('room', models.IntegerField(null=True, blank=True)),
                ('hostel', models.IntegerField(null=True, db_column='hostel', blank=True)),
                ('bloodgrp', models.CharField(max_length=3, db_column='bloodGrp', blank=True)),
                ('baccno', models.IntegerField(db_column='bAccNo')),
                ('bank', models.CharField(max_length=50, blank=True)),
                ('ifsc', models.CharField(max_length=11, db_column='IFSC', blank=True)),
                ('issec', models.IntegerField(db_column='isSec')),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'student',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Warden',
            fields=[
                ('fid', models.IntegerField(serialize=False, primary_key=True, db_column='FID')),
                ('hostel', models.IntegerField(db_column='hostel')),
            ],
            options={
                'db_table': 'warden',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
