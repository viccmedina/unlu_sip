from flask import Blueprint, render_template, redirect, url_for
from distribuidora import db
from distribuidora.models.domicilio import Domicilio


domicilio_blueprint = Blueprint('domicilio', __name__, template_folder='templates')

@domicilio_blueprint.route('/list')
def list():
	"""
	Nos devolverá el listado de todas las localidades en la BD
	"""
	domicilio = Domicilio.query.all()
	return render_template('list_domicilio.html', domiclio=domicilio)