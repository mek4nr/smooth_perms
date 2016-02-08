# -*- coding: utf-8 -*-
"""
..module:forms.registry
    :project: smooth_perms
    :platform: Unix
    :synopsis: Module for registry forms, created on 05/02/2016

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>

"""
from django import forms
from smooth_perms.forms.fields import MultipleChoiceFieldFields


class PermissionAdminMixinInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermissionAdminMixinInlineForm, self).__init__(*args, **kwargs)
        choices = None
        if self.instance.pk is not None and choices is None:
            choices = self.instance.smooth_registry.get_fields_from_content_type()

            self.fields['fields'] = MultipleChoiceFieldFields(
                choices=choices,
                required=False,
            )
            self.fields['exclude_fields'] = MultipleChoiceFieldFields(
                choices=choices,
                required=False
            )
