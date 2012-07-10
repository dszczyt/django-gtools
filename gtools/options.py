# -*- coding: utf-8 -*-
import re
from django.conf import settings
from django.db.models.options import Options as DjangoOptions, get_verbose_name
from django.utils.translation import string_concat

DEFAULT_NAMES = ('verbose_name', 'verbose_name_plural', 'db_table', 'ordering',
                 'unique_together', 'permissions', 'get_latest_by',
                 'order_with_respect_to', 'app_label', 'db_tablespace',
                 'abstract', 'managed', 'proxy', 'auto_created',
                 # below : specific meta attributes
                 'fields_accessible', 'fields_protected',
                )

class Options(DjangoOptions):
    def __init__(self, meta, app_label=None):
        super(Options, self).__init__(meta, app_label)
        self.fields_accessible = []
        self.fields_protected = []

    def contribute_to_class(self, cls, name):
        from django.db import connection
        from django.db.backends.util import truncate_name

        cls._meta = self
        self.installed = re.sub('\.models$', '', cls.__module__) in settings.INSTALLED_APPS
        # First, construct the default values for these options.
        self.object_name = cls.__name__
        self.module_name = self.object_name.lower()
        self.verbose_name = get_verbose_name(self.object_name)

        # Next, apply any overridden values from 'class Meta'.
        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for name in self.meta.__dict__:
                # Ignore any private attributes that Django doesn't care about.
                # NOTE: We can't modify a dictionary's contents while looping
                # over it, so we loop over the *original* dictionary instead.
                if name.startswith('_'):
                    del meta_attrs[name]
            for attr_name in DEFAULT_NAMES:
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs.pop(attr_name))
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self.meta, attr_name))

            # unique_together can be either a tuple of tuples, or a single
            # tuple of two strings. Normalize it to a tuple of tuples, so that
            # calling code can uniformly expect that.
            ut = meta_attrs.pop('unique_together', self.unique_together)
            if ut and not isinstance(ut[0], (tuple, list)):
                ut = (ut,)
            self.unique_together = ut

            # verbose_name_plural is a special case because it uses a 's'
            # by default.
            if self.verbose_name_plural is None:
                self.verbose_name_plural = string_concat(self.verbose_name, 's')

            # Any leftover attributes must be invalid.
            if meta_attrs != {}:
                raise TypeError("'class Meta' got invalid attribute(s): %s" % ','.join(meta_attrs.keys()))
        else:
            self.verbose_name_plural = string_concat(self.verbose_name, 's')
        del self.meta

        # If the db_table wasn't provided, use the app_label + module_name.
        if not self.db_table:
            self.db_table = "%s_%s" % (self.app_label, self.module_name)
            self.db_table = truncate_name(self.db_table, connection.ops.max_name_length())


