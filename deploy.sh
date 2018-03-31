#!/bin/bash

# preamble
sudo service nginx stop
touch /tmp/avalon_uwsgi.pid
uwsgi --stop /tmp/avalon_uwsgi.pid
source /home/ec2-user/venv/avalon/bin/activate

# update codebase
# KW: TODO status checks
cd /home/ec2-user/avalon_game/webapp
git stash
git checkout master
git fetch
git merge origin master

# run uwsgi
# KW: TODO set up uwsgi emperor for zero downtime
uwsgi="uwsgi --ini uwsgi_ini/prod.ini"
nginx="sudo service nginx start"

$nginx & $uwsgi