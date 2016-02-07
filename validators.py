from django import forms
from ast import literal_eval
from django.utils.translation import ugettext_lazy as _


def validate_tab(value):
    """
    Function who validate if value giver has good syntax for choice
    :param value: String
    :return: None
    """
    try:
        t = literal_eval(value)
        if not isinstance(t, (tuple, list)):
            raise forms.ValidationError(_("Your choice isn't a tuple or a List"))
    except SyntaxError:
        raise forms.ValidationError(_("Syntax isn't correct for a tuple or list"))