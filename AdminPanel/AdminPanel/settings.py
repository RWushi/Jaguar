from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR.parent))

from Instruments.Config import DATABASE_CONFIG

SECRET_KEY = 'django-insecure-m%smptp27b#$9k@11e=i_r@atww@(+7xyy4l2^wv8nklf*tt@b'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Questions'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
]

ROOT_URLCONF = 'AdminPanel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AdminPanel.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': DATABASE_CONFIG['host'],
        'NAME': DATABASE_CONFIG['database'],
        'USER': DATABASE_CONFIG['user'],
        'PASSWORD': DATABASE_CONFIG['password'],
        'PORT': DATABASE_CONFIG['port']
    }
}

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

STATIC_URL = '/static/'
#python AdminPanel/manage.py makemigrations
#python AdminPanel/manage.py migrate
#python AdminPanel/manage.py runserver