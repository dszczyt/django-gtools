# -*- coding: utf-8 -*-
from polls_project.polls.models import Poll
import gtools

class PollViews(gtools.Views):
    # request is an instance variable, we can access it everywhere !

    def context(self, **kwargs):
        return super(PollViews, self).context(
            **kwargs
        )

    @gtools.methods_allowed('GET', 'POST')
    @gtools.html() # access with html
    def add(self):
        return {
            'object': Poll()
        }

    @gtools.methods_allowed('POST')
    @gtools.fallback_on_except(Poll.ValidationError, add)
    def create(self):
        return {
            'object': Poll.objects.create(**self.request.POST)
        }

    @gtools.methods_allowed('GET')
    @gtools.html() #("poll_form.html")
    def edit(self, object_id):
        pass

    @gtools.methods_allowed('POST')
    @gtools.fallback_on_except(Poll.ValidationError, edit)
    def update(self, object_id):
        pass

    # I want to see the list with html, xml and json !
    @gtools.methods_allowed('GET')
    @gtools.html()
    @gtools.xml()
    @gtools.json()
    def list(self):
        return {
            'object_list': Poll.objects.all()
        }
