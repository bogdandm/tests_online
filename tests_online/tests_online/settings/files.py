import os

from .core import BASE_PATH

ROOT_URLCONF = 'tests_online.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_PATH / "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', str((BASE_PATH / '..' / 'static').resolve()))
STATICFILES_DIRS = (str(BASE_PATH / "static"),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('MEDIA', str((BASE_PATH / '..' / 'media').resolve()))
FILE_UPLOAD_PERMISSIONS = 0o644
