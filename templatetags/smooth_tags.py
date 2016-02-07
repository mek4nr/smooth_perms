# -*- coding: utf-8 -*-
"""
..module:annoncetags
    :project: 
    :platform: Unix
    :synopsis: Module for core database specification, created on 21/10/2015 

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>

"""
from django import template
import logging

LOG = logging.getLogger("LOG")
register = template.Library()


@register.assignment_tag
def can_add(fields):
    """
    :return: True if user can participate
    """
    add = False
    for field in fields:
        if not hasattr(field, 'is_readonly'):
            add = True
    LOG.debug(add)
    return add


@register.filter
def contain(var):
    LOG.debug(var)
    return "{}" . format(dir(var))