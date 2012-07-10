# -*- coding: utf-8 -*-
import inspect
from functools import wraps
import sys

from django.shortcuts import render_to_response
from django.conf.urls.defaults import url, include
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.template import RequestContext

from functools import WRAPPER_ASSIGNMENTS as DEFAULT_WRAPPER_ASSIGNMENTS

WRAPPER_ASSIGNMENTS = DEFAULT_WRAPPER_ASSIGNMENTS + ('urls', )

def available_attrs(fn):
    """
    Return the list of functools-wrappable attributes on a callable.
    This is required as a workaround for http://bugs.python.org/issue3445.
    """
    return tuple(a for a in WRAPPER_ASSIGNMENTS if hasattr(fn, a))


def html(_template_name=None):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def _wrapped(self, *args, **kwargs):
            context = func(self, *args, **kwargs)

            template_name = _template_name
            if not template_name:
                model_module = sys.modules[self.__class__.__module__]
                app_label = model_module.__name__.split('.')[-2]

                template_name = "%s/%s/%s.html" % (
                    app_label,
                    self.__class__.__name__.lower(),
                    func.func_name,
                )
                if callable(template_name):
                    template_name = template_name(context)

            return render_to_response(
                template_name,
                self.context(**context),
                RequestContext(self.request),
            )

        if not hasattr(_wrapped, "urls"):
            _wrapped.urls = getattr(func, "urls", [])

        url_args = ""
        func_args = inspect.getargspec(func).args[1:]
        for arg in func_args:
            if arg.endswith('_id'):
                arg_regex = r'\d+'
            else:
                arg_regex = r'\w+'

            url_args = r"%s/(?P<%s>%s)" % (
                url_args,
                arg,
                arg_regex,
            )

        _wrapped.urls.append(
            r'^%s%s/$' % (
                func.func_name,
                url_args,
            )
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
                return HttpResponseNotAllowed(methods)
            return func(self, *args, **kwargs)
        return _wrapped
    return decorator


def xml(template_name=None):
    def decorator(fn):
        @wraps(fn, assigned=available_attrs(fn))
        def new_function(self, *args, **kwargs):
            return fn(self, *args, **kwargs)
        new_function.__name__ = fn.__name__
        if not hasattr(new_function, "urls"):
            new_function.urls = getattr(fn, "urls", [])
        new_function.urls.append(
            r'^%s.xml$' % fn.__name__
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
            r'^%s.json$' % fn.__name__
        )
        return new_function
    return decorator

def redirect(to=None, *args, **kwargs):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def _wrapped(self, *args, **kwargs):
            from django.shortcuts import redirect
            obj = func(self, *args, **kwargs)
            if to == None:
                return HttpResponseRedirect(obj.get_absolute_url())
            if callable(to):
                return HttpResponseRedirect(to(obj))
            return redirect(to, *args, **kwargs)

        if not hasattr(_wrapped, "urls"):
            _wrapped.urls = getattr(func, "urls", [])
        _wrapped.urls.append(
            r'^%s/$' % func.__name__
        )
        return _wrapped

    return decorator

class Views(object):
    request = None

    def __call__(self, request, name, **kwargs):
        self.request = request
        return getattr(self, name)(**kwargs)

    def context(self, **kwargs):
        return kwargs

    def urlpatterns(self, namespace=None, app_name=None):
        urls = []
        for method_name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod):
            if not hasattr(method, "urls"):
                continue
            for regexp in method.urls:
                urls.append(
                    url(
                        regexp,
                        self,
                        kwargs = {
                            'name': method_name,
                        },
                        name = method_name
                    )
                )

        if app_name is None:
            app_name = self.__class__.mro()[2].__name__
        if namespace is None:
            #namespace = "%s_%s" % (self.__class__.mro()[2].__name__, self.__class__.__name__)
            namespace = self.__class__.__name__
        print namespace

        return include(
            urls,
            namespace = namespace,
            app_name = app_name,
        )

