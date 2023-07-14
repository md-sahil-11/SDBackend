from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOWED_ORIGINS = [
    "https://nl-frontend-seven.vercel.app",
    "http://sahil11.pythonanywhere.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False

ALLOWED_ORIGINS = []

CORS_ORIGIN_WHITELIST = (
    "https://nl-frontend-seven.vercel.app",
    "http://sahil11.pythonanywhere.com",
)
