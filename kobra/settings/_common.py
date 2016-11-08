# -*- coding: utf-8 -*-
from datetime import timedelta
import warnings

import environ

from sesam import SesamStudentServiceClient

env = environ.Env()
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('kobra')

# https://docs.python.org/3/library/warnings.html#temporarily-suppressing-warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    env.read_env(str(ROOT_DIR.path('.env')))

# This assumes you are using a reverse proxy that will never let through HTTP
# requests with spoofed headers.
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'opbeat.contrib.django',  # Error reporting
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'social.apps.django_app.default',
    'rest_social_auth',

    'kobra'
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'OPTIONS': {
            "CLIENT_CLASS": 'django_redis.client.DefaultClient',
        }
    }
}

# todo: change this to use the new MIDDLEWARE setting when Opbeat is updated to
# work with it
MIDDLEWARE_CLASSES = [
    # OpbeatAPMMiddleware should always be first to give accurate performance
    # measurements
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'opbeat.contrib.django.middleware.Opbeat404CatchMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR.path('webclient').path('build').path('templates'))],
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

AUTHENTICATION_BACKENDS = [
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'social_liu.LiuBackend'
]
AUTH_USER_MODEL = 'kobra.User'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'kobra.api.v1.permissions.KobraObjectPermissions',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}
JWT_AUTH = {
    'JWT_ALGORITHM': 'HS512',
    'JWT_ALLOW_REFRESH': True,
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'kobra.api.v1.serializers.jwt_response_payload_handler'
}

# fullname is the identifier used by python-social-auth.
SOCIAL_AUTH_USER_FIELDS = ['email', 'fullname']
SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',

    # Associates the current social details with another user account with
    # a similar email address.
    'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associates the social account with the user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details',
    'social.pipeline.debug.debug',
)

SOCIAL_AUTH_LIU_HOST = env.str('ADFS_HOST', 'fs.liu.se')
SOCIAL_AUTH_LIU_KEY = env.str('ADFS_CLIENT_ID', '')
SOCIAL_AUTH_LIU_SCOPE = ['https://kobra.karservice.se']

ROOT_URLCONF = 'kobra.urls'
WSGI_APPLICATION = 'kobra.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = str(ROOT_DIR.path('collected-static'))
STATICFILES_DIRS = (
    str(APPS_DIR.path('webclient').path('build').path('static')),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    # This is THE log config. This makes sense since we use a root logger.
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(name)s %(message)s'
        },
        # Used by the Django development server. Included from django.utils.log.
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        # Used by the Django development server. Included from django.utils.log.
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'opbeat': {
            'level': 'WARNING',
            'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
        }
    },
    'loggers': {
        # Log everything of level WARNING or above to the console and to opbeat.
        # This is to keep the log config as simple and as predictable as
        # possible.
        None: {
            'level': 'WARNING',
            'handlers': ['console', 'opbeat']
        },
        # Exceptions to the above rule go here. Use propagate=False to prevent
        # the root logger to also swallow the event.

        # Used by the Django development server. Included from django.utils.log.
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Backend Opbeat config
OPBEAT_BACKEND = OPBEAT = {
    'ORGANIZATION_ID': env.str('OPBEAT_BACKEND_ORGANIZATION_ID', ''),
    'APP_ID': env.str('OPBEAT_BACKEND_APP_ID', ''),
    'SECRET_TOKEN': env.str('OPBEAT_BACKEND_SECRET_TOKEN', ''),
    'TRANSACTIONS_IGNORE_PATTERNS': [
        'views.health_view'
    ],
    'DEBUG': True
}

# Frontend Opbeat config
OPBEAT_FRONTEND = {
    'ORGANIZATION_ID': env.str('OPBEAT_FRONTEND_ORGANIZATION_ID', ''),
    'APP_ID': env.str('OPBEAT_FRONTEND_APP_ID', ''),
    'SECRET_TOKEN': env.str('OPBEAT_FRONTEND_SECRET_TOKEN', ''),
}

SESAM_USERNAME = env.str('SESAM_USERNAME', '')
SESAM_PASSWORD = env.str('SESAM_PASSWORD', '')
# To utilize the connection pooling in the SesamStudentServiceClient, we
# instantiate the client here and make it available as a singleton.
# todo: investigate better ways of achieving this.
SESAM_STUDENT_SERVICE_CLIENT = SesamStudentServiceClient(
    SESAM_USERNAME, SESAM_PASSWORD)
# Specifies how old the data from Sesam can be before an update is forced.
SESAM_DATA_AGE_THRESHOLD = timedelta(
    seconds=env.int('SESAM_DATA_AGE_THRESHOLD', 6*60*60))

ORACLE_USERNAME = env.str('ORACLE_USERNAME', '')
ORACLE_PASSWORD = env.str('ORACLE_PASSWORD', '')
ORACLE_HOST = env.str('ORACLE_HOST', '')
ORACLE_PORT = env.int('ORACLE_PORT', 1521)
