# -*- coding: utf-8 -*-
"""
..module:widgets
    :project: 
    :platform: Unix
    :synopsis: Module for core database specification, created on 05/02/2016 

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>

"""
from django import forms
from ast import literal_eval
import logging

LOG = logging.getLogger("LOG")


class SelectMultipleChosen(forms.SelectMultiple):
    class Media:
        css = {
            'all': ('smooth_perms/css/chosen.min.css', 'smooth_perms/css/module_overflow.css', 'smooth_perms/css/django-cms-patch.css')
        }
        js = ('admin/js/jquery.js', 'smooth_perms/js/chosen.jquery.min.js',)

    def render(self, name, value, attrs=None, choices=()):
        if not isinstance(value, (list, tuple)):
            value = literal_eval(value)
        output = super(SelectMultipleChosen, self).render(name, value, attrs, choices)
        output += '<script type="text/javascript" >$("select[name={0}]").chosen({1})</script>' . format(name, '{}')
        return output
