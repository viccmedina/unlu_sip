from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from distribuidora.settings import DB_PATH, DB_SECRET_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = DB_SECRET_KEY

db = SQLAlchemy(app)

# Conectamos la aplicación con DB
# Migrate(app, db)


# Blueprints
from distribuidora.core.views import core_blueprint
from distribuidora.core.provincia.views import provincia_blueprint
from distribuidora.core.localidad.views import localidad_blueprint
from distribuidora.core.domicilio.views import domicilio_blueprint
from distribuidora.core.tipo_dni.views import tipo_dni_blueprint
from distribuidora.core.gestion_usuario.views import gestion_usuario_blueprint
from distribuidora.core.persona.view import persona_blueprint

app.register_blueprint(core_blueprint, url_prefix='/')
app.register_blueprint(provincia_blueprint, url_prefix='/provincia')
app.register_blueprint(localidad_blueprint, url_prefix='/localidad')
app.register_blueprint(domicilio_blueprint, url_prefix='/domicilio')
app.register_blueprint(tipo_dni_blueprint, url_prefix='/tipo_dni')
app.register_blueprint(gestion_usuario_blueprint, url_prefix='/usuario')
app.register_blueprint(persona_blueprint, url_prefix='/persona')