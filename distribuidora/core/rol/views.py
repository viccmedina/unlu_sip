from flask import Blueprint, render_template, redirect, url_for
from distribuidora import db
from distribuidora.core.permiso.forms import AddPermiso
from distribuidora.core.rol.forms import AddRol
from distribuidora.models.gestion_usuario import Permiso, Rol

rol_blueprint = Blueprint('rol', __name__, template_folder='templates')

@rol_blueprint.route('/add', methods=['GET', 'POST'])
def add():
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
        return redirect(url_for('rol.list'))
    else:
        print('HAY UN ERROR')
        print(form.descripcion.data)
        print(form.errors)
        return render_template('add_rol.html', form=form)

@rol_blueprint.route('/list')
def list():
    """
        Nos devolverá el listado de todos los roles en la BD
    """
    rol = Permiso.query.all()
    return render_template('list_rol.html', rol=rol)