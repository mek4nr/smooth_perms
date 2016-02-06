from smooth_perms.models import SmoothRegistryModel, PermissionAdminMixin
from smooth_perms.forms import PermissionAdminMixinInlineForm
from django.contrib import admin


class PermissionAdminMixinInline(admin.TabularInline):
    model = PermissionAdminMixin
    extra = 0
    form = PermissionAdminMixinInlineForm
    fields = ["fields", "exclude_fields"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SmoothRegistryModel)
class SmoothRegistryAdmin(admin.ModelAdmin):
    readonly_fields = ["name", "content_type"]

    inlines = [PermissionAdminMixinInline]
    model = SmoothRegistryModel

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
