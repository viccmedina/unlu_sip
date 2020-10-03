from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from distribuidora.settings import DB_PATH, DB_SECRET_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = DB_SECRET_KEY

db = SQLAlchemy(app)

# Conectamos la aplicación con DB
Migrate(app, db)

# Blueprints
from distribuidora.core.provincia.views import provincia_blueprint
from distribuidora.core.localidad.views import localidad_blueprint
from distribuidora.core.domicilio.views import domicilio_blueprint
from distribuidora.core.tipo_dni.views import tipo_dni_blueprint
from distribuidora.core.rol_permiso.views import rol_permiso_blueprint
from distribuidora.core.usuario.views import usuario_blueprint
from distribuidora.core.usuario_permiso.views import usuario_permiso_blueprint
from distribuidora.core.usuario_rol.views import usuario_rol_blueprint
from distribuidora.core.persona.view import persona_blueprint

app.register_blueprint(provincia_blueprint, url_prefix='/provincia')
app.register_blueprint(localidad_blueprint, url_prefix='/localidad')
app.register_blueprint(tipo_dni_blueprint, url_prefix='/tipo_dni')
app.register_blueprint(rol_permiso_blueprint, url_prefix='/rol_permiso')
app.register_blueprint(usuario_blueprint,url_prefix='/usuario')
app.register_blueprint(usuario_permiso_blueprint,url_prefix='/usuario_permiso')
app.register_blueprint(usuario_rol_blueprint,url_prefix='/usuario_rol')
app.register_blueprint(persona_blueprint,url_prefix='/persona')