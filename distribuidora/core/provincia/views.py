from flask import Blueprint, render_template, redirect, url_for
from distribuidora import db
from distribuidora.models.provincia import Provincia
from distribuidora.core.provincia.forms import AddProvincia


provincia_blueprint = Blueprint('provincia', __name__, template_folder='templates')

@provincia_blueprint.route('/add', methods=['GET', 'POST'])
def add():
	"""
	Nos permitirá agregar una nueva provincia
	"""
	form = AddProvincia()

	# Si el formulario es válido
	if form.validate_on_submit():
		descripcion = form.descripcion.data

		new_provincia = Provincia(descripcion)
		db.session.add(new_provincia)
		db.session.commit()
		return redirect(url_for('provincia.list'))
	else:
		print('HAY UN ERROR')
		print(form.descripcion.data)
		print(form.errors)
	return render_template('add_provincia.html', form=form)

@provincia_blueprint.route('/list')
def list():
	"""
	Nos devolverá el listado de todas las provincias en la BD
	"""
	provincia = Provincia.query.all()
	return render_template('list_provincia.html', provincia=provincia)

# TODO:: esto debe estar dentro de usuario_persona. 
# para probar lo pongo aca
@provincia_blueprint.route('/home_cliente')
def home_cliente():
	panel = []
	mock_data = {
		'titulo': 'Gestionar Nuevo Pedido',
		'subtitulo': 'Nuevo Pedido',
		'descripcion': 'Esto es una descripcion',
		'boton': 'Nuevo Pedido'
	}

	panel.append(mock_data)
	mock_data = {
		'titulo': 'Gestionar Nuevo Pedido 2',
		'subtitulo': 'Nuevo Pedido 2',
		'descripcion': 'Esto es una descripcion 2',
		'boton': 'Nuevo Pedido 2'
	}
	panel.append(mock_data)

	collapse = []
	mock_data = {
	'titulo': 'Mis Datos',
	'contenido': 'Estos son datos de Prueba'
	}
	collapse.append(mock_data)
	
	mock_data = {
	'titulo': 'Mis Datos',
	'contenido': 'Estos son datos de Prueba'
	}

	mock_data = {
	'titulo': 'Pedidos Guardados',
	'contenido': None
	}
	collapse.append(mock_data)

	datos = {
		'accesos_rapidos': panel,
		'collapse': collapse
	}
	return render_template('home_cliente.html', datos=datos)