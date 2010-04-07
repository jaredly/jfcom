#!/usr/bin/env python

# activate reversion

from django.contrib import admin
from reversion.admin import ReversionAdmin
from basic.blog.models import Post

class PostRevAdmin(VersionAdmin):
    """Admin settings"""

admin.site.register(Post, PostRevAdmin)

from myprojects.models import Project

class ProjectRevAdmin(VersionAdmin):
    pass

admin.site.register(Project, ProjectRevAdmin)


# vim: et sw=4 sts=4
