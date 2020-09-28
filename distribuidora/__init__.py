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

app.register_blueprint(provincia_blueprint, url_prefix='/provincia')
app.register_blueprint(localidad_blueprint, url_prefix='/localidad')
