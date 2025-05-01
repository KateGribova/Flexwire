import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get('SECRET_KEY', 'any-other-dummy-key')

DEBUG = os.environ.get('DEBUG', 'true').lower() in {
    'y',
    'yes',
    'true',
    '1',
    't',
}

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')


INSTALLED_APPS = [
    'ckeditor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'django_select2',
    'feedback.apps.FeedbackConfig',
    'home.apps.HomeConfig',
    'sorl.thumbnail',
    'teams.apps.TeamsConfig',
    'users.apps.UsersConfig',
    'debug_toolbar',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


INTERNAL_IPS = os.environ.get('INTERNAL_IPS', '*').split(',')


ROOT_URLCONF = 'flexwire.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


WSGI_APPLICATION = 'flexwire.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'NumericPasswordValidator',
    },
]


LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/auth/login/'

AUTH_USER_MODEL = 'users.CustomUser'


LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
else:
    EMAIL_HOST = 'smtp.yandex.ru'
    EMAIL_PORT = 465
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = True
    EMAIL_HOST_USER = os.environ.get(
        'EMAIL_HOST_USER', 'obviously.wrong@email.ru'
    )
    EMAIL_HOST_PASSWORD = os.environ.get(
        'EMAIL_HOST_PASSWORD', 'obviouslywrongpassword'
    )
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


DEFAULT_USER_ACTIVITY = os.environ.get(
    'DEFAULT_USER_ACTIVITY', str(DEBUG)
).lower() in {'y', 'yes', 'true', '1', 't'}


CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            [
                'Undo',
                'Redo',
                'Bold',
                'Italic',
                'Underline',
                'Link',
                'Unlink',
                'Anchor',
                'Format',
                'Maximize',
                'Source',
                'NumberedList',
                'BulletedList',
            ],
            [
                'JustifyLeft',
                'JustifyCenter',
                'JustifyRight',
                'JustifyBlock',
                'Font',
                'FontSize',
                'TextColor',
                'Outdent',
                'Indent',
                'HorizontalRule',
                'Blockquote',
            ],
        ],
        'width': 'auto',
        'extraPlugins': ','.join(
            [
                'codesnippet',
            ]
        ),
        'removePlugins': 'exportpdf',
    },
}
