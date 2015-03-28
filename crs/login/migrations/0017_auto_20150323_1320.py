# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_auto_20150323_1239'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studcomplainlink',
            options={'managed': False},
        ),
    ]
