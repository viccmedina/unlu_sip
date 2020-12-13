from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from distribuidora.settings import DB_PATH, DB_SECRET_KEY, FILE_PATH



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = DB_SECRET_KEY
app.config['UPLOAD_EXTENSIONS'] = ['csv']
app.config['UPLOAD_FOLDER'] = FILE_PATH

db = SQLAlchemy(app)

login_manager = LoginManager()

login_manager.init_app(app)


from distribuidora.core.views import core_blueprint
from distribuidora.core.gestion_usuario.views import gestion_usuario
from distribuidora.core.gestion_stock.views import stock
from distribuidora.core.gestion_cta_corriente.views import cta_corriente
from distribuidora.core.gestion_producto.views import producto
from distribuidora.core.gestion_lista_precio.views import lista_precio
from distribuidora.core.gestion_pedido.views import pedido
from distribuidora.core.gestion_devolucion.views import devolucion
from distribuidora.core.gestion_informes.views import informe
from distribuidora.core.mensaje.views import msg
from distribuidora.core.error_handler.handler import error_pages
from distribuidora.core.gestion_devolucion.views import devolucion

app.register_blueprint(msg)
app.register_blueprint(devolucion)
app.register_blueprint(error_pages)
app.register_blueprint(stock)
app.register_blueprint(core_blueprint, url_prefix='/')
app.register_blueprint(gestion_usuario)
app.register_blueprint(cta_corriente)
app.register_blueprint(producto)
app.register_blueprint(devolucion)
app.register_blueprint(lista_precio)
app.register_blueprint(pedido)
app.register_blueprint(informe)
