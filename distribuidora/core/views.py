from flask import render_template, request, Blueprint
from flask_login import  current_user

# Definimos el Blueprint para manejas las vistas que son
# propias de la página que cualquier usuario puede ver

core_blueprint = Blueprint('core_blueprint', __name__, template_folder='templates')

@core_blueprint.route('/')
def index():
	"""
	Nos mostrará el Home del sitio.
	"""
	print(current_user.is_authenticated, flush=True)
	return render_template('index.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=current_user.get_role())

@core_blueprint.route('/productos')
def productos():
	"""
	Nos devolverá la sección Productos.
	"""
	return render_template('productos.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=current_user.get_role())

@core_blueprint.route('/contacto')
def contacto():
	"""
	Nos devolverá la sección Contactos.
	"""

	return render_template('contacto.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=current_user.get_role())

@core_blueprint.route('/nosotros')
def nosotros():
	"""
	Nos devolverá la sección Nosotros.
	"""

	return render_template('nosotros.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=current_user.get_role())

@core_blueprint.route('/como_comprar')
def como_comprar():
	"""
	Nos devolverá la sección Cómo Comprar.
	"""

	return render_template('como_comprar.html', \
		is_authenticated=current_user.is_authenticated, \
		rol=current_user.get_role())

