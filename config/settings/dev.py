from .base import *

DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
