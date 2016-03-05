# -*- coding: utf-8 -*-
import datetime
import os
import re
import sys

from typing import Any, Tuple  # noqa

if sys.version_info < (3, 3):
    # dependency on ipaddress module
    raise Exception("Python 3.3 or higher is required.")

from ..utils import helpers  # noqa
""" !! In production, add a file called secret.py to the settings package that
defines AUTHUSER_PASSWORD, SECRET_KEY, SECRET_DATABASE_URL. !!


SECRET_DATABASE_URL should be of the following form:
    postgres://<user>:<password>@<host>/<database>
"""
SECRET_DATABASE_URL = None  # type: str
ADMINS = None  # type: List[Tuple[str,str]]
USE_SASL = True

try:
    from .secret import *  # noqa
except ImportError:
    pass

PRODUCTION = os.getenv("PRODUCTION") == "TRUE"
TRAVIS = os.getenv("TRAVIS") == "true"
# FIXME: figure out a less-hacky way to do this.
TESTING = 'test' in sys.argv
LOGGING_VERBOSE = PRODUCTION

# DEBUG defaults to off in PRODUCTION, on otherwise.
DEBUG = os.getenv("DEBUG", str(not PRODUCTION).upper()) == "TRUE"

# Don't send emails unless we're in production.
EMAIL_ANNOUNCEMENTS = PRODUCTION
# Don't require https for testing.
SESSION_COOKIE_SECURE = PRODUCTION
CSRF_COOKIE_SECURE = PRODUCTION

if not PRODUCTION:
    # We don't care about session security when running a testing instance.
    SECRET_KEY = "_5kc##e7(!4=4)h4slxlgm010l+43zd_84g@82771ay6no-1&i"
    # Trust X-Forwarded-For when testing
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

# Internal IP ranges in production
_internal_ip_list = ["198.38.16.0/20", "2001:468:cc0::/48"]

if not PRODUCTION:
    # Additional Internal IP ranges for debugging
    _internal_ip_list.extend(["127.0.0.0/8", "10.0.0.0/8"])

INTERNAL_IPS = helpers.GlobList(_internal_ip_list)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/"

APPEND_SLASH = False

# Email backend and mailserver configuration

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mail.tjhsst.edu"
EMAIL_PORT = 25
EMAIL_USE_TLS = False  # FIXME: use tls
EMAIL_SUBJECT_PREFIX = "[Ion] "
EMAIL_ANNOUNCEMENTS = True

EMAIL_FROM = "ion-noreply@tjhsst.edu"

# Address to send production error messages

if ADMINS is None:
    ADMINS = [("Dummy User", "root@localhost")]

# Use PostgreSQL database

DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'CONN_MAX_AGE': 30}}  # type: Dict[str,Dict[str,Any]]

# In-memory sqlite3 databases signifigantly speeds up the tests.
if TESTING:
    DATABASES["default"]["ENGINE"] = "django.db.backends.sqlite3"
    # Horrible hack to suppress all migrations to speed up the tests.
    MIGRATION_MODULES = helpers.MigrationMock()
    # FIXME: we really shouldn't have to do this.
    LOGGING_VERBOSE = re.search('-v ?[2-3]|--verbosity [2-3]', ' '.join(sys.argv)) is not None
elif PRODUCTION or SECRET_DATABASE_URL is not None:
    DATABASES['default'].update(helpers.parse_db_url(SECRET_DATABASE_URL))
else:
    # Default testing db config.
    DATABASES["default"].update({"NAME": "ion", "USER": "ion", "PASSWORD": "pwd"})

MANAGERS = ADMINS

# Address to send feedback messages to
FEEDBACK_EMAIL = "intranet@lists.tjhsst.edu"

# Address to send approval messages to
APPROVAL_EMAIL = "intranet-approval@lists.tjhsst.edu"

FILE_UPLOAD_HANDLERS = ["django.core.files.uploadhandler.MemoryFileUploadHandler", "django.core.files.uploadhandler.TemporaryFileUploadHandler"]

# The maximum number of pages in one document that can be
# printed through the printing functionality (determined through pdfinfo)
PRINTING_PAGES_LIMIT = 15

# The maximum file upload and download size for files
FILES_MAX_UPLOAD_SIZE = 200 * 1024 * 1024
FILES_MAX_DOWNLOAD_SIZE = 200 * 1024 * 1024

