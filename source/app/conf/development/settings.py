from django.utils.translation import gettext_lazy as _
import os
import warnings
from os.path import dirname

from django.utils.translation import ugettext_lazy as _

warnings.simplefilter('error', DeprecationWarning)

BASE_DIR = dirname(dirname(dirname(dirname(os.path.abspath(__file__)))))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')

SECRET_KEY = 'NhfTvayqggTBPswCXXhWaN69HuglgZIkM'

DEBUG = True
ALLOWED_HOSTS = []

SITE_ID = 1

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # google auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    # Vendor apps
    'bootstrap4',

    # Application apps
    'main',
    'accounts',
    'captcha',
    'downtime',
    'django_forum_app',
    'photologue',
    'tinymce',
    'avatar',
    'flag',
    'notify',


]

# TINYMCE_JS_URL = 'http://tinymce.moxiecode.com/js/tinymce/jscripts/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = os.path.join(CONTENT_DIR, 'static/vendor/tinymce')
TINYMCE_JS_URL = os.path.join(TINYMCE_JS_ROOT, "tinymce.min.js")

TINYMCE_DEFAULT_CONFIG = {
    'language': 'en',
    'theme': 'modern',
    'height': 200,
    'plugins': [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table contextmenu paste emoticons media',
    ],
    'toolbar': 'media | emoticons | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | code preview',
    'menubar': False,
    'media_alt_source': False,
    'media_poster': False,
    'media_dimensions': False,
}

RECAPTCHA_PUBLIC_KEY = '6LeZd9kZAAAAAOkzaVVfV4qAhr7p2HwFUlhLQc4w'
RECAPTCHA_PRIVATE_KEY = '6LeZd9kZAAAAANpAdxal24uWdqXK_EGZNsVG2Xp2'


MIDDLEWARE = [
    'downtime.middleware.DowntimeMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(CONTENT_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'app.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FILE_PATH = os.path.join(CONTENT_DIR, 'tmp/emails')
EMAIL_HOST_USER = 'test@example.com'
DEFAULT_FROM_EMAIL = 'test@example.com'

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'social_app_db',
        'USER': 'root',
        'PASSWORD': '01858692m!K',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ENABLE_USER_ACTIVATION = False
DISABLE_USERNAME = False
LOGIN_VIA_EMAIL = True
LOGIN_VIA_EMAIL_OR_USERNAME = False
LOGIN_REDIRECT_URL = 'django_forum_app:fresh'
LOGIN_URL = 'accounts:log_in'
USE_REMEMBER_ME = True
RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME = False
ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE = True

SIGN_UP_FIELDS = ['username', 'first_name',
                  'last_name', 'email', 'password1', 'password2']
if DISABLE_USERNAME:
    SIGN_UP_FIELDS = ['first_name', 'last_name',
                      'email', 'password1', 'password2']

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('zh-Hans', _('Simplified Chinese')),
]

TIME_ZONE = 'UTC'
USE_TZ = True

STATIC_ROOT = os.path.join(CONTENT_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(CONTENT_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(CONTENT_DIR, 'assets'),
    os.path.join(CONTENT_DIR, 'images')

]

LOCALE_PATHS = [
    os.path.join(CONTENT_DIR, 'locale')
]

# Settings related to flag app

FLAGS_ALLOWED = 3


FLAG_REASONS = [(1, _('Spam | Exists only to promote a service')),
                (2, _('Abusive | Intended at promoting hatred')),
                (3, _('Obscene | Promotes obscenity')),]

# Post to be displyed on feed with minimum No. of upvotes
FEED_MIN_UPVOTES = 3

# No. of Forum to be displyed on Popular (side bar)
POPULAR_FORUMS = 15
if DEBUG:
    STRIPE_PUBLISHABLE_KEY = 'pk_test_51McS4uSG4BR6YpnQyLUy50KAqQNkBeFUzLYsJ1vbj60tMkmkEg2hfAfZIWbgpHD8MNdo8QMxUooIGQyyb31xu4n500kxM0whTq'
    STRIPE_SECRET_KEY = 'pk_test_51McS4uSG4BR6YpnQyLUy50KAqQNkBeFUzLYsJ1vbj60tMkmkEg2hfAfZIWbgpHD8MNdo8QMxUooIGQyyb31xu4n500kxM0whTq'
