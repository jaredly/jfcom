#!/usr/bin/python2.6
import sys, os
from os.path import expanduser

print 'Content-type:text/html\n'

# Add a custom Python path.
sys.path.insert(0, expanduser("~/python"))
sys.path.insert(0, expanduser("~/lib/python"))
sys.path.insert(0, expanduser("~/lib/python/flup-1.0.2"))
sys.path.insert(0, expanduser("~/lib/python/Pygments-1.3.1-py2.6.egg"))
sys.path.insert(0, expanduser("~/lib/python/docutils-0.6-py2.6.egg"))
sys.path.insert(0, expanduser("~/lib/python2.4/site-packages"))

# Switch to the directory of your project. (Optional.)
sys.path.insert(1, expanduser('~/django_apps'))
os.chdir(expanduser('~/django_apps'))

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "jaredforsyth.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
