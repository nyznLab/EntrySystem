"""
Django settings for EntrySystem project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 医嘱记录，病程记录存放目录
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fr0z^p#00@t1qrf2j!7aa68_aybm5$z$b_c9!yak&&b+8^qqa%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'scales',
    'patients',
    'users',
    'inpatients',
    'followup',
    'statistics'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'EntrySystem.MyMiddleware.AuthMiddleWare',
    'EntrySystem.MyMiddleware.PageRecordMiddleWare',
]

ROOT_URLCONF = 'EntrySystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, "./templates", ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],

            'libraries': {
                'SelfDefinedFilter': 'patients.templatetags.SelfDefinedFilter',

            }
        },
    },
]

WSGI_APPLICATION = 'EntrySystem.wsgi.application'



# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.mysql',   # 数据库引擎
        # 'NAME': 'entry_system',         # 你要存储数据的库名，事先要创建之
        # 'USER': 'root',         # 数据库用户名
        # 'PASSWORD': '12345678',     # 密码
        # 'HOST': 'localhost',    # 主机
        # 'PORT': '3306',         # 数据库使用的端口

        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'entry_system',  # 你要存储数据的库名，事先要创建之
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456',  # 密码
        'HOST': 'localhost',  # 主机
        'PORT': '3306',  # 数据库使用的端口

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# access static files by url
STATIC_URL = '/mystatic/'  # 别名  #直接可以听过url访问到css或者js文件

# locate the common static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'common_static'),
]

# the dir for command "python manage.py collectstatic"
# 不是必须的，可以不使用
STATIC_ROOT = os.path.join(BASE_DIR, "collect_static")

SESSION_COOKIE_AGE = 60 * 60  # 设置过期时间60分钟，默认为两周
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 设置关闭浏览器时失效
# 在settings文件内添加下面的代码
INTERNAL_IPS = ['127.0.0.1']
