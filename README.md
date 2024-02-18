Prequisite:
Install postgresql and make user accordingly
Install requirements:
pip install -r requirements.txt
Make migrations:
python manage.py makemigrations
Run migrations:
python manage.py migrate
Run app:
python manage.py runserver
For tests:
python manage.py test