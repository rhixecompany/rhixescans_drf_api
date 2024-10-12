"""
With these settings, tests run faster.
"""

from .base import *  # noqa: F403
from .base import BASE_DIR
from .base import TEMPLATES
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="B0fgfgNoPPDPm6e5enTfW7EAAFHRqAC7WKT7RXWEzlmR8wlU9VMIozhkKsIPnef1",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DEBUGGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore[index]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "http://media.testserver"
# django-webpack-loader
# ------------------------------------------------------------------------------
WEBPACK_LOADER["DEFAULT"]["LOADER_CLASS"] = "webpack_loader.loaders.FakeWebpackLoader"  # noqa: F405
# Your stuff...
# ------------------------------------------------------------------------------
# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
if (
    env("POSTGRES_ENGINE", default="django.db.backends.sqlite3")
    == "django.db.backends.postgresql"
):
    DATABASES = {
        "default": {
            "ENGINE": env("POSTGRES_ENGINE"),
            "NAME": env("POSTGRES_DB"),
            "USER": env("POSTGRES_USER"),
            "PASSWORD": env("POSTGRES_PASSWORD"),
            "HOST": env("POSTGRES_HOST"),
            "PORT": env("POSTGRES_PORT"),
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "api.sqlite3",
            "USER": "",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "",
        },
    }
# DATABASES = {"default": env.db("DATABASE_URL")}  # noqa: ERA001
DATABASES["default"]["ATOMIC_REQUESTS"] = True
PAGINATE_BY = 15
DATETIME_FORMAT = "M d Y, h:i A"
