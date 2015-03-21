# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20150320_1320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'managed': True},
        ),
    ]
