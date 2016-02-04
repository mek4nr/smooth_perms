from .groups import *
from .options import *
from .permissions import *

from django.conf import settings
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

user_app_name, user_model_name = settings.AUTH_USER_MODEL.rsplit('.', 1)
User = None
try:
    User = apps.get_registered_model(user_app_name, user_model_name)
except KeyError:
    pass
if User is None:
    raise ImproperlyConfigured(
        "You have defined a custom user model %s, but the app %s is not "
        "in settings.INSTALLED_APPS" % (settings.AUTH_USER_MODEL, user_app_name)
    )


smooth_registry.register(User)
smooth_registry.register(SmoothGroup)
