from .base import *
import ast
import sys
import os

ALLOWED_HOSTS = ['*']

WAGTAILADMIN_BASE_URL = "https://photonranch.org"

DEBUG = ast.literal_eval(os.environ.get('DEBUG', 'False'))
if DEBUG:
    print('WARNING: DEBUG mode is turned on in PRODUCTION!', file=sys.stderr)

SECRET_KEY = os.environ['SECRET_KEY']

DB_OPTIONS = {}

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'HOST': os.environ['DB_HOST'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'OPTIONS': {
        },
    }
}


# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET', 'photonranch-wagtail')
# AWS_S3_REGION_NAME = os.environ.get('AWS_DEFAULT_REGION', 'us-west-2')
# AWS_DEFAULT_ACL = None
# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# # s3 public media settings
# PUBLIC_MEDIA_LOCATION = 'files'
# MEDIA_URL = f'https://s3-{AWS_S3_REGION_NAME}.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{PUBLIC_MEDIA_LOCATION}/'
# # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# EMAIL_ENABLED = ast.literal_eval(os.environ.get('EMAIL_ENABLED', 'False'))
# if EMAIL_ENABLED:
#     EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
#     EMAIL_USE_TLS       = True
#     EMAIL_HOST          = 'smtp.gmail.com'
#     EMAIL_HOST_USER     = os.environ.get('EMAIL_USERNAME','')
#     EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD','')
#     EMAIL_PORT          =  587
#     DEFAULT_FROM_EMAIL  = 'LCO webmaster <change-me@lco.global>'
