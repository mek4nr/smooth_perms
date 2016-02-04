from django.db import models
from smooth_perms.validators import validate_tab

class SmoothRegistryModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}" . format(self.name)

    def __unicode__(self):
        return self.__str__()


class PermissionAdminMixin(models.Model):
    smooth_registry = models.ForeignKey(SmoothRegistryModel, related_name="registry")

    perm = models.CharField(max_length=1000)
    fields = models.CharField(max_length=1000, validators=[validate_tab])

    def __str__(self):
        return "{}{}" . format(self.perm, self.fields)

    def __unicode__(self):
        return self.__str__()
