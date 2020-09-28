from flask import Blueprint, render_template, redirect, url_for
from distribuidora import db
from distribuidora.models.provincia import Provincia
from distribuidora.models.localidad import Localidad
from distribuidora.core.localidad.forms import AddLocalidad


localidad_blueprint = Blueprint('localidad', __name__, template_folder='templates')

@localidad_blueprint.route('/add', methods=['GET', 'POST'])
def add():
	"""
	Nos permitirá agregar una nueva localidad
	"""
	form = AddLocalidad()

	# Si el formulario es válido
	if form.validate_on_submit():
		descripcion = form.descripcion.data
		provincia = Provincia.query.filter_by(descripcion=form.provincia.data).first()
		print('#'*40)
		print(form.provincia.data)
		print(provincia)
		print(provincia.provincia_id)
		new_localidad = Localidad(descripcion, provincia.provincia_id)
		db.session.add(new_localidad)
		db.session.commit()
		return redirect(url_for('localidad.list'))
	else:
		print('HAY UN ERROR')
		print(form.descripcion.data)
		print(form.errors)
	return render_template('add_localidad.html', form=form)

@localidad_blueprint.route('/list')
def list():
	"""
	Nos devolverá el listado de todas las localidades en la BD
	"""
	localidad = Localidad.query.all()
	return render_template('list_localidad.html', localidad=localidad)