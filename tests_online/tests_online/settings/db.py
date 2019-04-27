import os

from .core import BASE_PATH

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'tests_online'),
        'USER': os.environ.get('POSTGRES_USER', 'tests_online'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
} if 'POSTGRES_DB' in os.environ else {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_PATH / ".." / "db.sqlite3"),
    }
}