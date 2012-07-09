# -*- coding: utf-8 -*-
from django.db import models as django_models

from django.db.models import CharField, ForeignKey, IntegerField, DateTimeField

class Model(django_models.Model):
    class Meta:
        abstract = True
