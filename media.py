import os
import mimetypes
from django.conf import settings
from django.shortcuts import Http404
from django.http import HttpResponse
from django.views.static import directory_index

from runpy import run_module
from django.utils.importlib import import_module
import imp


        # For each app, we need to look for an admin.py inside that app's
        # package. We can't use os.path here -- recall that modules may be
        # imported different ways (think zip files) -- so we need to get
        # the app's __path__ and look for admin.py on that path.

        # Step 1: find out the app's __path__ Import errors here will (and
        # should) bubble up, but a missing __path__ (which is legal, but weird)
        # fails silently -- apps that do weird things with __path__ might
        # need to roll their own admin registration.

def get_by_path(path):
    pathsplit = path.split(os.sep)
    for app in settings.INSTALLED_APPS:
        # Split of the last part of the app name; e.g. 'django.contrib.admin' -> 'admin'

        app_short_name = app.rpartition('.')[2]
        if app_short_name == pathsplit[0]:
            yield app


def get_path(path, basepath):
    apps = get_by_path(path)
    pathsplit = path.split(os.sep)
    for app in apps:
        try:
            app_path = import_module(app).__file__
            moddir = os.path.dirname(app_path)
            return os.path.join(moddir, 'media', *pathsplit[1:])
        except AttributeError:
            continue
    return os.path.join(basepath, path)


def serve_apps(request, path, document_root=None):
    """
    This view serves static media and directory indexes for a django application. It should
    only be used in development, media should be provided directly by a web server in production.
    
    This view assumes a django application stores its media in app/media (which is very common) and
    the file is referred to in the templates by the last part of a django app path. e.g. As in
    django.contrib.admin -> 'admin'.
    
    First we check if the media is a request in an application directory; if so we attempt to serve
    it from there. Then we attempt to provide the document from the document_root parameter (if
    provided).

    To use this view you should add something like the following to urls.py:
    if settings.DEBUG:
        urlpatterns += (r'^media/(?P<path>.*)$', 'site.media.serve_apps', {'document_root' : settings.MEDIA_ROOT})
        
    You can then have the admin media files served by setting
    ADMIN_MEDIA_PREFIX = '/media/admin/'
    """
    abspath = get_path(path, document_root) or ''
    if not os.path.exists(abspath):
        raise Http404("No media found for path %s (tried '%s')" % (path, abspath))
    if os.path.isdir(abspath):
        # To make the template work a directory must have a trailing slash in the url
        # The one exception is when path == /
        if not path.endswith('/') and path:
            raise Http404("This path is a directory. Add a trailing slash to view index")
        return directory_index(path[:-1], abspath)
    
    mimetype = mimetypes.guess_type(abspath)[0] or 'application/octet-stream'
    contents = open(abspath, 'rb').read()
    response = HttpResponse(contents, mimetype=mimetype)
    response["Content-Length"] = len(contents)
    return response

# vim: et sw=4 sts=4
