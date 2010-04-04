from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns('',
    (r'^$', views.home),
    (r'^blog/', include('basic.blog.urls')),
    (r'^feedback/', include('feedback.urls')),
    (r'^settings/', include('appsettings.urls')),
    (r'^projects/', include('myprojects.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

