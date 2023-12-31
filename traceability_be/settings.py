"""
Django settings for traceability_be project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from django.utils.timezone import timedelta
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-q$_4al88u3fm&x=avv$@4w6jp#!ztz&%g=jk7670ni49=4c8o2"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # librarie
    # "admin_tools",
    # "admin_tools.theming",
    # "admin_tools.menu",
    # "admin_tools.dashboard",
    # "djangobower",
    # "django.contrib.sites",
    #
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "cloudinary_storage",
    "django.contrib.staticfiles",
    "cloudinary",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    "drf_yasg",
    "user_image",
    "product_image",
    "grow_up_image",
    "user",
    "product",
    "comment",
    "growup",
    "transaction",
    "detail_description",
    "notification",
    "cart",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "product.middleware.CustomExceptionHandlerMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "traceability_be.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            # "loaders": [
            # "django.template.loaders.filesystem.Loader",
            # "django.template.loaders.app_directories.Loader",
            # "admin_tools.template_loaders.Loader",
            # ],
            "context_processors": [
                # custom
                # "admin_tools.template_loaders.Loader",
                # "django.core.context_processors.request",
                #
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "traceability_be.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": "traceabilityDB",
    #     "USER": "postgres",
    #     "PASSWORD": "trung2001",
    #     "HOST": "localhost",
    #     "PORT": "5432",
    # },
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Ho_Chi_Minh"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Custom
APPEND_SLASH = False


AUTH_USER_MODEL = "user.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "EXCEPTION_HANDLER": "utils.custom_exception_handler.custom_exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
ALLOWED_HOSTS = ["*"]


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": "secret",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "users.serializers.MyTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "api_key": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    # 'USE_SESSION_AUTH':False
}
# Send mail
# ADMINS = (("Your Name", "duongtrungqb12@gmail.com"),)
# OSCAR_FROM_EMAIL = "SimpRaidenEi"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_USE_TLS = True  # Set to False if your email server doesn't use TLS
EMAIL_HOST_USER = "duongtrungqb12@gmail.com"  # Replace with your email username
EMAIL_HOST_PASSWORD = "dlowmcbrjnydxedk"
# Replace with your email password
# SPECTACULAR_SETTINGS = {"COMPONENT_SPLIT_REQUEST": True}
##cloudinary
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "dhdztuiag",
    "API_KEY": "564387499357929",
    "API_SECRET": "0lDQDb72t79wF_3gBWYzPhuYdWI",
}
MEDIA_URL = "/media/"  # or any prefix you choose
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Statistical

# BOWER_COMPONENTS_ROOT = os.path.join("traceability_be", "components")


# BOWER_INSTALLED_APPS = (
#     "jquery#2.0.3",
#     "jquery-ui#~1.10.3",
#     "d3#3.3.6",
#     "nvd3#1.1.12-beta",
# ).finders.BowerFinder",)

# blockchain
WEB3_PROVIDER = "https://stylus-testnet.arbitrum.io/rpc"
ADDRESS_CONTRACT_ACTOR_MANAGER = "0x28Dd6CC1AC50c66b3f0d36935196398Ee8ea5685"
ADDRESS_CONTRACT_PRODUCT_MANAGER = "0x62D4a2b5D9b95F6Ad09a5FBC65EBF0a02cEBcD7b"
ADDRESS_CONTRACT_TRACEBILITY = "0xDa22e3Abe86A23Fd2b6546c3e8A0F3eD3D04A5a6"
CHAIN_ID = 23011913
PRIVATE_KEY_SYSTEM = "7b4bd6f0fd9472379cb51a0b9d7a7c7439446ef1f4fc8bb90395f964a57da751"

#
ORIGIN_URL = os.environ.get("ORIGIN_URL")
CLIENT_URL = os.environ.get("CLIENT_URL")
