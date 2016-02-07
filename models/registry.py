from django.db import models
from django.contrib.contenttypes.models import ContentType
from smooth_perms.validators import validate_tab
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
import logging

LOG = logging.getLogger("LOG")


class SmoothRegistryModel(models.Model):
    name = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType)

    def __str__(self):
        return "{}" . format(self.name)

    def __unicode__(self):
        return self.__str__()

    def get_fields_from_content_type(self):
        """
        Get fields of object given. Remove Foreign key in list. and id, created_by, owner, modified_at
        :param obj: ModelObject
        :return: choices list of (field, verbose_name)
        """
        choices = list()
        obj = self.content_type.model_class()
        fields = obj._meta.concrete_fields
        try:
            fields_admin = admin._registry[type(obj)].get_fields(self.request, obj)
            read_only_admin = admin._registry[type(obj)].get_readonly_fields(self.request, obj)
        except (AttributeError, KeyError, NameError):
            fields_admin = [field.name for field in fields]
            read_only_admin = []

        for field in fields:
            if field.name in ("id", "created_at", "modified_at", "owner", "created_by"):
                continue
            if isinstance(field, ForeignKey):
                continue
            if field.name in fields_admin and field.name not in read_only_admin:
                choices += [[field.name, field.verbose_name]]
        return choices


class PermissionAdminMixin(models.Model):
    smooth_registry = models.ForeignKey(SmoothRegistryModel, related_name="registry")

    perm = models.CharField(max_length=1000)
    fields = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        default="[]",
        validators=[validate_tab],
        help_text=_("This fields will be in read-only if user doens't have permission given")
    )
    exclude_fields = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        default="[]",
        validators=[validate_tab],
        help_text=_("This fields will be exclude if user doens't have permission given")
    )

    def __str__(self):
        return "{} permission" . format(self.perm)

    def __unicode__(self):
        return self.__str__()
