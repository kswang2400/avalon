clean:
	find . -name \*.cache -delete
	find . -name \*.coverage -delete
	find . -name \*.pyc -delete

runserver:
	uwsgi --ini uwsgi_ini/kwang.ini

test:
	cd webapp; pytest --cov=game