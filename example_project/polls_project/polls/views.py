# -*- coding: utf-8 -*-
from polls_project.polls.models import Poll
import gtools
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from gtools.models import secure_update_object, get_context_for_object

class PollViews(gtools.Views):
    @gtools.methods_allowed('GET', 'POST')
    @gtools.html() # access with html
    def add(self):
        return get_context_for_object(
            Poll(),
            self.request.POST or None,
        )

    @gtools.methods_allowed('POST')
    @gtools.fallback_on_except(ValidationError, add)
    @gtools.redirect()
    def create(self):
        obj = secure_update_object(
            Poll(),
            self.request.POST
        )
        obj.save()
        return obj

    @gtools.methods_allowed('GET', 'POST')
    @gtools.html()
    def edit(self, object_id):
        return get_context_for_object(
            get_object_or_404(Poll, pk=object_id),
            self.request.POST or None,
        )

    @gtools.methods_allowed('POST')
    @gtools.fallback_on_except(ValidationError, edit)
    @gtools.redirect()
    def update(self, object_id):
        obj = secure_update_object(
            get_object_or_404(Poll, pk=object_id),
            self.request.POST
        )
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