CSRF_FAILURE_VIEW = "intranet.apps.error.views.handle_csrf_view"

# Django 1.9 gives the warning that "Your url pattern has a regex beginning with
# a '/'. Remove this slash as it is unnecessary." In our use case, the slash actually
# is important; in urls.py we include() a separate urls.py inside of each app, and the
# pattern for each does not end in a slash. This allows us to match the index page of
# the app without a slash, and then we add the slash manually in every other rule.
# Without this, we'd have urls like /announcements/?show_all=true which is just ugly.
# Thus, we silence this system check. -- JW, 12/30/2015
# W001 doesn't apply, as we use nginx to handle SecurityMiddleware's functions.
# Suppress W019, as we use frames in the signage module.
SILENCED_SYSTEM_CHECKS = ["urls.W002", "security.W001", "security.W019"]

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
#
# In production, Nginx filters requests that are not in this list. If this is
# not done, an email failure notification gets sent whenever someone messes with
# the HTTP Host header.
ALLOWED_HOSTS = ["ion.tjhsst.edu", "198.38.18.250", "localhost", "127.0.0.1"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "America/New_York"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#
# Not used.
MEDIA_ROOT = ""

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#
# Not used.
MEDIA_URL = ""

TEST_RUNNER = "django.test.runner.DiscoverRunner"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#
# This is the folder that Nginx serves as /static in production
STATIC_ROOT = os.path.join(PROJECT_ROOT, "collected_static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don"t forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, "static"),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.FileSystemFinder",
                       "django.contrib.staticfiles.finders.AppDirectoriesFinder",
                       # "django.contrib.staticfiles.finders.DefaultStorageFinder",
                       )

AUTHENTICATION_BACKENDS = ("intranet.apps.auth.backends.MasterPasswordAuthenticationBackend",
                           "intranet.apps.auth.backends.KerberosAuthenticationBackend",
                           "oauth2_provider.backends.OAuth2Backend",)

# Use the custom User model defined in apps/users/models.py
AUTH_USER_MODEL = "users.User"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (os.path.join(PROJECT_ROOT, "templates"),),
        "OPTIONS": {
            "context_processors":
            ("django.contrib.auth.context_processors.auth",  # Authentication; must be defined first
             "django.template.context_processors.debug",  # Django default
             "django.template.context_processors.request",  # Django default
             "django.contrib.messages.context_processors.messages",  # For page messages
             "intranet.apps.context_processors.ion_base_url",  # For determining the base url
             "intranet.apps.context_processors.nav_categorizer",  # For determining the category in the navbar
             "intranet.apps.context_processors.global_warning",  # For showing a global warning throughout the application (in page_base.html)
             "intranet.apps.eighth.context_processors.start_date",  # For determining the eighth pd start date
             "intranet.apps.eighth.context_processors.absence_count",  # For showing the absence count in the navbar
             "intranet.apps.context_processors.mobile_app"  # For the custom android app functionality (tbd?)
             ),
            "debug": True,  # Only enabled if DEBUG is true as well
            'loaders': (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ),
            'libraries': {
                'staticfiles': 'django.contrib.staticfiles.templatetags.staticfiles',
            },
        }
    },
]  # type: List[Dict[str,Any]]

if PRODUCTION:
    TEMPLATES[0]["OPTIONS"]["loaders"] = [('django.template.loaders.cached.Loader', [
                                           'django.template.loaders.filesystem.Loader',
                                           'django.template.loaders.app_directories.Loader'])]

if not PRODUCTION and os.getenv("WARN_INVALID_TEMPLATE_VARS", "NO") == "YES":
    TEMPLATES[0]["OPTIONS"]["string_if_invalid"] = helpers.InvalidString("%s")

