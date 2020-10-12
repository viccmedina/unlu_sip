from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from distribuidora.settings import DB_PATH, DB_SECRET_KEY



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = DB_SECRET_KEY

db = SQLAlchemy(app)

login_manager = LoginManager()

login_manager.init_app(app)


from distribuidora.core.views import core_blueprint
from distribuidora.core.gestion_usuario.views import gestion_usuario

app.register_blueprint(core_blueprint, url_prefix='/')
app.register_blueprint(gestion_usuario)
