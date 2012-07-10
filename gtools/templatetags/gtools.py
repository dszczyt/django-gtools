# -*- coding: utf-8 -*-
from easytags import EasyLibrary

register = EasyLibrary()

@register.easytag
def hidden_input(context, obj, name, *values):
    return u"<input type=\"text\" name=\"%s\" value=\"%s\"/>" % (
        name,
        filter(lambda x: x, [getattr(obj, name)] + list(values))[0],
    )


@register.easytag
def text_input(context, obj, name, *values):
    return u"<input type=\"text\" name=\"%s\" value=\"%s\"/>" % (
        name,
        filter(lambda x: x, [getattr(obj, name)] + list(values))[0],
    )

