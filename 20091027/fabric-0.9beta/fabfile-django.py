#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement # needed for python 2.5
from fabric.api import env, local, run, require

env.hosts = ['domain.de']
env.path = '/home/user/apache2/bin'
env.project_path = '/home/user/project'
env.memcached_ip = '127.0.0.1'
env.memcached_port = '1234'
env.memcached_size = '20' # in MByte

def deploy():
    "Lokale Änderungen pushen, Änderungen pullen auf server, Server neustarten"
    require('hosts')
    require('path')
    require('project_path')
    local('git push;')
    with ('cd %(project_path)s/' % env):
        run('git pull', pty=True)
        run('delpyc', pty=True)
    restart_server()
    
def stop_server():
    "Apache stoppen"
    run('%(path)s/stop' % env, pty=True)

def start_server():
    "Apache starten"
    run('%(path)s/start' % env, pty=True)

def restart_server():
    "Apache neustarten"
    with cd('%(path)s/' % env):
        run('stop' % pty=True)
        run('start' % pty=True)

def restart_memcached():
    "Memcached neustarten"
    run('kill `pgrep -u $LOGNAME memcached`' % env, pty=True)
    run('/usr/local/bin/memcached -d -l %(memcached_ip)s -m %(memcached_size)s -p %(memcached_port)s' % env, pty=True)
    restart_server()