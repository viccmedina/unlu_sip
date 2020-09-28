DB_PATH = ''
DB_SECRET_KEY = ''

try:
   from distribuidora.settings_local import *
except ImportError:
    raise Exception("A local_settings.py file is required to run this project")