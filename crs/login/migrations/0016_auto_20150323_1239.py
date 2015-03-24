# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_auto_20150323_1238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='djangocontenttype',
            options={},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='secretaryrating',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='studcomplainlink',
            options={},
        ),
    ]
