from distribuidora.models.gestion_usuario import Usuario
from distribuidora.models.mensaje import Message
from distribuidora.core.mensaje.forms import MessageForm
from distribuidora.core.mensaje.helper import *
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db

msg = Blueprint('mensajes', __name__, template_folder='templates')


def cargar_errores(errores):
    """
    Pasamos el diccionario con todos los errores levantados por Flask
    """
    for key, value in errores.items():
        for v in value:
            flash(v, 'error')


@msg.route('/mensaje/listar', methods=['GET'])
@login_required
def listar_mensajes(recipient):
	msjs = Message.query.filter_by(usuario_id=current_user.get_mis_datos())
	listado = list()
	for m in msjs:
		listado.append(m.get_mensaje_dict())

	print(listado, flush=True)
	return jsonify({'status':'OK', 'msjs':listado})


@msg.route('/mensaje/nuevo', methods=['GET', 'POST'])
@login_required
def enviar_mensaje():
	form = MessageForm()
	if form.validate_on_submit():
		data = {
			'emisor': current_user.get_id(),
			'receptor': form.recipient.data,
			'body': form.body.data
		}
		
		print('data: {}'.format(data), flush=True)
		result = insert_nuevo_mensaje(data)
		if result:
			flash('El mensaje ha sido enviado correctamente', 'success')
		else:
			flash('Verifique la información ingresada', 'error')
	else:
		cargar_errores(form.errors)

	return render_template('enviar_mensaje.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='ROL', \
        site='TITULO' + ' - Nuevo Mensaje', \
        form=form)

