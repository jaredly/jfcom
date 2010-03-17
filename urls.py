from django.conf.urls.defaults import *
import os
print 'urls...'

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import appsettings
appsettings.autodiscover()

MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')
import media
import settings

urlpatterns = patterns('',
    #(r'^$', homepage.views.home),
    (r'^blog/', include('basic.blog.urls')),
    (r'^todo/', include('todo.urls')),
    (r'^feedback/', include('feedback.urls')),
    (r'^settings/', include('appsettings.urls')),
    (r'^projects/', include('myprojects.urls')),
    (r'^photologue/', include('photologue.urls')),
    # Example:
    # (r'^jfcom/', include('jfcom.foo.urls')),
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #        {'document_root':MEDIA_ROOT, 'show_indexes':True}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^bad/$', 'django.views.generic.simple.direct_to_template', {'template':'bad.html'}),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', media.serve_apps, {'document_root' : settings.MEDIA_ROOT}),
)
#if settings.DEBUG or True:
#    urlpatterns += patterns((r'^media/(?P<path>.*)$', media.serve_apps, {'document_root' : settings.MEDIA_ROOT}))
