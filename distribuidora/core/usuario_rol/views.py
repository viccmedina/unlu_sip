from flask import Blueprint, render_template, redirect, url_for
from distribuidora import db
from distribuidora.models.gestion_usuario import Usuario, Permiso

usuario_rol_blueprint = Blueprint('usuario_rol', __name__, template_folder='templates')

@usuario_rol_blueprint.route('/list/usuario')
def list_usuario():
	"""
	Nos devolverá el listado de todas los usuarios de la BD
	"""
	usuario = Usuario.query.all()
	return render_template('list_usuario.html', usuario=usuario)

@usuario_rol_blueprint.route('/list/permiso')
def list_rol():
	"""
	Nos devolverá el listado de todas los roles en la BD
	"""
	rol = Rol.query.all()
	return render_template('list_rol.html', rol=rol)