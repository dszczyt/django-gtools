# -*- coding: utf-8 -*-
# from django.db import models <--- this old import is odd

from gtools import models

import datetime

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField(u"date published", default=datetime.datetime.now())

    #@question.setter
    #def question(self, value):
    #    if value[-1] != u"?":
    #        raise models.ValidationError(u"Your question should end with a question mark.")
    #    self.set_value('question', value)

    #class Meta:
    #    protected = ['pub_date']

    def __unicode__(self):
        return self.question

    @models.permalink
    def get_absolute_url(self):
        return (
            "PollViews:show",
            (),
            {
                'object_id': self.pk
            }
        )

    class Meta:
        fields_accessible = [
            'question',
            'pub_date',
        ]

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    #class Meta:
    #    accessible = ['choice']

    def __unicode__(self):
        return self.choice
