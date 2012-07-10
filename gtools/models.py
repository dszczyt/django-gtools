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

from .base import ModelBase

class Model(django_models.Model):
    __metaclass__ = ModelBase

    def _secure_update(self, values):
        for key, value in values.items():
            if key in self._meta.fields_accessible:
                setattr(self, key, value)

    class Meta:
        abstract = True
