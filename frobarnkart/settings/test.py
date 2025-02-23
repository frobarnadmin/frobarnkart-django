# Frobarn/frobarnapp/settings/test.py

from .base import *

DEBUG = False
ALLOWED_HOSTS = ['test.frobarn.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',
    }
}