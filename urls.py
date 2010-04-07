from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

import admin as myadmin

from basic.blog.feeds import BlogPostsFeed, BlogPostsByCategory

feeds = {
        'latest':BlogPostsFeed,
        'category':BlogPostsByCategory,
    }

import views

urlpatterns = patterns('',
    (r'^$', views.home),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict':feeds}),
    (r'^blog/', include('basic.blog.urls')),
    (r'^feedback/', include('feedback.urls')),
    (r'^settings/', include('appsettings.urls')),
    (r'^projects/', include('myprojects.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$', serve, {'document_root' : settings.MEDIA_ROOT, 'show_indexes':True}),
    )
