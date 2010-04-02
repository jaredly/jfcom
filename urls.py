from django.conf.urls.defaults import *
import os
print 'urls...'

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')
import media
import settings

import views

urlpatterns = patterns('',
    (r'^$', views.home),
    (r'^blog/', include('basic.blog.urls')),
    # (r'^todo/', include('todo.urls')),
    (r'^feedback/', include('feedback.urls')),
    (r'^settings/', include('appsettings.urls')),
    (r'^projects/', include('myprojects.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', media.serve_apps, {'document_root' : settings.MEDIA_ROOT}),
)
#if settings.DEBUG or True:
#    urlpatterns += patterns((r'^media/(?P<path>.*)$', media.serve_apps, {'document_root' : settings.MEDIA_ROOT}))
