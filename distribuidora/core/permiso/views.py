from flask import Blueprint, render_template, redirect, url_for
from distribuidora import db
from distribuidora.core.permiso.forms import AddPermiso
from distribuidora.models.gestion_usuario import Permiso

permiso_blueprint = Blueprint('permiso', __name__, template_folder='templates')

@permiso_blueprint.route('/add', methods=['GET', 'POST'])
def add():
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
        return redirect(url_for('permiso.list'))
    else:
        print('HAY UN ERROR')
        print(form.descripcion.data)
        print(form.errors)
        return render_template('add_permiso.html', form=form)

@permiso_blueprint.route('/list')
def list():
    """
        Nos devolverá el listado de todas las localidades en la BD
    """
    permiso = Permiso.query.all()
    return render_template('list_permiso.html', permiso=permiso)