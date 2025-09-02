from ..base import *

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
        'PASSWORD': 'Lw%92L;]AHdk'
    }
}

# Application Client-ID and Client-Secret

CLIENT_ID = 'hYjpXPIgnqB6I6rxfCosmWRpMZtIlCMNKb5HIA8L'
CLIENT_SECRET = '6ifWfljIRzrkwbmA4kx1Y34TwXt4Buq8UPIlux5lvvK5tg2IiqXc2TFBlzQ7SlTD8yuVK1bJy9C3lrIemGHIwGihnXWUUvpsKwobzpD6m8Uf15iqa461DrnokIUEbPyh'

# Server protocol

SERVER_PROTOCOLS = 'http://'

# Frontend URL
FRONT_END_URL = "dafront.mvpcopy.net"
DOMAIN_IP = "dawebapi.mvpcopy.net"

# SMTP Credentials
FROM_EMAIL = 'smtp@starkdigital.net'
EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_HOST_USER = 'smtp@starkdigital.net'
EMAIL_HOST_PASSWORD = 'admin?963'
EMAIL_PORT = '465'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False

FRONT_END_URL = "http://127.0.0.1:8000/"
BASE_URL = "http://127.0.0.1:8000/api/v1/"
