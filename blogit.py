#!/usr/bin/env python2.6

import tempfile
import subprocess
import string
import sys
import time
import os

import settings # Assumed to be in the same directory.
from django.core.management import setup_environ
setup_environ(settings)

from django.db.models.loading import cache
cache._populate()

EDITOR = 'vim'

def pick(lst, name=None):
    dct = {}
    for i,item in lst:
        dct[str(i)] = item
        print '%s) %s' % (i, item)
    while True:
        inp = raw_input('pick one: ')
        if inp in dct:
            return dct[inp]
        elif not inp:
            return None

def pick_app():
    app = pick(enumerate(cache.app_models.keys()))
    if not app:
        sys.exit(0)
    return app

def get_app(app):
    if app not in cache.app_models:
        print 'Invalid app'
        return pick_app()
    return cache.app_models[app]

def pick_model(app):
    model = pick(enumerate(app.keys()))
    if not model:
        sys.exit(0)
    return app[model]

def get_model(app, model):
    if not model in app:
        print 'Invalid model'
        return pick_model(app)
    return app[model]

def get_object(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return pick_object(model)

def pick_object(model):
    obj = pick(enumerate(obj for obj in model.objects.all()))
    if not obj:
        sys.exit(0)
    return obj

def search_object(model, text):
    try:
        field, kwds = text.split(':', 1)
        return model.objects.get(**{field+'__contains':kwds})
    except model.MultipleObjectsReturned:
        print 'search is not specific enough'
    except model.DoesNotExist:
        print 'no objects found'
    return pick_object(model)

def pick_field(object):
    field = pick(enumerate(vars(object).keys()))
    if not field:
        sys.exit(0)
    return field

from reversion.revisions import revision
import reversion

def edit_object(object, field, format='rest'):
    revision.start()
    ext = {'rest':'rst','mdown':'md','txtile':'txt','html':'html','plain':'txt'}

    filename = tempfile.mktemp('.' + ext[format])
    original = getattr(object, field)
    open(filename,'w').write(original)
    mtime = os.path.getmtime(filename)

    p = subprocess.Popen((EDITOR, filename), stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    while p.poll() is None:
        time.sleep(.2)
        ntime = os.path.getmtime(filename)
        if ntime > mtime:
            mtime = ntime
            text = open(filename).read()
            if text == original:
                continue
            setattr(object, field, text)
            object.save()

    text = open(filename).read()
    if text == original:
        return False
    setattr(object, field, text)
    object.save()
    revision.end()

import optparse
def get_options():
    p = optparse.OptionParser('usage: %prog [app] [model] [field]')
    p.add_option('-a', '--app', dest='app', help='django application')
    p.add_option('-m', '--model', dest='model', help='specify which model to edit')
    p.add_option('-f', '--field', dest='field', help='specify which field to edit')
    p.add_option('-n', '--num', dest='num', type='int', help='specify the object id to edit')
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
    reversion.register(model)
    if options.num:
        object = get_object(model, options.num)
    elif options.search:
        object = search_object(model, options.search)
    else:
        object = pick_object(model)

    field = options.field
    if not field:
        field = pick_field(object)
        
    edit_object(object, field)

if __name__=='__main__':
    main()

# vim: et sw=4 sts=4
