import os

os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-local-testing')
os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('DB_NAME', 'test_db')
os.environ.setdefault('DB_USER', 'root')
os.environ.setdefault('DB_PASSWORD', 'test')
os.environ.setdefault('DB_HOST', '127.0.0.1')
os.environ.setdefault('DB_PORT', '3306')
os.environ.setdefault('EMAIL_HOST', 'smtp.example.com')
os.environ.setdefault('EMAIL_PORT', '587')
os.environ.setdefault('EMAIL_HOST_USER', 'test@example.com')
os.environ.setdefault('EMAIL_HOST_PASSWORD', 'testpass')

from core.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
