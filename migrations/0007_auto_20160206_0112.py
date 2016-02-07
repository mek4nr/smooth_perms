# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smooth_perms.validators


class Migration(migrations.Migration):

    dependencies = [
        ('smooth_perms', '0006_auto_20160205_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissionadminmixin',
            name='exclude_fields',
            field=models.CharField(default='[]', help_text="This fields will be exclude if user doens't have permission given", blank=True, validators=[smooth_perms.validators.validate_tab], null=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='permissionadminmixin',
            name='fields',
            field=models.CharField(default='[]', help_text="This fields will be in read-only if user doens't have permission given", blank=True, validators=[smooth_perms.validators.validate_tab], null=True, max_length=1000),
        ),
    ]
