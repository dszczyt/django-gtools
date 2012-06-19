django-gtools
=============

HOW IT SHOULD WORK ?
--------------------

models.py
```python
from gtools import gmodels

class Poll(gmodels.Model):
    question = gmodels.CharField(max_length=200)
    pub_date = gmodels.DateTimeField('date published')

    @question.setter
    def question(self, value):
        if value[-1] != '?':
            raise ValidationError("Your question should end with a question mark.")
        self.set_value("question", value)

    class Meta:
        protected = ['pub_date']

class Choice(gmodels.Model):
    poll = gmodels.ForeignKey(Poll)
    choice = gmodels.CharField(max_length=200)
    votes = gmodels.IntegerField()

    class Meta:
        accessible = ['choice']
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
