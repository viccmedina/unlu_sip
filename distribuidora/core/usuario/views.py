from flask import Blueprint, render_template, redirect, url_for
from distribuidora import db
from distribuidora.core.usuario.forms import AddUsuario
from distribuidora.models.domicilio import Domicilio
from distribuidora.models.localidad import Localidad
from distribuidora.models.persona import Persona
from distribuidora.models.provincia import Provincia
from distribuidora.models.tipo_dni import TipoDNI
from distribuidora.models.gestion_usuario import Usuario

usuario_blueprint = Blueprint('usuario', __name__, template_folder='templates')

@usuario_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    """
    Nos permitirá registar un nuevo usuario/cliente
    """
    form = AddUsuario()

    # Si el formulario es válido

    if form.validate_on_submit():
        #atributos persona
        apellido = form.apellido.data
        nombre = form.nombre.data
        num_dni = form.num_dni.data
        fecha_nacimiento = form.fecha_nacimiento.data
        email = form.email.data
        razon_social = form.razon_social.data
        telefono_ppal = form.telefono_ppal.data
        telefono_sec = form.telefono_sec.data
        tipo_dni = TipoDNI.query.filter_by(descripcion=form.tipo_dni.data).first()
        #atributos domicilio
        calle = form.calle.data
        numero = form.numero.data
        piso = form.piso.data
        departamento = form.departamento.data
        aclaracion = form.aclaracion.data
        localidad_id = Localidad.query.filter_by(descripcion=form.localidad.data).first()
        provincia_id = Provincia.query.filter_by(descripcion=form.provincia.data).first()

        # preguntar...
        #localidad_id1 = Localidad.query.filter_by(descripcion=form.provincia_id.data).first()

        new_domicilio = Domicilio(calle, numero, piso, departamento, aclaracion, localidad_id)#creamos un domicilio
        db.session.add(new_domicilio)
        db.session.commit()#agregamos el domicilio a la bd
        new_persona = Persona(apellido, nombre, num_dni, fecha_nacimiento, email, razon_social,
                              telefono_ppal, telefono_sec, tipo_dni, new_domicilio.domicilio_id)#creamos una persona
        db.session.add(new_persona)
        db.session.commit()#agregamos una persona a la db
        #datos del usuario
        username = form.username.data
        password = form.password.data
        persona_id = Persona.query.filter_by(descripcion=form.email.data).first()
        new_usuario = Usuario(username, password, persona_id)#creamos un nuevo usuario
        db.session.add(new_usuario)
        db.session.commit()#lo agregamos a la db

        return redirect(url_for('usuario.list'))
    else:
        print('HAY UN ERROR')
        print(form.descripcion.data)
        print(form.errors)
        return render_template('add_usuario.html', form=form)

@usuario_blueprint.route('/list')
def list():
    """
    Nos devolverá el listado de todas los usuario en la BD
    """
    usuario = Usuario.query.all()
    return render_template('list_usuarios.html', usuario=usuario)