#!/usr/bin/env python

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    raise
    sys.exit(1)

from django.core.management import setup_environ

setup_environ(settings)

from basic.blog.models import Post
import string

posts = list(Post.objects.all())

for i,post in enumerate(posts):
    print '%d) %s' % (i, post.title)

num = raw_input('post num:')
if not num.isdigit():
    print 'fail:',num
num = int(num)

import tempfile
import subprocess

post = posts[num]

filename = tempfile.mktemp('.rst')
open(filename,'w').write(post.body)

import sys

p = subprocess.Popen(('vim',filename),stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
p.wait()

text = open(filename).read()
if raw_input('post?').lower() in ('y','yes'):
    post.body = text
    post.save()
else:
    print 'junking'




# vim: et sw=4 sts=4
