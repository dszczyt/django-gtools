# -*- coding: utf-8 -*-

from django.db import models as django_models
from django.db.models import (
    AutoField,
    BigIntegerField,
    BooleanField,
    CharField,
    CommaSeparatedIntegerField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    FilePathField,
    FloatField,
    ImageField,
    IntegerField,
    IPAddressField,
    GenericIPAddressField,
    NullBooleanField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    SlugField,
    SmallIntegerField,
    TextField,
    TimeField,
    URLField,

    ForeignKey,
    OneToOneField,
    ManyToManyField,

    Q,
    F,

    Avg,
    Count,
    Max,
    Min,
    StdDev,
    Sum,
    Variance,

    permalink,
)
from django.core.exceptions import ValidationError

from .base import ModelBase

def secure_update_object(obj, data=None):
    if data is not None:
        obj._secure_update(data)
    return obj

def get_context_for_object(obj, data=None, **kwargs):
    context = kwargs.copy()
    context['object'] = secure_update_object(obj, data)

    if data is not None:
        try:
            obj.full_clean()
        except ValidationError, e:
            context['errors'] = e.message_dict
    return context

class Model(django_models.Model):
    __metaclass__ = ModelBase

    def _secure_update(self, values):
        for key, value in values.items():
            if (self._meta.fields_accessible and key in self._meta.fields_accessible) or \
               (self._meta.fields_protected and key not in self._meta.fields_protected):
                setattr(self, key, value)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Model, self).save(*args, **kwargs)

    class Meta:
        abstract = True
