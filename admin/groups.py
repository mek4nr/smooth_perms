from django.forms.utils import ErrorList
from django import forms
from django.contrib import admin

from smooth_perms.utils.permissions import get_current_user
from smooth_perms.utils.register import smooth_registry
from smooth_perms.models import SmoothGroup


class SmoothGroupForm(forms.ModelForm):
    """
    Generic form for User & Group permissions in cms
    """

    def __init__(self, data=None, files=None, auto_id='id_{}', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if instance:
            initial = initial or {}
            initial.update(self.populate_initials(instance))
        super(SmoothGroupForm, self).__init__(data, files, auto_id, prefix,
                                              initial, error_class, label_suffix, empty_permitted, instance)
        self.fields.update(smooth_registry.get_fields_form())

    def populate_initials(self, obj):
        return smooth_registry.get_initials(obj)

    def save(self, commit=True):
        group = super(SmoothGroupForm, self).save(commit=False)
        created = not bool(group.pk)
        if created:
            group.created_by = get_current_user()
        smooth_registry.save_permissions(self.cleaned_data, group)
        return group


class SmoothGroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('name',)}),
    ]

    model = SmoothGroup
    form = SmoothGroupForm

    def __init__(self, *args, **kwargs):
        super(SmoothGroupAdmin, self).__init__(*args, **kwargs)

    def get_fieldsets(self, request, obj=None):
        # The function is called one time before form is created
        # So we add a token in request in first call, next
        # we can call dynamic fields (form is created)
        if hasattr(request, "_gfs_marker"):
            return smooth_registry.update_permission_fieldsets(request, self.fieldsets)
        setattr(request, "_gfs_marker", 1)
        return super(SmoothGroupAdmin, self).get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if obj.pk is None:
            obj.owner = request.user
        obj.save()
