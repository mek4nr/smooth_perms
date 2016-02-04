from smooth_perms.models import SmoothRegistryModel, PermissionAdminMixin
from django.contrib import admin


class PermissionAdminMixinInline(admin.TabularInline):
    model = PermissionAdminMixin
    extra = 0


@admin.register(SmoothRegistryModel)
class SmoothRegistryAdmin(admin.ModelAdmin):
    readonly_fields = ["name"]

    inlines = [PermissionAdminMixinInline]
    model = SmoothRegistryModel

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
