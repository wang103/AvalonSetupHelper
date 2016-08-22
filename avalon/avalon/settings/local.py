from avalon.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't8fg)85f2j_5z==ow7)t#4$x%fh76vhgdepw7p%!par=q35(4c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
  '*',
]

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'HOST': 'localhost',
    'PORT': '',           # empty for default
    'NAME': 'avalon',     # DB name
    'USER': 'saber',      # just a local user
    'PASSWORD': 'saber',  # just a local user
  },
  'sqlite3': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

