from django.db.models import signals
from smooth_perms.signals.groups import post_save_user_group
from django.contrib.auth.models import Group

signals.post_save.connect(post_save_user_group, sender=Group)
