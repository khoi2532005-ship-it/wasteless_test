from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "3$kq1vn7+6#ia*1@dv@myfwsuo7w&9sx-c$wyz9+l*vgb6irbi"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [  # noqa
    "django_sass",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAIL_CACHE = False

try:
    from .local import *  # noqa
except ImportError:
    pass
