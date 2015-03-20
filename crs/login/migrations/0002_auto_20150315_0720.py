# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authgroup',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='authgrouppermissions',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='authpermission',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='authuser',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='authusergroups',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='authuseruserpermissions',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='clink',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='com',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='complain',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='complainlink',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='djangoadminlog',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='djangomigrations',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='djangosession',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='faculty',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='hostel',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='pollque',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='pollres',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='secretary',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='warden',
            options={'managed': False},
        ),
    ]