MIDDLEWARE_CLASSES = [
    "intranet.middleware.url_slashes.FixSlashes",  # Remove slashes in URLs
    "django.middleware.common.CommonMiddleware",  # Django default
    "django.contrib.sessions.middleware.SessionMiddleware",  # Django sessions
    "django.middleware.csrf.CsrfViewMiddleware",  # Django CSRF
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Django X-Frame-Options
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Django auth
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",  # Django session auth
    "oauth2_provider.middleware.OAuth2TokenMiddleware",  # Django Oauth toolkit
    "maintenancemode.middleware.MaintenanceModeMiddleware",  # Maintenance mode
    "intranet.middleware.environment.KerberosCacheMiddleware",  # Kerberos
    "intranet.middleware.threadlocals.ThreadLocalsMiddleware",  # Thread locals
    "intranet.middleware.traceback.UserTracebackMiddleware",  # Include user in traceback
    "django.contrib.messages.middleware.MessageMiddleware",  # Messages
    "intranet.middleware.ajax.AjaxNotAuthenticatedMiddleWare",  # See note in ajax.py
    "intranet.middleware.templates.AdminSelectizeLoadingIndicatorMiddleware",  # Selectize fixes
    "intranet.middleware.access_log.AccessLogMiddleWare",  # Access log
    "corsheaders.middleware.CorsMiddleware",  # CORS headers, for ext. API use
    # "intranet.middleware.profiler.ProfileMiddleware",         # Debugging only
    "intranet.middleware.ldap_db.CheckLDAPBindMiddleware",  # Show ldap simple bind message
]

# URLconf at urls.py
ROOT_URLCONF = "intranet.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "intranet.wsgi.application"

# Name of current virtualenv
VIRTUAL_ENV = os.path.basename(os.environ["VIRTUAL_ENV"]) if "VIRTUAL_ENV" in os.environ else "None"


def get_month_seconds():
    return datetime.timedelta(hours=24).total_seconds() * 30

# Age of cache information
CACHE_AGE = {
    "dn_id_mapping": int(12 * get_month_seconds()),
    "user_grade": int(10 * get_month_seconds()),
    "user_classes": int(6 * get_month_seconds()),
    "user_photo": int(6 * get_month_seconds()),
    "class_teacher": int(6 * get_month_seconds()),
    "class_attribute": int(6 * get_month_seconds()),
    "user_attribute": int(2 * get_month_seconds()),
    "bell_schedule": int(datetime.timedelta(weeks=1).total_seconds()),
    "ldap_permissions": int(datetime.timedelta(hours=24).total_seconds()),
    "users_list": int(datetime.timedelta(hours=24).total_seconds()),
    "emerg": int(datetime.timedelta(minutes=5).total_seconds())
}

if not PRODUCTION and os.getenv("SHORT_CACHE", "NO") == "YES":
    # Make the cache age last just long enough to reload the page to
    # check if caching worked
    for key in CACHE_AGE:
        CACHE_AGE[key] = 60

# Cacheops configuration
# may be removed in the future
CACHEOPS_REDIS = {"host": "127.0.0.1", "port": 6379, "db": 1, "socket_timeout": 1}

CACHEOPS_DEGRADE_ON_FAILURE = True

CACHEOPS_DEFAULTS = {"ops": "all", "cache_on_save": True, "timeout": int(datetime.timedelta(hours=24).total_seconds())}

CACHEOPS = {
    "eighth.*": {
        "timeout": 1  # int(datetime.timedelta(hours=1).total_seconds())
    },
    "announcements.*": {},
    "events.*": {},
    "groups.*": {},
    "users.*": {},
    "auth.*": {}
}

if not TESTING:
    # Settings for django-redis-sessions
    SESSION_ENGINE = "redis_sessions.session"

    SESSION_REDIS_HOST = "127.0.0.1"
    SESSION_REDIS_PORT = 6379
    SESSION_REDIS_DB = 0
    SESSION_REDIS_PREFIX = VIRTUAL_ENV + ":session"

    SESSION_COOKIE_AGE = int(datetime.timedelta(hours=2).total_seconds())
    SESSION_SAVE_EVERY_REQUEST = True

CACHES = {
    "default": {
        "OPTIONS": {
            # Avoid conflict between production and testing redis db
            "DB": 1 if PRODUCTION else 2,
        }
    }
}  # type: Dict[str,Dict[str,Any]]

if TESTING or os.getenv("DUMMY_CACHE", "NO") == "YES":
    CACHES["default"]["BACKEND"] = "django.core.cache.backends.dummy.DummyCache"
else:
    CACHES["default"] = {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "127.0.0.1:6379",
        "OPTIONS": {
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "PICKLE_VERSION": 4,
        },
        "KEY_PREFIX": VIRTUAL_ENV
    }

# LDAP configuration
AD_REALM = "LOCAL.TJHSST.EDU"  # Active Directory (LOCAL) Realm
CSL_REALM = "CSL.TJHSST.EDU"  # CSL Realm
HOST = "ion.tjhsst.edu"
LDAP_REALM = CSL_REALM
LDAP_SERVER = "ldap://iodine-ldap.tjhsst.edu"
KINIT_TIMEOUT = 15  # seconds before pexpect timeouts

