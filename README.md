Pour lancer le projet et voir les reéultats
creation de env
Si vous êtes suus Linux:
    virtualenv env
Si vous êtes suus Linux:
    python3 -m venv env

Activation de venv:
    source env/bin/activate

Ensuite il vous faut installer les packages de python:
    cd facelook/app
    pip install -r app/requirements.txt

Ensuite vous créer la basse de données en fisant:
    cd RS
    python3 manage.py migrate

Vous pouver créer un admin pour gérer les données dans la base de données en fisant:
    python3 manage.py createsuperuser
        Il va vous demander un nom, email et un mot de passse

Finalement, pour lancer le serveur:
    Dans facelook/app/RS, vous faites python3 manage.py runserver

Pour vois l'interface des admin:
    localhost:8000/admin
    Login, mdp : Les info que vous avez créer

Pour voir le rendu final
    localhost:8000
