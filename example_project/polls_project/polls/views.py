# -*- coding: utf-8 -*-
from polls_project.polls.models import Poll
import gtools
from django.shortcuts import get_object_or_404

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
    #@gtools.fallback_on_except(Poll.ValidationError, add)
    @gtools.redirect()
    def create(self):
        obj = Poll()
        obj._secure_update(self.request.POST)
        obj.save()
        return obj

    @gtools.methods_allowed('GET')
    @gtools.html()
    def edit(self, object_id):
        return {
            'object': get_object_or_404(Poll, pk=object_id)
        }

    @gtools.methods_allowed('POST')
    #@gtools.fallback_on_except(Poll.ValidationError, edit)
    @gtools.redirect()
    def update(self, object_id):
        obj = get_object_or_404(
            Poll,
            pk=object_id,
        )
        obj._secure_update(self.request.POST)
        obj.save()
        return obj

    # I want to see the list with html, xml and json !
    @gtools.methods_allowed('GET')
    @gtools.html()
    @gtools.xml()
    @gtools.json()
    def list(self):
        return {
            'object_list': Poll.objects.all()
        }

    @gtools.methods_allowed('GET')
    @gtools.html()
    def show(self, object_id):
        return {
            'object': get_object_or_404(Poll, pk=object_id),
        }
