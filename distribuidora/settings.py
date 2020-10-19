DB_PATH = ''
DB_SECRET_KEY = ''
DATOS_PATH = ''

try:
   from distribuidora.settings_local import *
except ImportError:
    raise Exception("A settings_local.py file is required to run this project")