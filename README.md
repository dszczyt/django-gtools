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

class Choice(gmodels.Model):
    poll = gmodels.ForeignKey(Poll)
    choice = gmodels.CharField(max_length=200)
    votes = gmodels.IntegerField()

    class Meta:
        accessible = ['choice']
```

views.py
```python
# -*- coding: utf-8 -*-
from poll.models import Poll
import gtools

class Poll(gtools.View):
    # request is an instance variable, we can access it everywhere !

    @gtools.html("poll_form.html")
    def add(self):
        return {
            'object': Poll()
        }

    @gtools.redirect
    def create(self):
        return {
            'object':
        }

    @gtools.html # access with html
    def change(self, id):
        pass

    def
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
