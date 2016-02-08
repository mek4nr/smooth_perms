# -*- coding: utf-8 -*-
"""
..module:signals.groups
    :project: smooth_perms
    :platform: Unix
    :synopsis: Module for group model signals , created on 04/02/2016

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>

"""
from smooth_perms.models import SmoothGroup


def post_save_user_group(instance, raw, created, **kwargs):
    """
        requires: CurrentUserMiddleware
    """

    from smooth_perms.utils.permissions import get_current_user
    # read current user from thread locals
    creator = get_current_user()
    if not creator or not created or creator.is_anonymous():
        return
    smooth_group = SmoothGroup(group_ptr_id=instance.pk, created_by=creator)
    smooth_group.__dict__.update(instance.__dict__)
    smooth_group.save()
