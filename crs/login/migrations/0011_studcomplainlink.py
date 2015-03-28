# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_auto_20150320_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Studcomplainlink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cid', models.CharField(max_length=19)),
                ('studid', models.IntegerField()),
            ],
            options={
                'db_table': 'studComplainlink',
                'managed': True,
            },
            bases=(models.Model,),
        ),
    ]
