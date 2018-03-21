
```
# virtualenv
mkvirtualenv --python=/usr/bin/python3 avalon
workon avalon
virtualenv -p python3 avalon

# python
pip install -r requirements.txt
python manage.py runserver
python manage.py shell

# nginx
nginx -c /usr/local/etc/nginx/nginx.conf
nginx -s start|restart|stop
lsof -i:80
/usr/local/var/run/nginx.pid


# TODO
psql --u postgres
```

nginx.conf

on mac:
    `/usr/local/etc/nginx/nginx.conf`
    `nginx -h|-c|-s`

on linux:
    `/etc/nginx/nginx.conf`
    `service nginx start|stop|restart`


# install nginx on your local server
on mac:
```
brew install nginx
cp nginx.conf /usr/local/etc/nginx/nginx.conf
sudo nginx
```