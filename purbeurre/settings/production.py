import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .common import *

ALLOWED_HOSTS = ["165.22.118.210"]

DEBUG = False

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.INFO,  # Send INFOs as events
)

sentry_sdk.init(
    dsn=("https://751878c9886d41ed853ed05124aa3c62@o516111."
         + "ingest.sentry.io/5622155"),
    integrations=[DjangoIntegration(), sentry_logging],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('{levelname} {asctime} {module} '
                       + '{process:d} {thread:d} {message}'),
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

"""
levels: DEBUG < INFO < WARNING < ERROR < CRITICAL
"""
