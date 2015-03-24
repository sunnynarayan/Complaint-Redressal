# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0014_auto_20150323_1224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='djangocontenttype',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='secretaryrating',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='studcomplainlink',
            options={'managed': False},
        ),
    ]
