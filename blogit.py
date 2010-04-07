#!/usr/bin/env python

import tempfile
import subprocess
import string
import sys
import time

import settings # Assumed to be in the same directory.
from django.core.management import setup_environ
setup_environ(settings)

from basic.blog.models import Post

EDITOR = 'vim'

def pick_object(model):
    objects = list(model.objects.all())

    for i,object in enumerate(objects):
        print '%d) %s' % (i, object.title)

    num = raw_input('item num:')
    if not num or not num.isdigit():
        return False
    num = int(num)
    object = objects[num]
    return object

from reversion.revisions import revision

@revision.create_on_success
def edit_object(object, field, format='rest'):
    ext = {'rest':'rst','mdown':'md','txtile':'txt','html':'html','plain':'txt'}

    filename = tempfile.mktemp('.' + ext[format])
    original = getattr(object, field)
    open(filename,'w').write(original)

    p = subprocess.Popen((EDITOR, filename), stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    p.wait()

    text = open(filename).read()
    if text == original:
        return False
    setattr(object, field, text)
    object.save()

import optparse
def get_options():
    p = optparse.OptionParser('usage: %prog [app] [model] [field]')
    p.add_option('-a', '--app', dest='app', help='django application')
    p.add_option('-m', '--model', dest='model', help='specify which model to edit')
    p.add_option('-f', '--field', dest='field', help='specify which field to edit')
    p.add_option('-n', '--num', dest='num', help='specify the object id to edit')
    p.add_option('--search', dest='search', help='search objects for "field:text"')

    options, pos = p.parse_args()
    if len(pos):
        raise Exception,'no positional arguments accepted: %s' % pos
    return options

def main():
    options = get_options()
    if not options.app:
        app = pick_app()
    else:
        app = get_app(options.app)
    if not options.model:
        model = pick_model(app)
    else:
        model = get_model(app, options.model)
    if not options.num:
        
    obj = pick_object(model)
    edit_object


# vim: et sw=4 sts=4
