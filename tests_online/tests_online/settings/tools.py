import os

from datetime import timedelta

from .core import DEBUG, INSTALLED_APPS, MIDDLEWARE, SECRET_KEY

# Celery

if 'BROKER_URL' in os.environ or 'REDIS_CONNECTION' in os.environ:
    CELERY_BROKER_URL = BROKER_URL = os.environ.get('BROKER_URL', os.environ.get("REDIS_CONNECTION") + "1")
    CELERY_RETRY_TIMEOUT = int(os.environ.get('CELERY_RETRY_TIMEOUT', 30))

# DRF

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Simple JWT

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Swagger

SWAGGER_SETTINGS = {
    'DEFAULT_API_URL': os.environ.get('DEFAULT_API_URL', "https://localhost:8000/api/v1"),
    'DOC_EXPANSION': None,
    'DEEP_LINKING': True,
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        'api_key': {
            'type': 'apiKey',
            'description': 'Bearer <token>',
            'name': 'Authorization',
            'in': 'header',
        }
    },
}

# Debug toolbar

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda x: DEBUG,
    "DISABLE_PANELS": {
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    }
}

__all__ = list(locals().keys())
for k in ('os', 'DEBUG', 'INSTALLED_APPS', 'MIDDLEWARE', 'SECRET_KEY'):
    __all__.remove(k)
