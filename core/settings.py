"""
Django settings for core project.
Projeto: Makis Digital - Base Central | makisdigital.com
Configurado para o seu portal profissional, com foco em segurança, performance e escalabilidade.
"""

from pathlib import Path
from decouple import config, Csv
import os

import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='localhost,127.0.0.1,195.26.252.210')


# Application definition

INSTALLED_APPS = [
    # Daphne precisa vir primeiro para o runserver servir WebSockets (chat em tempo real)
    'daphne',

    # Apps nativas do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Para SEO e sitemaps
    'django.contrib.sitemaps',

    # Apps de terceiros (segurança e performance)
    'whitenoise.runserver_nostatic',
    'channels',

    # Seus apps personalizados
    'core',
    'accounts',
    'portfolio',
    'blog',
    'utilidades',
    'comunidade',
    'chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Performance - arquivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# Channel layer do chat em tempo real. InMemoryChannelLayer só funciona com um único
# processo (bom para desenvolvimento local). Em produção com múltiplos workers/processos,
# trocar para channels_redis.core.RedisChannelLayer com um Redis real.
REDIS_URL = config('REDIS_URL', default='redis://127.0.0.1:6379')

# InMemoryChannelLayer only works within a single process — fine for local
# `runserver`, but with multiple workers/processes in production, messages
# would silently stop reaching everyone connected to a different process.
# Redis-backed layer is required as soon as there's more than one process.
if DEBUG:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        }
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [REDIS_URL],
            },
        }
    }


# Database - MySQL (sua escolha)
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',  # Suporte a emojis e caracteres especiais
        },
        # Performance - conexões persistentes
        'CONN_MAX_AGE': 60,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,  # Mais seguro que o padrão de 8
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (uploads de imagens dos projetos)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Performance - Whitenoise para comprimir arquivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Modelo de usuário personalizado
AUTH_USER_MODEL = 'accounts.PerfilUsuario'


# -------------------------- SEGURANÇA AVANÇADA --------------------------
# HTTPS em produção
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = not DEBUG
SECURE_BROWSER_XSS_FILTER = not DEBUG
SECURE_REFERRER_POLICY = 'same-origin'
X_FRAME_OPTIONS = 'DENY'  # Protege contra clickjacking

# Cloudflare & Nginx Proxy Reverse Headers
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True

# CSRF - permite apenas origens confiáveis em produção
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv(), default='https://makisjeanty.com,https://www.makisjeanty.com')

# Identidade do Site, Idiomas e SEO
SITE_NAME = config('SITE_NAME', default='Makis Jeanty')
SITE_DOMAIN = config('SITE_DOMAIN', default='makisjeanty.com')
SITE_URL = config('SITE_URL', default='https://makisjeanty.com')
DEFAULT_LANGUAGE = config('DEFAULT_LANGUAGE', default='fr')
SUPPORTED_LANGUAGES = config('SUPPORTED_LANGUAGES', cast=Csv(), default='fr,ht')


# -------------------------- PERFORMANCE --------------------------
# Cache com Redis (pode usar em produção para acelerar consultas)
if not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
        }
    }

# -------------------------- EMAIL --------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER')


# Sites framework (para sitemaps e SEO)
SITE_ID = 1