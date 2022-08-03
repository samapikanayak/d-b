"""
Django settings for dnbadmin project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
# import dotenv
# dotenv.read_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3z1+d2v&x@gj_#3b=yrd2sp3$dlx7_)4%+4j^_b3korca_ir#b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True


CORS_ORIGIN_WHITELIST = (
    str(os.environ.get('CORS_ORIGIN_WHITELIST')),
)

ALLOWED_HOSTS = ['localhost', os.environ.get(
    'LOCALHOST'), os.environ.get('DEV_HOST'), os.environ.get('FRONTEND_HOST')]


CSRF_TRUSTED_ORIGINS = [os.environ.get('CSRF_HOST')]


# Application definitiondjango-cors-headers

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'django_db_comments',
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    'party',
    'worker',
    'unitofmeasure',
    'job',
    'store',
    'position',
    'workerschedule',
    'accesscontrol',
    'coverage',
    'depositrule',
    'sellingrule',
    'product', 'taxonomy', 'brand', 'basics', 'globalsettings', 'itempricerule',
    'pos_department',
    'department', 'operators'
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
]

ROOT_URLCONF = 'dnbadmin.urls'

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

WSGI_APPLICATION = 'dnbadmin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_POSTGRES_DB'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'TEST': {
            'NAME': 'mytestdatabase',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.environ.get('ELASTIC_HOST'),
    },
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'file_party': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'party.log',
            'maxBytes': 1048576,  # 20 MB
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_login': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'login_authentication.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_accesscontrol': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'accesscontrol.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_globalsetting': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'globalsetting.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_unitofmeasure': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'unitofmeasure.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_department': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'department.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_workerschedule': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'workerschedule.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_basic': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'basics.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_taxonomy': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'taxonomy.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_position': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'position.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },

        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        }
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True
        },
        'party': {
            'level': 'INFO',
            'handlers': ['file_party'],
            'propagate': True,
        },
        'login_authentication': {
            'level': 'INFO',
            'handlers': ['file_login'],
            'propagate': True,
        },
        'accesscontrol': {
            'level': 'INFO',
            'handlers': ['file_accesscontrol'],
            'propagate': True,
        },
        'globalsettings': {
            'level': 'INFO',
            'handlers': ['file_globalsetting'],
            'propagate': True,
        },
        'unitofmeasure': {
            'level': 'INFO',
            'handlers': ['file_unitofmeasure'],
            'propagate': True,
        },
        'department': {
            'level': 'INFO',
            'handlers': ['file_department'],
            'propagate': True,
        },
        'workerschedule': {
            'level': 'INFO',
            'handlers': ['file_workerschedule'],
            'propagate': True,
        },
        'basics': {
            'level': 'INFO',
            'handlers': ['file_basic'],
            'propagate': True,
        },
        'taxonomy': {
            'level': 'INFO',
            'handlers': ['file_taxonomy'],
            'propagate': True,
        },
        'position': {
            'level': 'INFO',
            'handlers': ['file_position'],
            'propagate': True,
        },
    }
}
