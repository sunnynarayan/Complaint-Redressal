# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0019_auto_20150323_1321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='secretary',
            options={'managed': True},
        ),
    ]
