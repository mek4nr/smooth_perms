from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.conf import settings


class SmoothGroup(Group):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_usersmoothgroups")

    class Meta:
        verbose_name = _(u'User group (SmoothPerm)')
        verbose_name_plural = _(u'User groups (SmoothPerm)')
        app_label = 'smooth_perms'

