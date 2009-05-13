#!/usr/bin/python
# -*- coding: utf-8 -*-

config.fab_hosts = ['host.com']
config.fab_user = 'user' # Can also be written in ~/.fabric (fab_user = user)
config.server_path = '/home/user/django/apache2/bin'
config.project_path = '/home/user/django/project'
config.memcached_ip = 'IP'
config.memcached_port = 'PORT'
config.memcached_size = '20' # in MByte

def deploy():
    "Push local changes, pull changes on server, delete compiled files, restart server"
    local('git push;', fail='warn')
    run('cd %(project_path)s/; git pull; delpyc', fail='warn')
    restart_server()
    
def stop_server():
    "Stop Apache"
    run('%(server_path)s/stop', fail='warn')

def start_server():
    "Start Apache"
    run('%(server_path)s/start', fail='warn')

def restart_server():
    "Restart Apache"
    run('%(server_path)s/stop', fail='warn')
    run('%(server_path)s/start', fail='warn')

def restart_memcached():
    "Restart Memcached"
    run('kill `pgrep -u $LOGNAME memcached`', fail='warn')
    run('/usr/local/bin/memcached -d -l %(memcached_ip)s -m %(memcached_size)s -p %(memcached_port)s', fail='warn')
    restart_server()