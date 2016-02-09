# -*- coding: utf-8 -*-
"""
..module:admin.permissions
    :project: smooth_perms
    :platform: Unix
    :synopsis: modules definitions for registry models, created on 04/02/2016

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>
"""
from smooth_perms.models import SmoothRegistryModel, PermissionAdminMixin
from smooth_perms.forms import PermissionAdminMixinInlineForm
from django.contrib import admin


class PermissionAdminMixinInline(admin.TabularInline):
    """
    Class for PermissionMixinModel
    """
    model = PermissionAdminMixin
    extra = 0
    form = PermissionAdminMixinInlineForm
    fields = ["fields", "exclude_fields"]

    def has_add_permission(self, request):
        """
        They are generated automatically, so don't need to add more
        :return: False
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        They are generated automatically, so don't need to be destroy
        :return: False
        """
        return False


@admin.register(SmoothRegistryModel)
class SmoothRegistryAdmin(admin.ModelAdmin):
    """
    Admin for smooth registry model
    """
    readonly_fields = ["name", "content_type"]

    inlines = [PermissionAdminMixinInline]
    model = SmoothRegistryModel

    def has_add_permission(self, request):
        """
        They are generated automatically, so don't need to add more
        :return: False
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        They are generated automatically, so don't need to be destroy
        :return: False
        """
        return False
