# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_auto_20150321_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Secretaryrating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('secid', models.IntegerField(db_column='secID')),
                ('studid', models.IntegerField(db_column='studID')),
                ('rating', models.IntegerField()),
            ],
            options={
                'db_table': 'secretaryRating',
                'managed': True,
            },
            bases=(models.Model,),
        ),
    ]
