# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smooth_perms.validators


class Migration(migrations.Migration):

    dependencies = [
        ('smooth_perms', '0004_smoothregistrymodel_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='permissionadminmixin',
            name='exclude_fields',
            field=models.CharField(max_length=1000, validators=[smooth_perms.validators.validate_tab], default='citizen'),
            preserve_default=False,
        ),
    ]
