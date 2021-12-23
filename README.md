# For installing project environment

## Run following scripts in your terminal:

**Create virtual env:**
```
python -m venv env
```

**Activate virtual env:**
```
env\Scripts\activate
```

*(option) If you want to deactivate:*
```
env\Scripts\deactivate
```

**Install some requirements:**
```
pip install -r requirements.txt
```

@for more information: [link](https://www.tabnine.com/blog/how-to-create-django-projects-in-pycharm-community-edition/)

# Migration
**Make migration file on changes:**
```
python manage.py makemigrations
```

**Make migration file on changes:**
```
python manage.py migrate
```

**Creating a empty migration file manually:**
```
python manage.py makemigrations <app> --empty
```

#Django

**Creating a new app (module):**
```
python manage.py startapp *module_name*
```

**Creating a superuser:**
```
python manage.py createsuperuser
```

# Dump notes

**Create new app:**
```
python manage.py startapp hello
```
