from flask import Blueprint, render_template, redirect, url_for
from distribuidora import db
from distribuidora.models.domicilio import Domicilio
from distribuidora.models.localidad import Localidad
from distribuidora.models.persona import Persona
from distribuidora.core.persona.forms import AddLocalidad
from distribuidora.models.tipo_dni import TipoDNI

persona_blueprint = Blueprint('persona', __name__, template_folder='templates')

@persona_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    """
    Nos permitirá agregar una nueva persona/cliente
    """
    form = AddLocalidad()

    # Si el formulario es válido
    if form.validate_on_submit():
        apellido = form.apellido.data
        nombre = form.nombre.data
        num_dni = form.num_dni.data
        fecha_nacimiento = form.fecha_nacimiento.data
        email = form.email.data
        razon_social = form.razon_social.data
        telefono_ppal = form.telefono_ppal.data
        telefono_sec = form.telefono_sec.data
        tipo_dni = TipoDNI.query.filter_by(descripcion=form.tipo_dni.data).first()

        calle = form.calle.data
        numero = form.numero.data
        piso = form.piso.data
        departamento = form.departamento.data
        aclaracion = form.aclaracion.data
        localidad_id = Localidad.query.filter_by(descripcion=form.localidad.data).first()
        new_domicilio = Domicilio(calle,numero,piso,departamento,aclaracion,localidad_id)
        db.session.add(new_domicilio)
        db.session.commit()
        new_persona = Persona(apellido,nombre,num_dni,fecha_nacimiento,email,razon_social,telefono_ppal,telefono_sec,tipo_dni,new_domicilio.domicilio_id)
        db.session.add(new_persona)
        db.session.commit()
        return redirect(url_for('persona.list'))
    else:
        print('HAY UN ERROR')
        print(form.descripcion.data)
        print(form.errors)
        return render_template('add_persona.html', form=form)

@persona_blueprint.route('/list')
def list():
	"""
	Nos devolverá el listado de todas las personas en la BD
	"""
	persona = Persona.query.all()