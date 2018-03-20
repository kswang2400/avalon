
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
sudo lsof -i:80


# TODO
psql --u postgres
```

nginx.conf

on mac:
    `/usr/local/etc/nginx/nginx.conf`
    `sudo nginx`

on linux:
    `/etc/nginx/nginx.conf`
    `sudo service nginx start|stop|restart`