AUTHUSER_DN = "cn=authuser,dc=tjhsst,dc=edu"

# LDAP schema config
BASE_DN = "dc=tjhsst,dc=edu"
USER_DN = "ou=people,dc=tjhsst,dc=edu"
CLASS_DN = "ou=schedule,dc=tjhsst,dc=edu"

LDAP_OBJECT_CLASSES = {"student": "tjhsstStudent", "teacher": "tjhsstTeacher", "simple_user": "simpleUser", "attendance_user": "tjhsstUser"}

FCPS_STUDENT_ID_LENGTH = 7

# Django REST framework configuration
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),  # require authentication
    "USE_ABSOLUTE_URLS": True,

    # Return native `Date` and `Time` objects in `serializer.data`
    "DATETIME_FORMAT": None,
    "DATE_FORMAT": None,
    "TIME_FORMAT": None,
    "EXCEPTION_HANDLER": "intranet.apps.api.utils.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_AUTHENTICATION_CLASSES": ("intranet.apps.api.authentication.KerberosBasicAuthentication",
                                       "rest_framework.authentication.SessionAuthentication",
                                       "oauth2_provider.ext.rest_framework.OAuth2Authentication"),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",)
}

# Django Oauth Toolkit configuration
OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope',
               'write': 'Write scope'}
}
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'

INSTALLED_APPS = [
    # internal Django
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Django plugins
    "django_extensions",
    "rest_framework",
    "maintenancemode",
    # Intranet apps
    "intranet.apps",
    "intranet.apps.announcements",
    "intranet.apps.api",
    "intranet.apps.auth",
    "intranet.apps.eighth",
    "intranet.apps.events",
    "intranet.apps.groups",
    "intranet.apps.search",
    "intranet.apps.schedule",
    "intranet.apps.notifications",
    "intranet.apps.feedback",
    "intranet.apps.users",
    "intranet.apps.preferences",
    "intranet.apps.files",
    "intranet.apps.printing",
    "intranet.apps.polls",
    "intranet.apps.signage",
    "intranet.apps.seniors",
    "intranet.apps.emerg",
    "intranet.apps.ionldap",
    # Intranet middleware
    "intranet.middleware.environment",
    # Django plugins
    "widget_tweaks",
    "oauth2_provider",
    "corsheaders",
    "cacheops"
]

# Eighth period default block date format
# Post Django 1.8.7, this can no longer be used in templates.
EIGHTH_BLOCK_DATE_FORMAT = "D, N j, Y"

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOG_LEVEL = "DEBUG" if LOGGING_VERBOSE else "INFO"
if os.getenv("LOG_LEVEL") in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
    LOG_LEVEL = os.environ["LOG_LEVEL"]


def get_log(name):
    return [name] if (PRODUCTION and not TRAVIS) else []


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "%(levelname)s: %(message)s"
        },
        "access": {
            "format": "%(message)s"
        }
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        # Email ADMINS
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "intranet.middleware.email_handler.AdminEmailHandler",
            "include_html": True
        },
        # Log in console
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
        # Log access in console
        "console_access": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "access"
        },
        # Log access to file (DEBUG=FALSE)
        "access_log": {
            "level": "DEBUG",
            "filters": ["require_debug_false"],
            "class": "logging.FileHandler",
            "formatter": "access",
            "filename": "/var/log/ion/app_access.log",
            "delay": True
        },
        # Log auth to file (DEBUG=FALSE)
        "auth_log": {
            "level": "DEBUG",
            "filters": ["require_debug_false"],
            "class": "logging.FileHandler",
            "formatter": "access",
            "filename": "/var/log/ion/app_auth.log",
            "delay": True
        },
        # Log error to file (DEBUG=FALSE)
        "error_log": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "logging.FileHandler",
            "delay": True,
            "filename": "/var/log/ion/app_error.log"
        },
    },
    "loggers": {
        # Django errors get sent to the error log
        "django": {
            "handlers": ["console"] + get_log("error_log"),
            "level": "ERROR",
            "propagate": True,
        },
        # Intranet errors email admins and errorlog
        "intranet": {
            "handlers": ["console", "mail_admins"] + get_log("error_log"),
            "level": LOG_LEVEL,
            "propagate": True,
        },
        # Intranet access logs to accesslog
        "intranet_access": {
            "handlers": ["console_access"] + get_log("access_log"),
            "level": "DEBUG",
            "propagate": False
        },
        # Intranet auth logs to authlog
        "intranet_auth": {
            "handlers": ["console_access"] + get_log("auth_log"),
            "level": "DEBUG",
            "propagate": False
        }
    }
}

