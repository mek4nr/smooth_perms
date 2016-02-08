# -*- coding: utf-8 -*-
"""
..module:utils.permissions
    :project: smooth_perms
    :platform: Unix
    :synopsis: Utils for set/get current user without using request, created on 04/02/2016. Take from django_cms

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>

"""
from threading import local

# thread local support
_thread_locals = local()


def set_current_user(user):
    """
    Assigns current user from request to thread_locals, used by
    CurrentUserMiddleware.
    """
    _thread_locals.user = user


def get_current_user():
    """
    Returns current user, or None
    """
    return getattr(_thread_locals, 'user', None)
