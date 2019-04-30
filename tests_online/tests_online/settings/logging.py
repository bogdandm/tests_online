from .core import BASE_PATH, DEBUG
import os


LOG_DIR = BASE_PATH.parent /  os.environ.get('LOG_DIR', 'logs_tmp')
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'django': {
            'format': '[%(asctime)s:%(levelname)s:%(processName)s:%(module)s] <%(pathname)s:%(lineno)d> %(message)s'
        },
        'task': {
            'format': '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'django',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': str(LOG_DIR / 'django.log'),
            'formatter': 'django',
        },
        'task_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'task'
        },
        'task_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'tasks.log'),
            'formatter': 'task',
            'maxBytes': 1024 * 1024 * 20,  # 20 mb
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO' if DEBUG else 'ERROR',
        },
        'celery.tasks': {
            'handlers': ['task_console', 'task_file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        }
    }
}
