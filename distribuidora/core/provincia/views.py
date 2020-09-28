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
		print('#'*40)
		print(new_provincia)
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