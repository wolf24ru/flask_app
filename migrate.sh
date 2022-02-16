export FLASK_APP=migrate.py
flask db init
flask db migrate
flask db upgrade