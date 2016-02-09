# -*- coding: utf-8 -*-
"""
..module:models.registry
    :project: smooth_perms
    :platform: Unix
    :synopsis: Module for registry models, created on 04/02/2016

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>

"""
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.contenttypes.models import ContentType
from smooth_perms.validators import validate_tab
from django.utils.translation import ugettext_lazy as _
import logging

LOG = logging.getLogger("LOG")

def get_fields_from_obj(model, is_inline=False):
    opts = model._meta
    fields_init = list(
        [field for field in opts.local_fields] +
        [field for field in opts.local_many_to_many]
    )

    fields = []
    for field in fields_init:
        if field.name in ("id", "created_at", "modified_at", "owner", "created_by"):
            continue
        elif isinstance(field, ForeignKey) and is_inline:
            continue
        fields.append(field)
    return fields


class SmoothRegistryModel(models.Model):
    """
    Model definition for each model who is register in smooth_registry
    """
    name = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType)

    def __str__(self):
        return "{}" . format(self.name)

    def __unicode__(self):
        return self.__str__()

    def get_choices_from_fields(self):
        """
        Get fields of object given. Remove Foreign key in list. and id, created_by, owner, modified_at
        :param obj: ModelObject
        :return: choices list of (field, verbose_name)
        """
        choices = list()
        for field in get_fields_from_obj(self.content_type.model_class()):
            choices += [[field.name, field.verbose_name]]
        return choices


class PermissionAdminMixin(models.Model):
    """
    Model definition for define exclude/readonly fields for each perm
    """
    smooth_registry = models.ForeignKey(SmoothRegistryModel, related_name="registry")

    perm = models.CharField(max_length=1000)
    trolo = models.PositiveIntegerField(default=0)
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
