# -*- coding: utf-8 -*-
"""
..module:admin.options
    :project: smooth_perms
    :platform: Unix
    :synopsis: module for all definition for model using smooth_perms. Defintion for Inline and ModelAdmin,
    created on 04/02/2016

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>
"""
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.admin.options import InlineModelAdmin
from copy import deepcopy
from smooth_perms.models import PermissionNotFoundException, get_fields_from_obj
from smooth_perms.utils.registry import get_registry_perms
from django.utils.translation import ugettext_lazy as _
from ast import literal_eval
import logging

LOG = logging.getLogger("LOG")

def process_fields(request, model, obj):
    """
    Function who loop on all permission and generate allow, exclude and readonly fields
    :return: allow_fields, readonly_fields, exclude_fields
    :rtype: set(), set(), set()
    """
    allow_fields = set()
    readonly_fields = set()
    exclude_fields = set()

    permission_registry = get_registry_perms(model)
    for permission in permission_registry:
        perm = permission.perm
        try:
            have_perm = obj.has_smooth_permission(request, perm)
        except KeyError:
            raise PermissionNotFoundException("can_{}_permission not found" . format(perm))
        except Exception as e:
            raise e
        for field in literal_eval(permission.fields):
            if have_perm:
                allow_fields.add(field)
            else:
                readonly_fields.add(field)
        for field in literal_eval(permission.exclude_fields):
            if have_perm:
                allow_fields.add(field)
            else:
                exclude_fields.add(field)

    return allow_fields, readonly_fields, exclude_fields

def get_fields_name(model, is_inline=False):
    fields = []
    for field in get_fields_from_obj(model, is_inline):
        fields += [field.name]
    return fields

