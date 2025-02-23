# Frobarn/frobarnapp/settings/__init__.py
import os

environment = os.getenv('DJANGO_ENV', 'dev')

if environment == 'prod':
    from .prod import *
elif environment == 'test':
    from .test import *
else:
    from .dev import *