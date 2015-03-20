# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
            ],
            options={
                'db_table': 'auth_group',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('group', models.ForeignKey(to='login.AuthGroup')),
            ],
            options={
                'db_table': 'auth_group_permissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField()),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(unique=True, max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=75)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('group', models.ForeignKey(to='login.AuthGroup')),
                ('user', models.ForeignKey(to='login.AuthUser')),
            ],
            options={
                'db_table': 'auth_user_groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('permission', models.ForeignKey(to='login.AuthPermission')),
                ('user', models.ForeignKey(to='login.AuthUser')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Clink',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('cid', models.IntegerField(db_column='CID')),
                ('comid', models.IntegerField(db_column='ComID')),
                ('uid', models.IntegerField(db_column='UID')),
                ('time', models.DateTimeField()),
            ],
            options={
                'db_table': 'Clink',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Com',
            fields=[
                ('comid', models.IntegerField(serialize=False, primary_key=True, db_column='comID')),
                ('txt', models.TextField(db_column='Txt')),
            ],
            options={
                'db_table': 'Com',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Complain',
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
            ],
            options={
                'db_table': 'complain',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Complainlink',
            fields=[
                ('cid', models.IntegerField(serialize=False, primary_key=True, db_column='CID')),
                ('studid', models.IntegerField(null=True, db_column='studID', blank=True)),
                ('secid', models.IntegerField(null=True, db_column='secID', blank=True)),
                ('woid', models.IntegerField(null=True, db_column='woID', blank=True)),
                ('wardenid', models.IntegerField(null=True, db_column='wardenID', blank=True)),
            ],
            options={
                'db_table': 'complainLink',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.IntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
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
            ],
            options={
                'db_table': 'faculty',
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
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pollque',
            fields=[
                ('pollid', models.IntegerField(serialize=False, primary_key=True, db_column='PollID')),
                ('uid', models.IntegerField(db_column='UID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('ques', models.TextField()),
                ('choice', models.TextField()),
                ('choino', models.IntegerField(db_column='choiNo')),
            ],
            options={
                'db_table': 'PollQue',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pollres',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('pollid', models.IntegerField(db_column='PollID')),
                ('uid', models.IntegerField(db_column='UID')),
                ('votetime', models.DateTimeField(db_column='voteTime')),
                ('choice', models.IntegerField()),
            ],
            options={
                'db_table': 'PollRes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Secretary',
            fields=[
                ('uid', models.IntegerField(serialize=False, primary_key=True, db_column='UID')),
                ('type', models.IntegerField()),
                ('hostel', models.IntegerField()),
            ],
            options={
                'db_table': 'secretary',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('uid', models.IntegerField(serialize=False, primary_key=True, db_column='UID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=128, blank=True)),
                ('key_value', models.CharField(max_length=128, blank=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('sex', models.CharField(max_length=1, blank=True)),
                ('padd', models.TextField(blank=True)),
                ('mobile', models.CharField(max_length=10, blank=True)),
                ('email', models.CharField(max_length=50, blank=True)),
                ('roll', models.CharField(max_length=8, blank=True)),
                ('room', models.IntegerField(null=True, blank=True)),
                ('hostel', models.IntegerField(null=True, blank=True)),
                ('bloodgrp', models.CharField(max_length=3, db_column='bloodGrp', blank=True)),
                ('baccno', models.IntegerField(null=True, db_column='bAccNo', blank=True)),
                ('bank', models.CharField(max_length=50, blank=True)),
                ('ifsc', models.CharField(max_length=11, db_column='IFSC', blank=True)),
                ('issec', models.IntegerField(db_column='isSec')),
            ],
            options={
                'db_table': 'student',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Warden',
            fields=[
                ('fid', models.IntegerField(serialize=False, primary_key=True, db_column='FID')),
                ('hostel', models.IntegerField()),
            ],
            options={
                'db_table': 'warden',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='djangoadminlog',
            name='content_type',
            field=models.ForeignKey(blank=True, to='login.DjangoContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='djangoadminlog',
            name='user',
            field=models.ForeignKey(to='login.AuthUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='authpermission',
            name='content_type',
            field=models.ForeignKey(to='login.DjangoContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='authgrouppermissions',
            name='permission',
            field=models.ForeignKey(to='login.AuthPermission'),
            preserve_default=True,
        ),
    ]
