from flask import render_template, request, Blueprint, url_for, redirect
from flask_login import  current_user
from distribuidora import db
from distribuidora.models.producto import Producto, Marca, UnidadMedida, ProductoEnvase

# Definimos el Blueprint para manejas las vistas que son
# propias de la página que cualquier usuario puede ver

core_blueprint = Blueprint('core_blueprint', __name__, template_folder='templates')

def obtener_rol():
	if current_user.is_authenticated is False:
		rol = None
	else:
		rol = current_user.get_role()
	return rol


@core_blueprint.route('/')
def index():
	"""
	Nos mostrará el Home del sitio.
	"""
	rol = obtener_rol()
	print(current_user.is_authenticated, flush=True)
	return render_template('index.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=rol, \
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
	return render_template('contacto.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=rol, \
		site='Contactos')

@core_blueprint.route('/nosotros')
def nosotros():
	"""
	Nos devolverá la sección Nosotros.
	"""
	rol = obtener_rol()
	return render_template('nosotros.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=rol, \
		datos=current_user.get_mis_datos(),\
		site='Nosotros')

@core_blueprint.route('/como_comprar')
def como_comprar():
	"""
	Nos devolverá la sección Cómo Comprar.
	"""
	rol = obtener_rol()
	return render_template('como_comprar.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=rol, \
		datos=current_user.get_mis_datos(),\
		site='¿ Cómo Comparar ? ')
