#!/usr/bin/env python

from django.template import RequestContext
from django.shortcuts import render_to_response
from myprojects.models import Project
from basic.blog.models import Post

def home(request):

    return render_to_response('home.html',{'projects':Project.objects.all()[:8],
        'posts':Post.objects.all()[:3]}, context_instance = RequestContext(request))

# vim: et sw=4 sts=4
