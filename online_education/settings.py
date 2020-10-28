"""
Django settings for online_education project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import sys
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# 将我们自己定的包加入到Python搜索环境变量中
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+9w&&5d$(x28zo(-n25d_xplgtae&%7()##gqplj-smxur!(ha'

# SECURITY WARNING: don't run with debug turned on in production!
"""
测试环境
"""
DEBUG = True

ALLOWED_HOSTS = []
"""
生产环境
"""
# DEBUG = False
#
# ALLOWED_HOSTS = ['*']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'apps.apps.AppsConfig',
    'apps.courses.apps.CoursesConfig',  # or 'courses.apps.CoursesConfig',
    'apps.operations.apps.OperationsConfig',
    'apps.orgs.apps.OrgsConfig',
    'apps.users.apps.UsersConfig',
    # 'extra_apps.xadmin' # or 'xadmin'
    'xadmin',
    'crispy_forms',
    'captcha',
    'DjangoUeditor',
]

AUTH_USER_MODEL = 'users.UserProfile'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'online_education.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # 要使用{{MEDIA_URL}}这句得加上

            ],
            # 下面的配置可以让我们在视图中不需要写{% load static %}
            'builtins': [
                'django.templatetags.static',
            ]
        },
    },
]

WSGI_APPLICATION = 'online_education.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'online_education',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'online_education',
    #     'USER': 'Erics',
    #     'PASSWORD': 'Erics123456!',
    #     'HOST': '47.102.145.225',
    #     'PORT': '3306',
    # },
    # 'remote_mysql': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'online_education',
    #     'USER': 'Erics',
    #     'PASSWORD': 'Erics123456!',
    #     'HOST': '47.102.145.225',
    #     'PORT': '3306',
    # },
    # 'sqlite3': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

"""
测试服务器会找下面的路径
"""
STATIC_URL = '/static/'  # 引用名
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')  # 实际名 ,即实际文件夹的名字
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# DATABASE_ROUTERS = ['mysql_router.Router']

EMAIL_HOST = 'smtp.yeah.net'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'erics1996@yeah.net'
EMAIL_HOST_PASSWORD = 'ICIWFENZLJGETKWP'
EMAIL_FROM = 'erics1996@yeah.net'
