import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'omnicalc-secret-key-production-38492')
    MAX_HISTORY_ITEMS = 50
    DEBUG = False