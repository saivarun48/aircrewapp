from os import environ as env
import os
#import multiprocessing

PORT = int(env.get("PORT", 8000))
DEBUG_MODE = int(env.get("DEBUG_MODE", 1))

# App Info 
LANGUAGE = 'EN'

# Azure Info
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
AZURE_STORAGE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
AZURE_STORAGE_CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
AZURE_STORAGE_ACCOUNT_KEY = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')

# Database Info
DB_CONNECT_STRING = os.environ.get('DB_CONNECT_STRING')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


# Gunicorn config
bind = ":" + str(PORT)
#workers = multiprocessing.cpu_count() * 2 + 1
#threads = 2 * multiprocessing.cpu_count()