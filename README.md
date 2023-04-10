# glados_api

Rebuilt the Glados Domotics API (Flask) in Django : 
https://github.com/glados-domotics/api
)

# glados-api

## Project setup
To use the project correctly, it is necessary to install all its dependencies found in `requirements.txt`.

Here are the recommanded steps to do so : 

Create a virtual environnement 
```
python -m venv NAME_OF_ENV
```

Source from the environnement
```
source NAME_OF_ENV/PATH/TO/activate
```

Install libraries 
```
pip install -r requirements.txt
```

You also need to setup the database, use this command :
```
python manage.py migrate
```

### Testing and running project 

To launch the project's tests, use this command :
```
python manage.py test
```

To launch the project on a development environment, use this command :
```
python manage.py runserver
```
