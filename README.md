# Projet SoftDesk

### SoftDesk est une API RESTFUL permettant de remonter et suivre des problèmes techniques.

### Développer avec Django REST

Testé avec [postman](https://learning.postman.com/docs/introduction/overview/)

## Cloner le projet

```bash
$ git clone https://github.com/Jogodev/SoftDesk.git
$ cd softdesk
```

### Créer l'environnement virtuel

```bash
$ python -m venv env
```

### Activer l'environnement virtuel

#### Windows

```bash
$ . env\scripts\activate
```

#### Mac

```bash
$ source env\scripts\activate
```

#### linux

```bash
$ source env\scripts\activate
```

### Installer les paquets

```bash
$ pip install -r requirements.txt
```

### Se déplacer dans le second dossier softdesk

```bash
$ cd softdesk
```

### Lancer la commande

```bash
$ python manage.py runserver
```

### Base de données

#### Utilisateurs disponibles sur la base de données fournie

| **Username** | **Password** |
| ------------ | ------------ |
| Joey         | 12345        |
| Ali          | 12345        |
| Frank        | 12345        |

#### Si vous utilisez une nouvelle base de données lancer les migrations

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### Documentation

Toutes la documentation sur les différents endpoints est disponible sur [API DRF](https://documenter.getpostman.com/view/17405214/2s9Ykoc1Q9)
