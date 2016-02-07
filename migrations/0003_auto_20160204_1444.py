# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smooth_perms.validators


class Migration(migrations.Migration):

    dependencies = [
        ('smooth_perms', '0002_smoothgroup_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionAdminMixin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('perm', models.CharField(max_length=1000)),
                ('fields', models.CharField(max_length=1000, validators=[smooth_perms.validators.validate_tab])),
            ],
        ),
        migrations.CreateModel(
            name='SmoothRegistryModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='permissionadminmixin',
            name='smooth_registry',
            field=models.ForeignKey(related_name='registry', to='smooth_perms.SmoothRegistryModel'),
        ),
    ]
