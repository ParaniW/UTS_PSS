from django.conf import settings

DEBUG = True
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'uts_lms',          # Harus sesuai POSTGRES_DB
        'USER': 'uts_user',         # Harus sesuai POSTGRES_USER
        'PASSWORD': 'uts_password', # Harus sesuai POSTGRES_PASSWORD
        'HOST': 'uts_db',           # Nama container database
        'PORT': '5432',
    }
}

EXTRA_INSTALLED_APPS = [
    'core',
    'django_extensions',
]