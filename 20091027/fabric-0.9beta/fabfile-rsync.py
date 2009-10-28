#!/usr/bin/python
# -*- coding: utf-8 -*-

from fabric.api import env, rsync_project

env.hosts = ['domain.com']
env.path = '/home/user/project/'

def sync():
    """
    Synchronize project with webserver
    """
    rsync_project(env.path, delete=True, exclude=['*.pyc','*.py','.DS_Store'])