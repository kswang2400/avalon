#!/bin/bash

BRANCH="$1"
if [[ $BRANCH = "" ]]
then
    BRANCH="master"
fi

echo "starting deploy of branch $BRANCH"

# preamble
sudo service nginx stop
touch /tmp/avalon_uwsgi.pid
uwsgi --stop /tmp/avalon_uwsgi.pid
source /home/ec2-user/venv/avalon/bin/activate

# update codebase
# KW: TODO status checks
cd /home/ec2-user/avalon_game/webapp
git stash
git checkout $BRANCH
git fetch
git merge origin master

# migrate
# KW: TODO better granularity here, migrations are hard
# KW: TODO uncomment this when we actually use a real db
# source env.sh # KW: NOQA wrong dir but need to set this for db
# python manage.py makemigrations
# python manage.py migrate


# run uwsgi
# KW: TODO set up uwsgi emperor for zero downtime
uwsgi="uwsgi --ini uwsgi_ini/prod.ini"
nginx="sudo service nginx start"

$nginx & $uwsgi