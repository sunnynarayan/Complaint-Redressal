# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20150318_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='iswarden',
            field=models.IntegerField(default=1, db_column='isWarden'),
            preserve_default=False,
        ),
    ]
