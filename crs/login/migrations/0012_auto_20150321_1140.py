# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_studcomplainlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studcomplainlink',
            name='cid',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
