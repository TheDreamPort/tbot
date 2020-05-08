"""
Django settings for rest_api_django project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
import datetime
import psutil
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z2430z_m!17^qtf*)&630vt7kxtborftzwve)q7uwr^=ipr#x0'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


IS_PRODUCTION = False

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['daphne', 'localhost', '127.0.0.1', '::1']
UI_DOMAIN = os.environ.get('UI_DOMAIN_NAME') or 'localhost'
ALLOWED_HOSTS.append(UI_DOMAIN)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'modelclone',
    'django_celery_results',
    'django_celery_beat',
    'knox',
    'channels',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'constance',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# We should disable this for production
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'rest_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'rest_api.wsgi.application'
ASGI_APPLICATION = 'rest_api.routing.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute'
    },
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

"""
Only show admin-style DRF interface if DEBUG is true
"""
if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
            'rest_framework.renderers.BrowsableAPIRenderer')



# Set the default token expiration to 1 day instead of the default 10 hours.
# We will want to shorten this further and pair it with allowing continued use
# when session remains active.
REST_KNOX = {
    'TOKEN_TTL': datetime.timedelta(days=1),
    'USER_SERIALIZER': 'packet_parser.serializers.UserSerializer',
}

# Celery Settings
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://admin:admin@localhost:5672//')
CELERY_BACKEND_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://')

# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
CELERY_BROKER_HEARTBEAT = 30
# if not CELERY_BROKER_URL.endswith(str(CELERY_BROKER_HEARTBEAT)):
#    CELERY_BROKER_URL += '?heartbeat=%d' % CELERY_BROKER_HEARTBEAT

# CELERY_BROKER_POOL_LIMIT = 1  # TODO: review this setting
CELERY_BROKER_CONNECTION_TIMEOUT = 10  # TODO: review this setting

# CELERY_TASK_DEFAULT_QUEUE = 'default'  # TODO: review this setting
CELERY_RESULT_BACKEND = 'django-db'

CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['application/json']

CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000  # TODO: review this setting
CELERY_WORKER_MAX_MEMORY_PER_CHILD = 350000  # 350 MB (value is in KB)

# Scale worker pool up and down based on the following CPU load thresholds
CELERY_WORKER_AUTOSCALER = 'rest_api.autoscaler.MinnowAutoScaler'
MINNOW_AUTOSCALER_MIN_LOAD = 0.50    # Scale up if CPU load is lower than this number
MINNOW_AUTOSCALER_MAX_LOAD = 0.75    # Scale down if CPU load is higher than this number

BEAT_OS_MAINTENANCE_DELAY = 3600.0 # Every two seconds, do OS maintenance things
CELERY_BEAT_SCHEDULE = {
    'check_disk_usage': {
        'task': 'packet_parser.scheduler.disk_usage',
        'schedule': BEAT_OS_MAINTENANCE_DELAY,
    },
    'check_cpu_usage': {
        'task': 'packet_parser.scheduler.cpu_usage',
        'schedule': BEAT_OS_MAINTENANCE_DELAY,
    },
    'appliance-sysinfo': {
        'task': 'integration.metrics.save_sysinfo',
        'schedule': 25,
    },    
    'heartbeat': {
        'task': 'integration.tasks.heartbeat',
        'schedule': 45,
    },
    'send_data': {
        'task': 'integration.tasks.send_data',
        'schedule': 45,
    },
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     os.environ.get('POSTGRES_DB_ENV_POSTGRES_DB') or 'tbot',
        'USER':     os.environ.get('POSTGRES_USER') or 'scott',
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD') or 'MisiMisi!!',
        'HOST':     os.environ.get('POSTGRES_HOST') or 'tbot_postgres',
        'PORT':     os.environ.get('POSTGRES_DB_PORT_5432_TCP_PORT') or '5432',
    },
}

if 'makemigrations' in sys.argv or 'squashmigrations' in sys.argv or 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ.get('REDIS_HOST') or 'redis', 6379)],
            "capacity": 4*4096,
            "expiry": 300,
        },
        # "ROUTING": "rest_api.routing.channel_routing",
    },
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        'token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'You must include "token" in the value: "token abc123000..."'
        },
    },
    'USE_SESSION_AUTH': False,
    'SUPPORTED_SUBMIT_METHODS': ['get', 'post', 'put', 'delete', 'patch', 'options'],
    'VALIDATOR_URL': None,
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REDIS_DATABASE_CHANNELS = 0
REDIS_DATABASE_TASK_UPDATE_ORDERING = 1
REDIS_DATABASE_ANALYZE_MINIMUM = 5
REDIS_DATABASE_ANALYZE_MAXIMUM = 15  # This is limited by a configuration option in Redis: https://github.com/antirez/redis/blob/3.2.11/redis.conf#L178


########################################
# Django-Constance Settings
# Allows for dynamic updating of django settings
########################################
CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'
CONSTANCE_REDIS_CONNECTION = {
    'host': os.environ.get('REDIS_HOST') or 'redis',
    'port': 6379,
    'db': 0,
}

CONSTANCE_ADDITIONAL_FIELDS = {
    'interface_select': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': [ (x,x) for x in psutil.net_if_addrs().keys()],
    }],
}

CONSTANCE_CONFIG = {
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N  = True
USE_L10N  = True
USE_TZ    = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = '/opt/rest_api/public/staticfiles'
STATIC_URL = '/static/'
