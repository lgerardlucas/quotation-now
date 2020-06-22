import os
import psycopg2
from decouple import config
from dj_database_url import parse as dburl

# BASE_DIR = Define o caminho de partida do projeto para as demais configurações 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#SECRET_KEY = config('SECRET_KEY',default='m7!b(n)4$&jia=#@71=u24o4)xy79qaz$*2%+n#fk*dwdf0&j^')
SECRET_KEY = config('SECRET_KEY')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

DEBUG = config('DEBUG', default=False, cast=bool)

INTERNAL_IPS = ['127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'qnow_client',
    'qnow_user',
    'qnow_provider',
    'qnow_site',
    'rangefilter',
    'debug_toolbar',
]

CLOUDINARY = {
    'cloud_name' : config('cloud_name'),
    'api_key' : config('api_key'),
    'api_secret': config('api_secret')
}


# AUTH_USER_MODEL = Configuração que indica o uso da models customizada referente a User default do django
AUTH_USER_MODEL = "qnow_user.User"


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

ROOT_URLCONF = 'quotation-now.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',

            ],
        },
    },
]

WSGI_APPLICATION = 'quotation-now.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': config('ENGINE'),
        'NAME': config('NAME'),
        'USER': config('ROLE'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('HOST'),
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/


LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# Arquivos usados na renderização, exemplo: HTML
# STATICFILES_DIRS = Define os diretórios que serão vasculhados pelo FileSystemFinder.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# STATIC_ROOT = Define o diretório onde serão armazenados os arquivos estáticos coletados
STATIC_ROOT = 'staticfiles'
# STATIC_URL = Define o prefixo de URL para referência aos arquivos estáticos. exemplo: { static '/static/img.jpg}
STATIC_URL = '/static/'

# Arquivos usados pelo usuário, exemplo: uploads imagens
# MEDIA_ROOT = Define o diretório onde serão armazenados os arquivos de mídia (uploads).
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static/media/'))
# MEDIA_URL = Define o prefixo de URL para referência a arquivos de mídia (uploads).
MEDIA_URL = '/media/'

# Comando que faz um backup do arquivo .env renomeando para que o git o carregue consigo
# O conteúdo deste arquivo, deverá substituir o conteúdo do arquivo .env em outro computador
if os.path.isfile('.env'):
    os.system("cp -r -f .env .env.backup")


ADMINS = [('Marcos','lgerardlucas@gmail.com',)]

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER') 
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
SEND_EMAIL_SIS = config('SEND_EMAIL_SIS', default=True, cast=bool)



