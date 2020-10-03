from flask import Blueprint, render_template, redirect, url_for
from distribuidora import db
from distribuidora.models.gestion_usuario import Usuario, Permiso

usuario_permiso_blueprint = Blueprint('usuario_permiso', __name__, template_folder='templates')

@usuario_permiso_blueprint.route('/list/usuario')
def list_usuario():
	"""
	Nos devolverá el listado de todas los usuarios de la BD
	"""
	usuario = Usuario.query.all()
	return render_template('list_usuario.html', usuario=usuario)

@usuario_permiso_blueprint.route('/list/permiso')
def list_permiso():
	"""
	Nos devolverá el listado de todos los permisos en la BD
	"""
	permiso = Permiso.query.all()
	return render_template('list_permiso.html', permiso=permiso)