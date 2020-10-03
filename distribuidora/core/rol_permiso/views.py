from flask import Blueprint, render_template
from distribuidora.models.gestion_usuario import Rol, Permiso

rol_permiso_blueprint = Blueprint('rol_permiso', __name__, template_folder='templates')

@rol_permiso_blueprint.route('/list/rol')
def list_rol():
	"""
	Nos devolverá el listado de todas las localidades en la BD
	"""
	rol = Rol.query.all()
	return render_template('list_rol.html', rol=rol)

@rol_permiso_blueprint.route('/list/permiso')
def list_permiso():
	"""
	Nos devolverá el listado de todas las localidades en la BD
	"""
	permiso = Permiso.query.all()
	return render_template('list_permiso.html', permiso=permiso)