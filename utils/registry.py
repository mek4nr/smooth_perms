# -*- coding: utf-8 -*-
"""
..module:signals.registry
    :project: smooth_perms
    :platform: Unix
    :synopsis: Utils for set/get current user without using request, created on 04/02/2016. Take from django_cms

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>

"""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_permission_codename
from copy import deepcopy
from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured
from django.contrib.admin.sites import AlreadyRegistered, NotRegistered
from django.utils.translation import ugettext as _
from django import forms
from smooth_perms.models import SmoothRegistryModel, BASE_PERMISSIONS, PermissionAdminMixin


def get_registry(model):
    """
    Get registry from database with model
    """
    return SmoothRegistryModel.objects.get(content_type=ContentType.objects.get_for_model(model))


def get_registry_perms(model):
    """
    Get all permission mixin from model
    """
    return get_registry(model).registry.all()


class SmoothPermRegister(object):
    """
    Class definition for register all model with permission, generated fieldsets for smooth_group
    get initial data in this fieldsets
    """
    registry = []

    def get_codename(self, model, perm):
        """
        Return codename permission using model & name of perm (add, delete, change)
        """
        return get_permission_codename(perm, model._meta)

    def get_fields_form(self, fields=None):
        """
        Create automatically fields for group admin form
        Not Used because impossible to call __init__ on ModelForm
        :param fields:
        :return:
        """
        fields = fields or {}
        for model, text in self.registry:
            for t in ('add', 'change', 'delete'):
                # add permission `t` to model `model`
                fields['can_{}' . format(self.get_codename(model, t))] = forms.BooleanField(label=_(t.title()), required=False)
        return fields

    def get_initials(self, obj):
        """
        Read out permissions from permission system.
        """
        initials = {}
        permission_accessor = getattr(obj, 'permissions')

        for model, text in self.registry:
            name = model.__name__.lower()
            content_type = ContentType.objects.get_for_model(model)
            permissions = permission_accessor.filter(content_type=content_type).values_list('codename', flat=True)
            for t in ('add', 'change', 'delete'):
                codename = self.get_codename(model, t)
                initials['can_{}_{}'  .format(t, name)] = codename in permissions
        return initials

    def save_permissions(self, data, obj):
        """
        Save permission from data
        """
        if not obj.pk:
            # save obj, otherwise we can't assign permissions to him
            obj.save()
        permission_acessor = getattr(obj, 'permissions')
        for model, text in self.registry:
            content_type = ContentType.objects.get_for_model(model)
            for t in ('add', 'change', 'delete'):
                # add permission `t` to model `model`
                codename = self.get_codename(model, t)
                permission = Permission.objects.get(content_type=content_type, codename=codename)
                if data.get('can_{}' . format(codename), None):
                    permission_acessor.add(permission)
                else:
                    permission_acessor.remove(permission)

    def register(self, model, text=None):
        """
        Add a model in registry
        """
        if not isinstance(model, ModelBase):
            raise ImproperlyConfigured('This object {} is not a ModelBase class' . format(model.__name__))

        for m, t in self.registry:
            if m == model:
                raise AlreadyRegistered('The model {} is already registered' . format(model.__name__))

        if text is None:
            text = _(u'{} permissions') .format(model.__name__)

        try:
            registry_model = SmoothRegistryModel.objects.get_or_create(
                name="{} registry" . format(model.__name__),
                content_type=ContentType.objects.get_for_model(model)
            )

            for perm in BASE_PERMISSIONS:
                PermissionAdminMixin.objects.get_or_create(perm=perm, smooth_registry=registry_model[0])
            for perm in model.permissions.PERMISSIONS:
                PermissionAdminMixin.objects.get_or_create(perm=perm, smooth_registry=registry_model[0])
        except Exception:
            pass

        self.registry.append((model, _(text)))

    def unregister(self, model):
        """
        Remove model from registry
        """
        for i, perm_model in enumerate(self.registry):
            _model, _text = perm_model
            if model == _model:
                SmoothRegistryModel.objects.get(
                    content_type=ContentType.objects.get_for_model(model)
                ).delete()
                self.registry.remove(i)
                return True
        raise NotRegistered('The model {} is not registered' . format(model.__name__))

    def update_permission_fieldsets(self, request, fieldsets):
        """
        Nobody can grant more than he haves, so check for user permissions
        to Page and User model and render fieldsets depending on them.
        """
        fieldsets = deepcopy(fieldsets)

        for i, perm_model in enumerate(self.registry):
            model, title = perm_model
            opts, fields = model._meta, []
            name = model.__name__.lower()

            for t in ('add', 'change', 'delete'):
                if request.user.has_perm('{}.{}_{}' .format(opts.app_label, t, name)):
                    fields.append('can_{}_{}' . format(t, name))
            if fields:
                fieldsets.insert(2 + i, (title, {'fields': (fields,)}))
        return fieldsets


smooth_registry = SmoothPermRegister()
