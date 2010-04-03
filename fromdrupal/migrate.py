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

def config():
    p = optparse.OptionParser('usage: %prog [options] command')
    p.add_option('-t','--db-type',dest='db_type',
            help='database type')
    p.add_option('--db',help='database name')
    p.add_option('--user',help='database user')
    p.add_option('--pwd',help='database password')
    #g = optparse.OptionGroup(p, "Export Options")
    p.add_option('--node-file',help='output destination for node revisions',
            default='nodes.json')
    p.add_option('--url-file',help='output destination for urls'
            default='urls.json')
    p.add_option_group(g)
    #g = optparse.OptionGroup(p, "Import Options")
    options, args = p.parse_args
    
    if len(args)!=1 or args[0] not in ('export','import'):
        p.print_help()
        sys.exit(1)


if __name__=='__main__':
    export_data()

# vim: et sw=4 sts=4
