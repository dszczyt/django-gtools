django-gtools
=============

HOW IT SHOULD WORK ?
--------------------

models.py
```python
# -*- coding: utf-8 -*-
from gtools import gmodels

class Poll(gmodels.Model):
    question = gmodels.CharField(max_length=200)
    pub_date = gmodels.DateTimeField(u"date published")

    @question.setter
    def question(self, value):
        if value[-1] != u"?":
            raise ValidationError(u"Your question should end with a question mark.")
        self.set_value('question', value)

    class Meta:
        protected = ['pub_date']

    def __unicode__(self):
        return self.question

class Choice(gmodels.Model):
    poll = gmodels.ForeignKey(Poll)
    choice = gmodels.CharField(max_length=200)
    votes = gmodels.IntegerField()

    class Meta:
        accessible = ['choice']

    def __unicode__(self):
        return self.choice
```

Playing with these models :
```python
poll = Poll(question="What's up ?", choice_set=[{'choice': 'Not much'}, {'choice': 'Just hacking again'}])
poll.question
# What's up ?
poll.choice_set.all()
# QuerySet(<Choice: Not much>, <Choice: Just hacking again>)
poll.save() # saves poll and its choices
poll.question = "What's new ?"
poll.save() # saves poll, but not its choices because they are not modified !
```

views.py
```python
# -*- coding: utf-8 -*-
from poll.models import Poll
import gtools

class Poll(gtools.View):
    # request is an instance variable, we can access it everywhere !

    @gtools.html # access with html
    def add(self):
        return {
            'object': Poll()
        }

    @gtools.redirect
    def create(self):
        return {
            'object': Poll.objects.create(**self.request.POST)
        }

    @gtools.html("poll_form.html")
    def change(self, id):
        pass

    # I want to see the list with html, xml and json !
    @gtools.html
    @gtools.xml
    @gtools.json
    def list(self):
        return {
            'object_list': Poll.objects.all()
        }
```

poll_form.html
```html
{% load gtools %}
<html>
    <head>
        <title>Edit poll</title>
    </head>
    <body>
        <h1>Edit poll</h1>
        <form method="post" action=".">
            {% ginput object.question %}
            {% gsubmit "save" %}
        </form>
    </body>
</html>
```
