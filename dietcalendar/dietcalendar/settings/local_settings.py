import os

SECRET_KEY = '51xfz(#yc)h$1#2i$=oz@dsm!ew(=6tip_0$r-7+o+j_=$ib#t'

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = os.path.dirname(os.path.dirname(os.pardir(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "..", 'dev_db.sqlite3'),
    }
}