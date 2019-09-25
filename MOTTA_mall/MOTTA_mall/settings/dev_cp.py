"""
Django settings for MOTTA_mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import sys

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v+-)rv3a&j@y2fjgwk8wb3f1@-@b*#ld!9i4@a+_)s@%b$!w1m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# 以防止黑客构造包来发送请求。只有在列表中的host才能访问
# ALLOWED_HOSTS = [
#     'api.motta.site',
#     '192.168.208.137',
#     '127.0.0.1',
#     'localhost',
#     'www.motta.site',
#     '192.168.208.135', # NET
#     '192.168.1.142', # 桥接
#
# ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users.apps.UsersConfig',
    'smscode.apps.SmscodeConfig',
    'createdata.apps.CreatedataConfig',
    'divices.apps.DivicesConfig',
    'wsdata.apps.WsdataConfig',
    'warning.apps.WarningConfig',

    'rest_framework',
    'corsheaders',  # 跨域 白名单
    'dwebsocket',
]
# Django版本的问题，1.10之前，中间件的key为MIDDLEWARE_CLASSES, 1.10之后，为MIDDLEWARE。
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]
# 跨域问题
CORS_ORIGIN_ALLOW_ALL = False


ROOT_URLCONF = 'MOTTA_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'DIRS': ['front_end_pc/dist'],
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
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "front_end_pc"),
# ]

# 在settings末尾添加  执行 collectstatic 时 文件路径
# 指定收集静态文件的目录
# STATIC_ROOT = '/home/xufang/Desktop/motta_project/MOTTA_v_1.0/MOTTA_mall/front_end_pc'
# 把STATICFILES_DIRS注释掉
'''
STATICFILES_DIRS =[
   os.path.join(BASE_DIR, 'static'),
]
'''

WSGI_APPLICATION = 'MOTTA_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'mysql',  # 数据库用户密码
        'NAME': 'MOTTA_data'  # 数据库名字
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "sms_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/15",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },

}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


# 异常处理
REST_FRAMEWORK = {

    'EXCEPTION_HANDLER': 'utils.exceptions.exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# 配置jwt
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # JWT_EXPIRATION_DELTA 指明token的有效期
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils_jwt.jwt_response_payload_handler',  # 自定义jwt认证成功返回数据
}
# 1.日志文件
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/MOTTA_data.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
# 2.自定义用户模型类
AUTH_USER_MODEL = 'users.User'

# 3.CORS 跨域请求  添加白名单
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',  # 前端访问
    'http://localhost:8080',
    'http://www.motta.com:8080',
    'http://api.motta.site:8000',
    'http://127.0.0.1:8080',
    'http://192.168.44.1:8080',
    'http://192.168.208.1:8020',
    'http://192.168.1.47:8080',
    'http://192.168.208.146:8000',
    'http://192.168.1.47:8080',
    'http://192.168.1.47:8081'
)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# 4.告知Django使用我们自定义的 认证后端
AUTHENTICATION_BACKENDS = [
    'users.utils_jwt.UsernameMobileAuthBackend',
]

# 设置WEBSOCKET_ACCEPT_ALL=True可以允许每一个单独的视图使用websockets
# WEBSOCKET_ACCEPT_ALL=True