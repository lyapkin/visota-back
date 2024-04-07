DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'visotadb',
        'USER': 'visota',
        'PASSWORD': 'visotabd13',
        'HOST': 'localhost',
        'PORT': '',
    }
}

SITE_DOMAIN = ''

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}