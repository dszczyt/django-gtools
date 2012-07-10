# -*- coding: utf-8 -*-
from django.db import models as django_models

from django.db.models import CharField, ForeignKey, IntegerField, DateTimeField

from django.db.models import permalink

class Model(django_models.Model):
    def _secure_update(self, values):
        for key, value in values.items():
            setattr(self, key, value)

    class Meta:
        abstract = True
