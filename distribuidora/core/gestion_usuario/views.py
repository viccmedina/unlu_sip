from flask import Blueprint, render_template, redirect, url_for
from distribuidora import db
from distribuidora.models.gestion_usuario import Rol, Permiso, Usuario
from distribuidora.core.gestion_usuario.forms import AddPermiso, AddRol, AddUsuario

gestion_usuario_blueprint = Blueprint('usuario', __name__, template_folder='templates')

@gestion_usuario_blueprint.route('/add/rol', methods=['GET', 'POST'])
def add_rol():
    """
    Nos permitirá agregar un nuevo rol
    """
    form = AddRol()
    # Si el formulario es válido
    if form.validate_on_submit():
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        new_rol = Rol(nombre, descripcion)
        db.session.add(new_rol)
        db.session.commit()
        return redirect(url_for('list.rol'))
    else:
        print('HAY UN ERROR')
        print(form.descripcion.data)
        print(form.errors)
        return render_template('add_rol.html', form=form)

@gestion_usuario_blueprint.route('/list/rol')
def list_rol():
    """
        Nos devolverá el listado de todos los roles en la BD
    """
    rol = Rol.query.all()
    return render_template('list_rol.html', rol=rol)

@gestion_usuario_blueprint.route('/add/permiso', methods=['GET', 'POST'])
def add_permiso():
	"""
	Nos permitirá agregar un nuevo permiso
	"""
	form = AddPermiso()
	# Si el formulario es válido
	if form.validate_on_submit():
	    nombre = form.nombre.data
	    descripcion = form.descripcion.data
	    new_permiso = Permiso(nombre, descripcion)
	    db.session.add(new_permiso)
	    db.session.commit()
	    return redirect(url_for('list.permiso'))
	else:
	    print('HAY UN ERROR')
	    print(form.descripcion.data)
	    print(form.errors)
	    return render_template('add_permiso.html', form=form)

@gestion_usuario_blueprint.route('/list/permiso', methods=['GET', 'POST'])
def list_permiso():
	"""
	    Nos devolverá el listado de todas las localidades en la BD
	"""
	permiso = Permiso.query.all()
	return render_template('list_permiso.html', permiso=permiso)

@gestion_usuario_blueprint.route('/add/usuario', methods=['GET', 'POST'])
def add_usuario():
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
        #agregamos el domicilio a la bd
        db.session.commit()
        new_persona = Persona(apellido, nombre, num_dni, fecha_nacimiento, email, razon_social,
                              telefono_ppal, telefono_sec, tipo_dni, new_domicilio.domicilio_id)#creamos una persona
        db.session.add(new_persona)
        #agregamos una persona a la db
        db.session.commit()
        #datos del usuario
        username = form.username.data
        password = form.password.data
        persona_id = Persona.query.filter_by(email=form.email.data).first()
        #creamos un nuevo usuario
        new_usuario = Usuario(username, password, persona_id)
        db.session.add(new_usuario)
        #lo agregamos a la db
        db.session.commit()

        return redirect(url_for('usuario.list'))
    else:
        print('HAY UN ERROR')
        print(form.errors)
        return render_template('add_usuario.html', form=form)

@gestion_usuario_blueprint.route('/list/usuario')
def list_usuario():
    """
    Nos devolverá el listado de todas los usuario en la BD
    """
    usuario = Usuario.query.all()
    return render_template('list_usuario.html', usuario=usuario)