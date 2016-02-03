# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smooth_perms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='smoothgroup',
            name='created_by',
            field=models.ForeignKey(related_name='created_usersmoothgroups', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
