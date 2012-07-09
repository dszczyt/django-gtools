# -*- coding: utf-8 -*-
# from django.db import models <--- this old import is odd

from gtools import models

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField(u"date published")

    #@question.setter
    #def question(self, value):
    #    if value[-1] != u"?":
    #        raise models.ValidationError(u"Your question should end with a question mark.")
    #    self.set_value('question', value)

    #class Meta:
    #    protected = ['pub_date']

    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    #class Meta:
    #    accessible = ['choice']

    def __unicode__(self):
        return self.choice
