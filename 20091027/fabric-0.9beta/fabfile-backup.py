#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement # needed for python 2.5
from fabric.api import *

from time import *
lt = localtime()

env.hosts = ['domain.cpm']
env.postgres_bin = '/usr/local/pgsql/bin'
env.backup_dir = '/home/user/backup'
env.backup_dir_local = '/Users/user/Backups'
env.date = strftime("%Y-%m-%d", lt)

def backup():
    """
    Start the backup of databases and files, then copy gziped tars to my
    local harddrive.
    """
    require('hosts')
    require('backup_dir')
    require('backup_dir_local')
    require('date')
    backup_postgres()
    backup_mysql()
    backup_files()
    get_files()
	
def backup_postgres():
    """
    Create a database dump of my PostgreSQL database
    """
    with cd('%(backup_dir)s' % env):
        with cd('db'):
            run('/usr/local/pgsql/bin/pg_dump database_postgres -U user > %(date)s-database_postgres.sql' % env, pty=True)
            run('gzip -f %(date)s-database_postgres.sql' % env, pty=True)

def backup_mysql():
    """
    Create a database dump of my MySQL databases
    """
    with cd('%(backup_dir)s' % env):
        with cd('db'):
            run('mysqldump --user=user --password="secret" --add-drop-table database_mysql --opt -h localhost > %(date)s-database_mysql.sql' % env, pty=True)
            run('gzip -f %(date)s-database_mysql.sql' % env, pty=True)

def backup_files():
    """
    Create a backup of all files on the server
    """
    with cd('%(backup_dir)s' % env):
        with cd('files'):
            run('tar -czvpf %(date)s-backup_django.tgz /home/user/django/ --exclude=cache' % env, pty=True)
            run('tar -czvpf %(date)s-backup_home.tgz /home/user/ --exclude=django --exclude=cache --exclude=logs --exclude=backup --exclude=src --exclude=transfer' % env, pty=True)
    
def get_files():
    get('%(backup_dir)s/db/%(date)s-database_postgres.sql.gz' % env,'%(backup_dir_local)s/Datenbanken/' % env)
    get('%(backup_dir)s/db/%(date)s-database_mysql.sql.gz' % env,'%(backup_dir_local)s/Datenbanken/' % env)
    get('%(backup_dir)s/files/%(date)s-backup_home.tgz' % env,'%(backup_dir_local)s/Websites/' % env)
    get('%(backup_dir)s/files/%(date)s-backup_django.tgz' % env,'%(backup_dir_local)s/Websites/' % env)
    local('cd %(backup_dir_local)s/Websites/; mv %(date)s-backup_webapps.tgz backup_webapps.tgz; mv %(date)s-backup_home.tgz backup_home.tgz' % env)
