
Create an environment

python3 -m venv virtual
. virtual/bin/activate


Install the requirements

pip install -U pip
pip install Flask python-dateutil
pip install flask-sqlalchemy mysqlclient
pip install flask-bcrypt
pip install flask-login

Run the app
export FLASK_APP=ticket
export FLASK_ENV=development
flask run

