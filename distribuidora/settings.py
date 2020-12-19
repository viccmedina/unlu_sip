DB_PATH = '/opt/unlu_sip/data.sqlite'
DB_SECRET_KEY = 'mysecretkey'
DATOS_PATH = '/opt/unlu_sip/distribuidora/datos/'
FILE_PATH = '/opt/unlu_sip/files/'
PATH_IMG = '/home/vmedina/unlu_sip/distribuidora/static/img/productos/'

try:
   from distribuidora.settings_local import *
except ImportError:
    raise Exception("A settings_local.py file is required to run this project")
