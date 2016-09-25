# -*- coding: utf-8 -*-
from ._common import *

SECRET_KEY = env.str('DJANGO_SECRET_KEY',
                     'Unsafe_development_key._Never_use_in_production.')
DEBUG = env.bool('DJANGO_DEBUG_MODE', True)

CACHES['default']['LOCATION'] = env.str('DJANGO_REDIS_URL', '')

DATABASES = {
    'default': env.db_url('DJANGO_DATABASE_URL', 'sqlite:///db.sqlite3')
}


REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = [
    'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
]
