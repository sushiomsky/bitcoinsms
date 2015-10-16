import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = []
INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'rest_framework',
    'bitcoinsms.api',
    'bitcoinsms.site'
)
MIDDLEWARE_CLASSES = ()
ROOT_URLCONF = 'bitcoinsms.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'bitcoinsms.site.context_processors.site_name',
                'bitcoinsms.site.context_processors.base_url'
            ],
        },
    },
]
WSGI_APPLICATION = 'bitcoinsms.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT= '/opt/static/'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}

BITCOIN_RPC_HOST = "127.0.0.1:8332"
SMS_COST_IN_SATOSHIS = 50000
DEBUG = False
DEBUG_FAKE_BITCOIN = False
DEBUG_FAKE_SENDING = False
SITE_NAME = "BitcoinSMS.io"
BASE_URL = "https://bitcoinsms.io"

# You need to create settings_local.py to set the following sensitive
# configurations. you would NEVER want to check these into version control.
# In addition you can override any settings above in settings_local.py
SECRET_KEY = ''
NEXMO_API_KEY = ''
NEXMO_API_SECRET = ''
BITCOIN_RPC_USERNAME = ''
BITCOIN_RPC_PASSWORD = ''
SMS_NUMBER_FROM = ''

from bitcoinsms.settings_local import *
