"""
Django settings for bbs project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ip3#-n9mw72woa(ex*73e0b1tmb@1e*o-z=xqw%k@ac)k%ka1^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'post',
    'user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.BlockMiddleware'
]

ROOT_URLCONF = 'bbs.urls'

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

WSGI_APPLICATION = 'bbs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/statics/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "statics"),
]

MEDIA_URL = '/medias/'
MEDIA_ROOT = 'medias'

# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Cache 配置

# 默认配置
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
#     }
# }

# 使用 Redis 做缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",  # 存储引擎
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,
        }
    }
}

# Redis 配置
REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 1,
}

# ==============================================================================
# Wei Bo
WEIBO_APP_KEY = '1310374555'
WEIBO_APP_SECRET = 'e5cf3ddc50d77ba6f038013003c29550'
WEIBO_CALLBACK_URL = 'http://seamile.org/weibo/callback/'

# 第一步的接口
AUTHORIZE_API = 'https://api.weibo.com/oauth2/authorize'
AUTHORIZE_PARAMS = {
    'client_id': WEIBO_APP_KEY,
    'redirect_uri': WEIBO_CALLBACK_URL,
    'response_type': 'code',
}

# 第二部接口
ACCESS_TOKEN_API = 'https://api.weibo.com/oauth2/access_token'
ACCESS_TOKEN_PARAMS = {
    'client_id': WEIBO_APP_KEY,
    'client_secret': WEIBO_APP_SECRET,
    'grant_type': 'authorization_code',
    'redirect_uri': WEIBO_CALLBACK_URL,
    'code': '',  # 第一步的结果
}

# 获取用户信息
WEIBO_INFO_API = 'https://api.weibo.com/2/users/show.json'
WEIBO_INFO_PARAMS = {
    'access_token': '',
    'uid': ''
}
