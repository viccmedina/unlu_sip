from flask import Blueprint, render_template, redirect, url_for
from distribuidora import db
from distribuidora.models.tipo_dni import TipoDNI

tipo_dni_blueprint = Blueprint('tipo_dni', __name__, template_folder='templates')

@tipo_dni_blueprint.route('/list')
def list():
	"""
	Nos devolverá el listado de todas las localidades en la BD
	"""
	tipo_dni = TipoDNI.query.all()
	return render_template('list_tipo_dni.html', tipo_dni=tipo_dni)