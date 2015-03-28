# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0018_auto_20150323_1320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clink',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='studcomplainlink',
            options={},
        ),
    ]
