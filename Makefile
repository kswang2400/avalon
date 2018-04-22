clean:
	find . -name \*.cache -delete
	find . -name \*.coverage -delete
	find . -name \*.pyc -delete
	find . -name \__pycache__ -delete

runserver:
	uwsgi --ini webapp/uwsgi_ini/kwang.ini

test:
	cd webapp
	pytest --cov=game