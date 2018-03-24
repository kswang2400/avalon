# preamble
deactivate
sudo service nginx stop

# update version control
cd /home/ec2-user/avalon_game/webapp
git stash
git checkout master
git fetch
git merge origin master

# virtualenv
source /home/ec2-user/venv/avalon/bin/activate

# run uwsgi
# KW: TODO set up uwsgi emperor for zero downtime
uwsgi --ini prod.ini
sudo service nginx start