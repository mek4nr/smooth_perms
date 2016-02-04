from django.contrib.admin.options import InlineModelAdmin


class SmoothPermInlineAdmin(InlineModelAdmin):
    """
    Class form inline permission
    """

    extra = 0

    def has_change_permission(self, request, obj=None):
        """
        Standard change permission, if inline is show user can add & change
        """
        return True

    def has_add_permission(self, request):
        """
        Standard add permission, if inline is show user can add & change
        """
        return True

    def has_delete_permission(self, request, obj=None):
        """
        Standard delete permission, can_delete is init from get_formset
        """
        return self.can_delete

    def get_formset(self, request, obj=None, **kwargs):
        """
        Some fields may be excluded here. User can change only
        permissions which are available for him. E.g. if user does not haves
        can_publish flag, he can't change assign can_publish permissions.
        """
        exclude = self.exclude or []

        if obj is not None:
            for perm in getattr(getattr(obj, 'permissions')(), 'PERMISSIONS'):
                if not obj.has_generic_permission(request, perm):
                    exclude.append('can_{}' . format(perm))

            self.can_delete = obj.has_delete_permissions_permission(request)

        formset_cls = super(SmoothPermInlineAdmin, self).get_formset(request, obj=None, exclude=exclude, **kwargs)
        return formset_cls


class SmoothPermInlineTabularAdmin(SmoothPermInlineAdmin):
    template = 'admin/edit_inline/tabular.html'


class SmoothPermInlineStackedAdmin(SmoothPermInlineAdmin):
    template = 'admin/edit_inline/stacked.html'
