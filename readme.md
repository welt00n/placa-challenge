# Plaza Software Engineer Challenge
## How to run
In a Python >= 3.10 enviroment, install requirements.txt, run migrations and run the development server.
For example, in Ubuntu 20.04:
``` bash
python3 -m virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then go to the interview page at '/interview' to have your job interview.

## Admin
To check the db you may use the admin page at '/admin'. To do so you can use a superuser. Create one using the command below:
```
python manage.py createsuperuser
```