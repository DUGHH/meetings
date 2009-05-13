#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import *
lt = localtime()

config.fab_hosts = ['server.com'],
config.fab_host = 'server.com',
config.fab_user = 'user',
config.postgres_bin = '/usr/local/pgsql/bin',
config.backup_dir = '/home/user/backup',
config.backup_dir_local = '/Users/user/Archiv/Backups',
config.date = strftime("%Y-%m-%d", lt),

def backup():
    "Erzeugt ein Backup aller Dateien auf dem Server"
    local('echo Backup erzeugen')
    backup_postgres()
    backup_mysql()
    backup_files()
    get_files()
    
def backup_postgres():
    "Erzeugt einen Dump der PostgreSQL-Datenbanken"
    run('/usr/local/pgsql/bin/pg_dump user -U user > %(backup_dir)s/db/%(date)s-user-pg.sql', fail='abort')
    run('gzip -f %(backup_dir)s/db/%(date)s-user-pg.sql')

def backup_mysql():
    "Erzeugt einen Dump der MySQL-Datenbanken"
    run('mysqldump --user=user --password=PW --add-drop-table user --opt -h localhost > %(backup_dir)s/db/%(date)s-user-my.sql', fail='abort')
    run('gzip -f %(backup_dir)s/db/%(date)s-user-my.sql')

def backup_files():
    "Erzeugt Backups aller Dateien auf dem Server"
    run('tar -czvpf %(backup_dir)s/files/%(date)s-backup_files.tgz /home/user/files/ --exclude=cache')
    
def get_files():
    local('scp %(fab_user)s@%(fab_host)s:%(backup_dir)s/db/%(date)s* %(backup_dir_local)s/Datenbanken/')