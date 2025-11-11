from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = False

ALLOWED_HOSTS = ['rbudget.fly.dev', 'localhost', '127.0.0.1', 'https://rbudget.fly.dev']

# Initialize environment variables
load_dotenv()

# Fetch the SECRET_KEY from the environment variables
SECRET_KEY = os.environ.get('SECRET_KEY')

# Raise an error if SECRET_KEY is not set
if not SECRET_KEY:
    raise ValueError("The SECRET_KEY environment variable is not set.")

INSTALLED_APPS = [
    'income.apps.IncomeConfig',
    'expenses.apps.ExpensesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'budget.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]# Use cookies to store session data
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Set the session cookie to persist (e.g., 2 weeks)
SESSION_COOKIE_AGE = 15552000  # 6 months in seconds

# Allow session cookies to persist even after the browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_SECURE = True  # Ensures cookies are sent over HTTPS only
SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access to session cookies
SESSION_COOKIE_SAMESITE = 'Lax'  # Protects against CSRF attacks

WSGI_APPLICATION = 'budget.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),  # Load DATABASE_URL from .env
        conn_max_age=600,  # Optional: Keep database connections open for 600 seconds
        conn_health_checks=True,  # Optional: Enable connection health checks
    )
}

CSRF_TRUSTED_ORIGINS = ["https://rbudget.fly.dev",  # full URL with https
]

FLY_CONSUL_URL = 'c1cc933a81b8b070'


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Karen added below here

