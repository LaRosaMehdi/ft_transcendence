"""
Django settings for transcendence project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-07cym*_bkdj0xcofg@!golagfl%t!xic_7gbkxyrervni=+v_x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'sslserver',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blockchain',
    'users',
    'aouth',
    'games',
    'tournaments',
    'matchmaking',
    'smtp',
    'rest_framework',
    # 'channels',
	
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False, 
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'aouth.views.aouth.AouthLogoutAutoMiddleware',
    # 'aouth.views.twofactor.TwoFactorUnverifiedUsersAutoDeleteMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'blockchain', 'templates', 'spa'),
            os.path.join(BASE_DIR, 'aouth', 'templates', 'spa'),
            os.path.join(BASE_DIR, 'tournaments', 'templates', 'spa'),
            os.path.join(BASE_DIR, 'users', 'templates', 'spa'),
            os.path.join(BASE_DIR, 'marchmaking', 'templates', 'spa'),
            os.path.join(BASE_DIR, 'games', 'templates', 'spa'),
            os.path.join(BASE_DIR, 'tournaments', 'templates'),  # Add the directory path here
            os.path.join(BASE_DIR, 'aouth', 'templates'),
            os.path.join(BASE_DIR, 'users', 'templates'),
            os.path.join(BASE_DIR, 'matchmaking', 'templates'),
            os.path.join(BASE_DIR, 'games', 'templates'),
        ],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'ft_transcendence_database'),
        'USER': os.environ.get('DB_USER', 'mehdi'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'melody'),
        'HOST': os.environ.get('DB_HOST', 'ft_transcendence_database'),
        'PORT': os.environ.get('DB_PORT', '5432'),
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

STATICFILES_DIRS = [
    BASE_DIR / "backend/static",
    BASE_DIR / "tournaments/static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGGING
# -------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',  # Increase Django's log level to reduce verbosity
            'propagate': False,  # Prevents double logging in console
        },
        'django.db.backends': {
            'level': 'INFO',  # Reduce the output of database-related logs
            'handlers': ['console'],
            'propagate': False,
        },
        'users': {  # Your app
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'smtp': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'matchmaking': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'games': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'aouth': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'tournaments': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'matchmaking': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'blockchain': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# AUTHENTICATION
# --------------

AUTHENTICATION_BACKENDS = [
    'aouth.views.aouth.AouthUser',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'users.User'

# CSRF
# ----

SESSION_COOKIE_SECURE = True 
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# HSTS
# ----

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SSL
# ---

SECURE_SSL_REDIRECT = True

# MEDIA
# -----

MEDIA_URL = '/users/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 42 OAUTH REGISTRATION
# ---------------------

OAUTH_REGISTER_CLIENT_ID = 'u-s4t2ud-466be83f43b8d3d0ea71b9efc1a9d830027b84b1f2194622888816049e4afc65'
OAUTH_REGISTER_CLIENT_SECRET = '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'
OAUTH_REGISTER_REDIRECT_URI = 'https://localhost:8080/aouth/aouth_callback_register/'

# 42 OAUTH LOGIN
# --------------

AOUTH_LOGIN_CLIENT_ID =  'u-s4t2ud-cecd1a52c9d51af27bc2daeefe882eda5dd05f725f7c6207b551e44720c37969'
OAUTH_LOGIN_CLIENT_SECRET = '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'
AOUTH_LOGIN_REDIRECT_URI = 'https://localhost:8080/aouth/aouth_callback_login/'
