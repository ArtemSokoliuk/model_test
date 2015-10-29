# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='archive',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='article',
            name='favourite',
            field=models.NullBooleanField(),
        ),
    ]
