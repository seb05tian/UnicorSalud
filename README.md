--Crear entorno virtual
python -m virtualenv venv

--Iniciar entorno virtual
venv\Scripts\activate  

O 'F1' y select interpreter, seleccionas el venv y reinicias el cmd


--Instalamos Django en el entorno vitual
pip install django

--Iniciar proyecto DJANGO
django-admin startproject myproject .

--Crear apps
python manage.py startapp nombre_app

--Ejecutar proyecto
python manage.py runserver

--Guardar dependencias en archivo
pip freeze > requirements.txt

--Instalar archivos que esten en el requirements
pip install -r requirements.txt

--DATABASE POSTGRES EN SETTIGNS
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydatabase",
        "USER": "mydatabaseuser",
        "PASSWORD": "mypassword",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
