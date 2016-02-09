# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smooth_perms.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionAdminMixin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('perm', models.CharField(max_length=1000)),
                ('trolo', models.PositiveIntegerField(default=0)),
                ('fields', models.CharField(default=b'[]', validators=[smooth_perms.validators.validate_tab], max_length=1000, blank=True, help_text="This fields will be in read-only if user doens't have permission given", null=True)),
                ('exclude_fields', models.CharField(default=b'[]', validators=[smooth_perms.validators.validate_tab], max_length=1000, blank=True, help_text="This fields will be exclude if user doens't have permission given", null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SmoothGroup',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Group')),
                ('created_by', models.ForeignKey(related_name='created_usersmoothgroups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User group (SmoothPerm)',
                'verbose_name_plural': 'User groups (SmoothPerm)',
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='SmoothRegistryModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.AddField(
            model_name='permissionadminmixin',
            name='smooth_registry',
            field=models.ForeignKey(related_name='registry', to='smooth_perms.SmoothRegistryModel'),
        ),
    ]
