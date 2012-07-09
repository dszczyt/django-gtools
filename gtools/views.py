# -*- coding: utf-8 -*-
import inspect
from functools import wraps

from django.utils.decorators import classonlymethod, method_decorator
from django.shortcuts import render_to_response
from django.conf.urls.defaults import url, patterns, include
from django.http import HttpResponseNotAllowed

from django.utils.decorators import available_attrs

class ObjectListNotInContext(Exception):
    def __str__(self):
        return "'object_list' key not found"

class ObjectNotInContext(Exception):
    def __str__(self):
        return "'object' key not found"

def get_class_that_defined_method(meth):
    from pprint import pprint
    #pprint(
    #    dict(
    #        map(lambda x: (x, getattr(meth, x)), dir(meth))
    #    )
    #)
    #pprint(meth.__dict__)

    #obj = meth.im_self
    print inspect.getmodule(meth)
    for cls in inspect.getmro(meth.im_class):
        if meth.__name__ in cls.__dict__:
            return cls
    return None

def html(_template_name=None):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def _wrapped(self, *args, **kwargs):
            context = func(self, *args, **kwargs)
            try:
                object_list = context["object_list"]
            except KeyError:
                raise ObjectListNotInContext

            template_name = _template_name
            if not template_name:
                opts = object_list.model._meta
                app_label = opts.app_label

                template_name = "%s/%s/%s.html" % (
                    app_label,
                    self.__class__.__name__.lower(),
                    func.func_name,
                )
                if callable(template_name):
                    template_name = template_name(object_list)

            return render_to_response(
                template_name,
                context,
            )

        if not hasattr(_wrapped, "urls"):
            _wrapped.urls = getattr(func, "urls", [])
        _wrapped.urls.append(
            r'^(?P<name>%s)/$' % func.__name__
        )
        return _wrapped
    return decorator

def fallback_on_except(exception, fallback):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def _wrapped(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except exception:
                return fallback(self, *args, **kwargs)
        return _wrapped
    return decorator

def methods_allowed(*methods):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def _wrapped(self, *args, **kwargs):
            if self.request.method not in methods:
                raise HttpResponseNotAllowed(methods)
            return func(self, *args, **kwargs)
        return _wrapped
    return decorator


def xml(template_name=None):
    def decorator(fn):
        def new_function(self, *args, **kwargs):
            return fn(self, *args, **kwargs)
        new_function.__name__ = fn.__name__
        if not hasattr(new_function, "urls"):
            new_function.urls = getattr(fn, "urls", [])
        new_function.urls.append(
            r'^(?P<name>%s).xml$' % fn.__name__
        )
        return new_function
    return decorator

def json(template_name=None):
    def decorator(fn):
        def new_function(self, *args, **kwargs):
            return fn(self, *args, **kwargs)
        new_function.__name__ = fn.__name__
        if not hasattr(new_function, "urls"):
            new_function.urls = getattr(fn, "urls", [])
        new_function.urls.append(
            r'^(?P<name>%s).json$' % fn.__name__
        )
        return new_function
    return decorator


class Views(object):
    request = None

    def __call__(self, request, name, **kwargs):
        self.request = request
        return getattr(self, name)(**kwargs)

    def urlpatterns(self):
        urls = []
        for method_name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod):
            if not hasattr(method, "urls"):
                continue
            for regexp in method.urls:
                urls.append(
                    url(
                        regexp,
                        self,
                        name = method_name
                    )
                )

        return include(
            urls,
            namespace = self.__class__.__name__,
            app_name = self.__class__.mro()[1].__name__
        )

