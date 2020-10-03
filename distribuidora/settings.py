DB_PATH = ''
DB_SECRET_KEY = ''

try:
   from unlu_sip.distribuidora.settings_local import *
except ImportError:
    raise Exception("A local_settings.py file is required to run this project")