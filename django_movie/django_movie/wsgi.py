"""
WSGI config for django_movie project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_movie.settings')

call_command('makemigrations')
call_command('migrate')
call_command('createsuperuser', interactive=False, username='admin', email='admin@example.com', password='admin')


application = get_wsgi_application()
