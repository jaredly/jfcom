#!/usr/bin/env python

# activate reversion

from django.contrib import admin
from reversion.admin import VersionAdmin
from basic.blog.models import Post

from myprojects.models import Project

class ProjectRevAdmin(VersionAdmin):
    pass


from reversion.models import Revision, Version
admin.site.register(Revision)
admin.site.register(Version)

# vim: et sw=4 sts=4
