from flask import render_template, request, Blueprint

# Definimos el Blueprint para manejas las vistas que son
# propias de la página que cualquier usuario puede ver

core_blueprint = Blueprint('core_blueprint', __name__, template_folder='templates')

@core_blueprint.route('/')
def index():
	"""
	Nos mostrará el Home del sitio.
	"""

	return render_template('index.html')

@core_blueprint.route('/productos')
def productos():
	"""
	Nos devolverá la sección Productos.
	"""

	return render_template('productos.html')

@core_blueprint.route('/contacto')
def contacto():
	"""
	Nos devolverá la sección Contactos.
	"""

	return render_template('contacto.html')

@core_blueprint.route('/nosotros')
def nosotros():
	"""
	Nos devolverá la sección Nosotros.
	"""

	return render_template('nosotros.html')

@core_blueprint.route('/como_comprar')
def como_comprar():
	"""
	Nos devolverá la sección Cómo Comprar.
	"""

	return render_template('como_comprar.html')