# The debug toolbar is always loaded, unless you manually override SHOW_DEBUG_TOOLBAR
SHOW_DEBUG_TOOLBAR = os.getenv("SHOW_DEBUG_TOOLBAR", "YES") == "YES"

if SHOW_DEBUG_TOOLBAR:
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    # Boolean value defines whether enabled by default
    _panels = [
        ("debug_toolbar.panels.versions.VersionsPanel", False),
        ("debug_toolbar.panels.timer.TimerPanel", True),
        ("debug_toolbar.panels.settings.SettingsPanel", False),
        ("debug_toolbar.panels.headers.HeadersPanel", False),
        ("debug_toolbar.panels.request.RequestPanel", False),
        ("debug_toolbar.panels.sql.SQLPanel", True),
        ("debug_toolbar.panels.staticfiles.StaticFilesPanel", False),
        ("debug_toolbar.panels.templates.TemplatesPanel", False),
        ("debug_toolbar.panels.cache.CachePanel", False),
        ("debug_toolbar.panels.signals.SignalsPanel", False),
        ("debug_toolbar.panels.logging.LoggingPanel", True),
        ("debug_toolbar.panels.redirects.RedirectsPanel", False),
        ("debug_toolbar.panels.profiling.ProfilingPanel", False),
        # FIXME: broken ("debug_toolbar_line_profiler.panel.ProfilingPanel", False),
    ]

    DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False, "DISABLE_PANELS": [panel for panel, enabled in _panels if not enabled]}

    DEBUG_TOOLBAR_PANELS = [t[0] for t in _panels]

    # Add middleware
    MIDDLEWARE_CLASSES.extend([
        "intranet.middleware.templates.StripNewlinesMiddleware",  # Strip newlines
        "debug_toolbar.middleware.DebugToolbarMiddleware",  # Debug toolbar
    ])

    INSTALLED_APPS += ["debug_toolbar", "debug_toolbar_line_profiler"]

    # Only show debug toolbar when requested if in production.
    DEBUG_TOOLBAR_CONFIG["SHOW_TOOLBAR_CALLBACK"] = "intranet.utils.helpers.debug_toolbar_callback"

# Maintenance mode
MAINTENANCE_MODE = False

# Allow *.tjhsst.edu sites to access API, signage, and other resources
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_REGEX_WHITELIST = ('^(https?://)?(\w+\.)?tjhsst\.edu$')

# Uncomment to only allow XHR on API resources from TJ domains
# CORS_URLS_REGEX = r'^/api/.*$'

# Same origin frame options
X_FRAME_OPTIONS = 'SAMEORIGIN'

# X-XSS-Protection: 1; mode=block
# Already set on nginx level
SECURE_BROWSER_XSS_FILTER = True

# Add git information for the login page
GIT = {
    "commit_short_hash": helpers.get_current_commit_short_hash(PROJECT_ROOT),
    "commit_long_hash": helpers.get_current_commit_long_hash(PROJECT_ROOT),
    "commit_info": helpers.get_current_commit_info(),
    "commit_date": helpers.get_current_commit_date(),
    "commit_github_url": helpers.get_current_commit_github_url(PROJECT_ROOT)
}

# Senior graduation date in Javascript-readable format
SENIOR_GRADUATION = datetime.datetime(year=2016, month=6, day=18, hour=19).strftime('%B %d %Y %H:%M:%S')

# Senior graduation year
SENIOR_GRADUATION_YEAR = 2016

# The hour on an eighth period day to lock teachers from
# taking attendance (10PM)
ATTENDANCE_LOCK_HOUR = 20

# The number of days to show an absence message (2 weeks)
CLEAR_ABSENCE_DAYS = 14

# The address for FCPS' Emergency Announcement page
FCPS_EMERGENCY_PAGE = "http://www.fcps.edu/content/emergencyContent.html"

# Shows a warning message with yellow background on the login page
# LOGIN_WARNING = "This is a message to display on the login page."

# Shows a warning message with yellow background on the login and all interior pages
# GLOBAL_WARNING = "This is a message to display throughout the application."
