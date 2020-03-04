import os
from datetime import timedelta

from google.oauth2 import service_account

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Every time, generate secret key. e.g. .python manage.py generate_secret_key
SECRET_KEY = '@sz++6z)(18qjxyt%woye9$v_c(623l2h6=rq)k_og-p5yf47w'

# NOTE: Application constants
DEBUG = os.environ.get('DEBUG', False)

if DEBUG:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(BASE_DIR, 'iam.json')
    )
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, '.trash')
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = "/static/"

else:
    # NOTE: Sendgrid Email
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'apikey'
    EMAIL_FROM = "noreply@loftllc.dev"
    EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_API_KEY')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    # NOTE: Staticfile settings
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID')
    GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
    GS_FILE_OVERWRITE = False
    GS_DEFAULT_ACL = 'publicRead'
    GS_CACHE_CONTROL = 'max-age=2678400'
    GS_EXPIRATION = timedelta(hours=1)
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"


# NOTE: APP Settings
AUTH_USER_MODEL = 'app.User'
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = 'app:dashboard'
LOGIN_URL = 'app:login'

APPEND_SLASH = True
SITE_ID = 1
SECRET_KEY = '-)=9lusb4duh02=f7z-vel2#$%@n=g4&ei%7_oh$pp9&m8rsac'
ALLOWED_HOSTS = ['*']
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024**2*10

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django_extensions',
    'widget_tweaks',
    'storages',
    'src.app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

# NOTE: Routing settings
ROOT_URLCONF = 'src.urls'
WSGI_APPLICATION = 'src.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# NOTE: Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', 'docker'),
        'USER': os.environ.get('DATABASE_USER', 'docker'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'docker'),
        'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
    }
}

# NOTE: Authorize validations
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.\
UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.\
MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.\
CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.\
NumericPasswordValidator',
    },
]

# NOTE: Password hash algorithm
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

# NOTE: Internationalization settings
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
    ('ja', '日本語'),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'src', 'app', 'locale'),
)
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# NOTE: Logging setting
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'src.app': {
            'handlers': ['console'],
            'propagate': True,
        },
    },
}
