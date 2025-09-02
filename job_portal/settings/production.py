SECRET_KEY = '@=&uxk$gj-pi_wbj2^@+kgvq3h=x^yrftea5%03e+)@bhbydry'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database settings for app
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dental_db',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'reset123'
    }
}
