# django-api

## Passos

### Passo 1

#### Criar o ambiente do projeto

```bash
python -m venv venv
source venv/bin/activate
```

#### Instalar Django + DRF

```bash
pip install django djangorestframework
```
### Passo 2

#### Criar o projeto Django

```bash
django-admin startproject config .
```

#### Criar os apps

```bash
python manage.py startapp core
python manage.py startapp users
python manage.py startapp tasks
```

Depois cria manualmente a pasta config/settings e divide o settings.py.

### Passo 3

#### Crie o superusuário (conta admin)

```bash
python manage.py createsuperuser
```

#### Iniciar o servidor

```bash
python manage.py runserver
```