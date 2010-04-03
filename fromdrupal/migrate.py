#!/usr/bin/env python2.6

import imp
from django.core.management import setup_environ
from django.core import serializers

def export_mysql(dbname, dbuser, dbpass, outnodes="nodes.json", outurls="urls.json"):
    settings = imp.new_module('fromdrupal.settings')
    settings.DATABASE_ENGINE = 'mysql'
    settings.DATABASE_NAME = dbname
    settings.DATABASE_USER = dbuser
    settings.DATABASE_PASSWORD = dbpass

    setup_environ(settings)

    from fromdrupal.models import NodeRevisions, UrlAlias

    out = open(outnodes, 'w')
    serializers.serialize('json', NodeRevisions.objects.all(), stream=out)
    out.close()
    out = open(outurls, 'w')
    serializers.serialize('json', UrlAlias.objects.all(), stream=out)
    out.close()

'''
from django.core.management.commands.inspectdb import Command
import sys
import StringIO
s = StringIO.StringIO()
sys.stdout = s

Command().handle_noargs()

databases = s.getvalue()
sys.stdout = sys.__stdout__
'''

from fromdrupal.models import NodeRevisions, UrlAlias

from django.core import serializers

def export_data():
    out = open('nodes.json','w')
    serializers.serialize('json', NodeRevisions.objects.all(), stream=out)
    out.close()
    out = open('urls.json','w')
    serializers.serialize('json', UrlAlias.objects.all(), stream=out)
    out.close()

if __name__=='__main__':
    export_data()

# vim: et sw=4 sts=4
