# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smooth_perms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='smoothregistrymodel',
            name='is_register',
            field=models.BooleanField(default=True),
        ),
    ]
