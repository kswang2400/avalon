[![Build Status](https://travis-ci.org/kswang2400/avalon.svg?branch=master)](https://travis-ci.org/kswang2400/avalon)

[play some avalon!](http://34.212.31.133/)



```
# testing
pytest --cov=game

# virtualenv
mkvirtualenv --python=/usr/bin/python3 avalon
workon avalon
virtualenv -p python3 avalon
source /home/ec2-user/venv/avalon/bin/activate
source /Users/kwang/.virtualenvs/avalon/bin/activate

# python
pip install -r requirements.txt
python manage.py runserver
python manage.py shell

# nginx
nginx -c /usr/local/etc/nginx/nginx.conf
nginx -s start|restart|stop
lsof -i:80
/usr/local/var/run/nginx.pid

# postgres
sudo -u postgres createuser admin
sudo -u postgres createdb avalon
sudo -u postgres psql
psql -U admin avalon
sudo vim /var/lib/pgsql9/data/pg_hba.conf

# KW: this might be bad, works but revisit
host    all             all             0.0.0.0/0               trust

sudo vim /var/lib/pgsql9/data/postgresql.conf

# nginx.conf
on mac:
    /usr/local/etc/nginx/nginx.conf
    nginx -h|-c|-s

on linux:
    /etc/nginx/nginx.conf
    service nginx start|stop|restart

# install nginx on your local server
on mac:
    brew install nginx
    cp nginx.conf /usr/local/etc/nginx/nginx.conf
    sudo nginx

on linux:
    sudo yum install nginx
```