#!/bin/bash

# preamble
sudo service nginx stop

# update codebase
# KW: TODO status checks
cd /home/ec2-user/avalon_game/webapp
git stash
git checkout master
git fetch
git merge origin master

# run uwsgi
# KW: TODO set up uwsgi emperor for zero downtime
uwsgi --ini prod.ini
sudo service nginx start