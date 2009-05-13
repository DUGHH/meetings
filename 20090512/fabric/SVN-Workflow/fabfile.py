#!/usr/bin/python
# -*- coding: utf-8 -*-

config.project = 'domain.de' # Name des Projektes
config.project_type = 'websites' # websites, intern, previews, user/username
config.svn_repos = '/server/svn/repos/online' # Pfad zu den Repositorys
config.svn_url = 'svn://server.admin/online' # SVN-URL
config.svn_passwd = '/server/svn/repos/online/passwd' # Pfad zur passwd
config.working_dir = '$HOME/Projekte/Kunden' # Pfad zum lokalen Arbeitsordner
config.fab_hosts = ['server.admin'] # Host
config.fab_user = 'user'

def create():
    """
    Erzeugt ein leeres Subversion-Repository auf dem Cluster,
    importiert die Standardstruktur und checkt das ganze im Arbeitsverzeichnis
    wieder aus.
    """
    run(
        'cd %(svn_repos)s/%(project_type)s/; \
         mkdir %(project)s; \
         cd %(project)s; \
         svnadmin create --fs-type fsfs .; \
         chmod -R 755 .; \
         chmod -R 777 *; \
         cd conf; \
         echo "[general]" > svnserve.conf; \
         echo "anon-access = read" >> svnserve.conf; \
         echo "auth-access = write" >> svnserve.conf; \
         echo "password-db = %(svn_passwd)s" >> svnserve.conf; \
         echo "realm = %(project)s" >> svnserve.conf;'
    )
    local(
        'mkdir import; \
         cd import; \
         mkdir trunk; \
         mkdir tags; \
         mkdir branches; \
         mkdir trunk/Konzept; \
         mkdir trunk/Layout; \
         mkdir trunk/Preview; \
         mkdir trunk/Screenshots; \
         mkdir trunk/Vorlagen; \
         mkdir trunk/Vorlagen/Fotos; \
         mkdir trunk/Vorlagen/Grafiken; \
         mkdir trunk/Vorlagen/Logos; \
         mkdir trunk/Vorlagen/Texte; \
         mkdir trunk/Website;'
    )
    local(
        'cd import; \
         svn import . %(svn_url)s/%(project_type)s/%(project)s -m "Initial import"; \
         cd ..; \
         rm -rf import/;'
    )
    local(
        'cd %(working_dir)s/; \
         git svn clone -s %(svn_url)s/%(project_type)s/%(project)s'
    )
    local(
        'cd %(working_dir)s/%(project)s; \
         mkdir Konzept; \
         mkdir Layout; \
         mkdir Preview; \
         mkdir Screenshots; \
         mkdir Vorlagen; \
         mkdir Vorlagen/Fotos; \
         mkdir Vorlagen/Grafiken; \
         mkdir Vorlagen/Logos; \
         mkdir Vorlagen/Texte; \
         mkdir Website;'
    )