# -*- coding: utf-8 -*-
from smooth_perms.models import SmoothGroup
import logging

LOG = logging.getLogger("LOG")


def post_save_user_group(instance, raw, created, **kwargs):
    """
        requires: CurrentUserMiddleware
    """

    LOG.debug("TEST")
    from smooth_perms.utils.permissions import get_current_user
    # read current user from thread locals
    creator = get_current_user()
    if not creator or not created or creator.is_anonymous():
        return
    smooth_group = SmoothGroup(group_ptr_id=instance.pk, created_by=creator)
    smooth_group.__dict__.update(instance.__dict__)
    smooth_group.save()