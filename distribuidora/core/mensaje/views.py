from distribuidora.models.gestion_usuario import Usuario
from distribuidora.models.mensaje import Message
from distribuidora.core.mensaje.forms import MessageForm
from distribuidora.core.mensaje.helper import *
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora import db
import json

msg = Blueprint('mensajes', __name__, template_folder='templates')


def cargar_errores(errores):
    """
    Pasamos el diccionario con todos los errores levantados por Flask
    """
    for key, value in errores.items():
        for v in value:
            flash(v, 'error')


@msg.route('/mensaje/index', methods=['GET'])
@login_required
def index():
	return render_template('mensajeria.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='ROL', \
        site='Mensajería', \
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))

@msg.route('/mensaje/listar', methods=['GET'])
@login_required
def listar_mensajes():
	
	#print(msjs, flush=True)
	msj_sin_leer = request.args.get('msj_leido', None)

	if msj_sin_leer is not None:
		print('°'*100, flush=True)
		msj_sin_leer = msj_sin_leer.replace("\'", "\"")
		print(msj_sin_leer, flush=True)
		print(type(msj_sin_leer), flush=True)
		msj_sin_leer = json.loads(msj_sin_leer)
		result = update_read_mensaje(msj_sin_leer['id'])
		print(result)
	
	usuarios_id = current_user.get_id()
	msjs = get_mensajes(usuarios_id)
	
	return render_template('mis_mensajes.html', datos=msjs)


@msg.route('/mensaje/nuevo', methods=['GET', 'POST'])
@login_required
def enviar_mensaje():
	form = MessageForm()
	if form.validate_on_submit():
		data = {
			'emisor': current_user.get_id(),
			'receptor': form.recipient.data,
			'body': form.message.data
		}
		
		print('data: {}'.format(data), flush=True)
		result = insert_nuevo_mensaje(data)
		#result = True
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
        site='Mensajería' + ' - Nuevo Mensaje', \
        form=form, \
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))