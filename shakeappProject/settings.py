import os
ENV = 'prod'

# For determining which url to go to for adding a recipe
if ENV == 'dev':
    DEV = True
else:
    DEV = False

MEDIA_URL = '/media/'

# Amazon AWS
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'] 
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'] 
AWS_STORAGE_BUCKET_NAME = 'shakeappheroku'

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

if ENV == 'dev':
    from settings_dev import *
elif ENV =='prod':
    from settings_prod import *
else:
    raise Exception('Settings.py import error')

if ENV == 'dev':
    S3BUCKET = 'shakeappheroku_media_dev'
    S3URL = 'https://shakeappheroku_media_dev.s3.amazonaws.com/'
else:
    S3BUCKET = 'shakeappheroku_media_prod'
    S3URL = 'https://shakeappheroku_media_prod.s3.amazonaws.com/' 
