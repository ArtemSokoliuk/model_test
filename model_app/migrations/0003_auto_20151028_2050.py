# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model_app', '0002_auto_20151028_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='favourite',
            field=models.BooleanField(default=False),
        ),
    ]