class SmoothPermAdmin(admin.ModelAdmin):
    """
    Class for model admin of object with permission, need at least one attr
    :param inline_perm_model: the model inline for permission
    """
    exclude_from_parent = []
    fieldsets_from_parent = []
    fields_from_parent = None

    @property
    def inline_perm_model(self):
        raise NotImplementedError(_("inline_perm_model need to be initialized"))

    def __init__(self, *arg, **kwargs):
        """
        Save all exclude, fields & fieldsets given by code
        """
        if self.exclude is not None:
            self.exclude_from_parent = tuple(self.exclude)

        if self.fieldsets is not None:
            self.fieldsets_from_parent = list(self.fieldsets)

        self.fields_from_parent = self.fields

        super(SmoothPermAdmin, self).__init__(*arg, **kwargs)

    def get_fields(self, request, obj=None):
        if self.fields is None:
            return get_fields_name(self.model, True)

        return self.fields

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if obj.pk is None:
            obj.owner = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        """
        Standard change permission, return True if user has change and/or view perm if we are on object
        else return classic perm with codename
        """
        if obj is not None:
            return obj.has_change_permission(request) or obj.has_view_permission(request)
        return super(SmoothPermAdmin, self).has_change_permission(request, obj)

    def has_add_permission(self, request):
        """
        Standard add permission, return True if user has basic had permission
        """
        return super(SmoothPermAdmin, self).has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """
        Standard delete permission, return True if user has delete perm if we are on object
        else return classic perm with codename
        """
        if obj is not None:
            return obj.has_delete_permission(request)
        return super(SmoothPermAdmin, self).has_delete_permission(request, obj)

    def remove_exclude_from_fieldsets(self, exclude, fieldsets):
        """
        Remove all exclude list in fieldsets
        :param exclude: The list of fields to exclude
        :return: the fieldsets without fields given
        """

        if fieldsets is not None:
            fieldsets = deepcopy(fieldsets)
            exclude = set(exclude)
            for i, key in enumerate(fieldsets):
                fields = list(key[1]['fields'])
                # We need first to remove all list to tuple, and remove exclude list in this one
                for j, field in enumerate(fields):
                    if isinstance(field, (tuple, list)):
                        field = set(field)
                        field -= exclude
                        field = tuple(field)
                    fields[j] = field

                # We get the result of for in above, and we remove exclude list on alone fields
                fields = set(fields)
                fields -= exclude
                fieldsets[i][1]['fields'] = list(fields)
        return fieldsets

    def get_queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = super(SmoothPermAdmin, self).get_queryset(request)
        my_list = list(qs)
        for i, item in enumerate(my_list):
            if not self.has_change_permission(request, item):
                qs = qs.exclude(id=item.id)
        return qs

    def get_readonly_fields(self, request, obj=None):
        """
        Generate fields or fieldsets, exludes and readonly fields using all permissions create.
        All permission are generate in admin by SmoothRegistryModel
        """

        readonly_fields = set()
        readonly_init = set(self.readonly_fields) or set()
        exclude_init = set(self.exclude_from_parent)

        if obj is not None:
            allow_fields, readonly_fields, exclude_fields = process_fields(request, self.model, obj)

            if self.model.permissions.smooth_level_perm is not self.model.permissions.HIGH_LEVEL:
                allow_fields = allow_fields - readonly_fields - exclude_fields

                readonly_fields -= exclude_fields - allow_fields
                exclude_fields -= allow_fields

                self.exclude = list(exclude_init.union(exclude_fields))
                self.exclude.append('owner')

            if not obj.has_change_permission(request) and obj.has_view_permission(request):
                if self.fields:
                    readonly_fields = set(self.fields)
                elif self.declared_fieldsets:
                    readonly_fields = flatten_fieldsets(self.declared_fieldsets)
                else:
                    readonly_fields = set(
                        get_fields_name(self.model)
                    )
                    readonly_fields -= set(self.exclude)

            if not self.fieldsets:
                if not self.fields_from_parent:
                    self.fields_from_parent = list(
                        get_fields_name(self.model)
                    )
                    print self.fields_from_parent

                if len(self.exclude) > 0:
                    self.fields = list(set(self.fields_from_parent) - exclude_fields)
            else:
                if len(self.exclude) > 0:
                    self.fieldsets = self.remove_exclude_from_fieldsets(self.exclude, self.fieldsets_from_parent)
                else:
                    self.fieldsets = list(self.fieldsets_from_parent)

        return list(readonly_init.union(readonly_fields))

    def get_inline_classes(self, request, obj=None):
        """
        Get all inlines class, and add the inline_perm_model if user has can_change_permission.
        :param request: request HTTP
        :param obj: obj in question
        :return: [inlines] list of inlines models
        """
        inlines = set(self.inlines) or set()
        if obj is not None:
            inlines.add(self.inline_perm_model)
            if not obj.has_change_permissions_permission(request):
                inlines.remove(self.inline_perm_model)

        return list(inlines)

    def get_inline_instances(self, request, obj=None):
        """
        Standard get_inline_instance, just update inlines, ..seealso:: get_inline_classes
        """
        self.inlines = self.get_inline_classes(request, obj)
        return super(SmoothPermAdmin, self).get_inline_instances(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Returns a Form class for use in the admin add view. This is used by
        add_view and change_view.
        """
        self.fields = deepcopy(self.fields_from_parent)
        self.exclude = deepcopy(self.exclude_from_parent)
        self.get_readonly_fields(request, obj)
        # For avoid KeyError we remove from fields all exclude
        self.fields = list(set(self.fields) - set(self.exclude))
        self.get_fieldsets(request, obj)

        return super(SmoothPermAdmin, self).get_form(request, obj, **kwargs)


class SmoothPermInlineModelAdmin(InlineModelAdmin):
    """
    Class for inline model admin of object with permission, need at least one attr
    :param inline_perm_model: the model inline for permission
    """
    exclude_from_parent = ()
    fields_from_parent = None

    def __init__(self, *args, **kwargs):
        """
        Save all exclude, fields given
        """
        super(SmoothPermInlineModelAdmin, self).__init__(*args, **kwargs)

        if self.exclude is not None:
            self.exclude_from_parent = tuple(self.exclude)

        if self.fields is not None:
            self.fields_from_parent = list(self.fields)
        else:
            self.fields_from_parent = get_fields_name(self.model, True)

    def get_fields(self, request, obj=None):
        if self.fields is None:
            return get_fields_name(self.model, True)

        return self.fields

    def get_formset(self, request, obj=None, **kwargs):
        """
        Generate readonly and exclude fields just before get the formset
        """
        self.exclude = deepcopy(self.exclude_from_parent)
        self.fields = deepcopy(self.fields_from_parent)
        self.get_readonly_fields(request, obj)

        # For avoid KeyError we remove from fields all exclude
        self.fields = list(set(self.fields) - set(self.exclude))
        formset = super(SmoothPermInlineModelAdmin, self).get_formset(request, obj, fields=self.fields, **kwargs)

        return formset

    def get_readonly_fields(self, request, obj=None):
        """
        Override readonly_fields. If user can only view page, all fields are readonly,
        if user hasn't advanced_settings perm, all :param:smooth_perm_field are readonly
        if user has all perms / superuser all readonly are readonly from modelAdmin
        """
        readonly_fields = set()
        readonly_init = set(self.readonly_fields) or set()
        exclude_init = set(self.exclude_from_parent)

        if obj is not None:
            allow_fields, readonly_fields, exclude_fields = process_fields(request, self.model, obj)

            if obj.permissions.smooth_level_perm is not obj.permissions.HIGH_LEVEL:
                allow_fields = allow_fields - readonly_fields - exclude_fields

            readonly_fields -= exclude_fields - allow_fields
            exclude_fields -= allow_fields

            self.exclude = list(exclude_init.union(exclude_fields))
            self.exclude.append('owner')

            if not obj.has_change_permission(request) and obj.has_view_permission(request):
                readonly_fields = set(self.get_fields(request, obj))
                readonly_fields -= set(self.exclude)

        return list(readonly_init.union(readonly_fields))


class SmoothPermStackedInline(SmoothPermInlineModelAdmin):
    template = 'admin/smooth_perms/edit_inline/stacked.html'


class SmoothPermTabularInline(SmoothPermInlineModelAdmin):
    template = 'admin/smooth_perms/edit_inline/tabular.html'
