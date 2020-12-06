from flask import render_template, request, Blueprint, url_for, redirect
from flask_login import  current_user
from distribuidora import db
from distribuidora.models.producto import Producto, Marca, UnidadMedida, ProductoEnvase
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer
# Definimos el Blueprint para manejas las vistas que son
# propias de la página que cualquier usuario puede ver

core_blueprint = Blueprint('core_blueprint', __name__, template_folder='templates')

def obtener_rol():
	if current_user.is_authenticated is False:
		rol = None
	else:
		rol = current_user.get_role()
	return rol

def get_datos_extras():
	if current_user.is_authenticated:
		return {'datos': current_user.get_mis_datos(), \
			'sin_leer': get_cantidad_msj_sin_leer(current_user.get_id())}
	else:

		return None


@core_blueprint.route('/')
def index():
	"""
	Nos mostrará el Home del sitio.
	"""
	rol = obtener_rol()
	datos = get_datos_extras()
	sin_leer=None
	mis_datos=None
	if datos is not None:
		sin_leer=datos['sin_leer']
		mis_datos = datos['datos']
	print(current_user.is_authenticated, flush=True)
	return render_template('index.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=rol, \
		sin_leer=sin_leer,\
		datos=mis_datos,\
		site='Home')

@core_blueprint.route('/productos')
def productos():
	"""
	Nos devolverá la sección Productos.
	"""
	return redirect(url_for('producto.listar_productos'))

@core_blueprint.route('/contacto')
def contacto():
	"""
	Nos devolverá la sección Contactos.
	"""
	rol = obtener_rol()
	datos = get_datos_extras()
	sin_leer=None
	mis_datos=None
	if datos is not None:
		sin_leer=datos['sin_leer']
		mis_datos = datos['datos']
	return render_template('contacto.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=rol, \
		datos=mis_datos,\
		sin_leer=sin_leer,\
		site='Contactos')

@core_blueprint.route('/nosotros')
def nosotros():
	"""
	Nos devolverá la sección Nosotros.
	"""
	rol = obtener_rol()
	datos = get_datos_extras()
	sin_leer=None
	mis_datos=None
	if datos is not None:
		sin_leer=datos['sin_leer']
		mis_datos = datos['datos']
	return render_template('nosotros.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=rol, \
		datos=mis_datos,\
		sin_leer=sin_leer,\
		site='Nosotros')

@core_blueprint.route('/como_comprar')
def como_comprar():
	"""
	Nos devolverá la sección Cómo Comprar.
	"""
	rol = obtener_rol()
	datos = get_datos_extras()
	sin_leer=None
	mis_datos=None
	if datos is not None:
		sin_leer=datos['sin_leer']
		mis_datos = datos['datos']
	return render_template('como_comprar.html', \
		is_authenticated=current_user.is_authenticated, \
		sin_leer=sin_leer,\
		rol=rol, \
		datos=mis_datos,\
		site='¿ Cómo Comparar ? ')
