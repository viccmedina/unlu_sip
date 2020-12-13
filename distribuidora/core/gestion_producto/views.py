from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from distribuidora.core.gestion_producto.forms import *
from distribuidora.core.gestion_pedido.forms import FormAgregarProducto
from distribuidora.core.gestion_pedido.helper import get_cantidad_estados_pedido, \
    get_ultimo_pedido_id, insert_into_detalle_pedido
from distribuidora.core.gestion_producto.helper import *
from distribuidora.core.mensaje.helper import get_cantidad_msj_sin_leer
from distribuidora.models.producto import Producto, Marca, ProductoEnvase, Envase, TipoProducto, \
    UnidadMedida, TipoProducto
from distribuidora.models.precio import Lista_precio_producto
from werkzeug.utils import secure_filename
from distribuidora import db, app
import os


producto = Blueprint('producto', __name__, template_folder='templates')

@producto.route('/producto', methods=['GET'])
@login_required
def index():
    if current_user.has_role('Operador'):
        return render_template('home_producto.html',\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated,\
        rol='operador',\
        sin_leer= get_cantidad_msj_sin_leer(current_user.get_id()),\
        site='Gestión de Productos')
    abort(403)

@producto.route('/consultar/producto', methods=['POST', 'GET'])
@login_required

def consultar_producto():
    if current_user.has_role('Operador'):
        id_producto = None
        id_marca = None
        id_um = None
        products = None
        form = ConsultarProducto()
        form.producto.choices = [(descripcion.descripcion) for descripcion in Producto.query.all()]
        form.marca.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
        form.uMedida.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
        if form.validate_on_submit():
            id_producto = form.producto.data
            id_marca = form.marca.data
            id_um = form.uMedida.data
            # hacer algo con los error de devolucine de id
            print("Productooo: {} ".format(products))
            # lo que voy a hacer un function boolean para validar q sean datis correcto consultando por el id
            #
            products = consult_producto(id_producto,id_marca,id_um)
            if products == -777:
                #flash("Se ha Eliminado el producto", 'warning')
                products = None
                flash("No se ha podido localizar el producto, producto invalido",'error')
            else:
                
                return render_template('form_consulta_producto.html', \
                datos=current_user.get_mis_datos(), \
                is_authenticated=current_user.is_authenticated,\
                rol='operador',\
                products=products,\
                form=form,\
                sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))


        return render_template('form_consulta_producto.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated,\
        rol='operador',\
        products=products,\
        form=form,\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()))
    abort(403)


@producto.route('/agregar/producto', methods=['POST', 'GET'])
@login_required
def agregar():
    if current_user.has_role('Operador'):
        id_producto = None
        id_marca = None
        id_um = None
        products = None
        form = AgregarProducto()
        form.marca.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
        form.uMedida.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
        form.tipo_producto.choices = [(descripcion.descripcion) for descripcion in TipoProducto.query.all()]
        form.envase.choices = [(descripcion.descripcion) for descripcion in Envase.query.all()]
        if form.validate_on_submit():
            if insert_new_producto(form.producto.data,form.marca.data,form.uMedida.data,\
            form.tipo_producto.data,form.envase.data):
                flash("Se ha ingresado un nuevo producto", 'warning')
            else:
                flash("No se ha podido crear el nuevo producto, ha surgido un error",'error')


        return render_template('form_agregar_producto.html',\
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol='operador',\
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
        products=products,\
        form=form)
    abort(403)


@producto.route('/modificar/producto', methods=['POST','GET'])
@login_required
def modificar():
    if current_user.has_role('Operador'):
        id_producto = None
        id_marca = None
        id_um = None
        products = None
        form = ModificarProducto()
        form1 = ModifProducto()
        form.producto.choices = [(descripcion.descripcion) for descripcion in Producto.query.all()]
        form.marca.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
        form.uMedida.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
        if form.validate_on_submit():
            id_producto = form.producto.data
            id_marca = form.marca.data
            id_um = form.uMedida.data
            products = consult_producto(form.producto.data,form.marca.data,form.uMedida.data)

            if products == -777:
                #flash("Se ha Eliminado el producto", 'warning')
                products = None
                flash("No se ha podido localizar el producto, producto invalido",'error')
            else:
                #form1.product.choices = [(descripcion.descripcion) for descripcion in Producto.query.all()]
                form1.marc.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
                form1.uMedid.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
                form1.envas.choices = [(descripcion.descripcion) for descripcion in Envase.query.all()]
                form1.tipo_product.choices = [(descripcion.descripcion) for descripcion in TipoProducto.query.all()]
                products = consult_producto(form.producto.data,form.marca.data,form.uMedida.data)
                for row in products:
                    form1.product.data = row['producto']

                if form1.validate_on_submit():

                    return render_template('form_modificar_product.html', \
                    datos=current_user.get_mis_datos(), \
                    sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
                    is_authenticated=current_user.is_authenticated, \
                    rol='operador',\
                    form=form,\
                    form1=form1,\
                    products=products)

    return render_template('form_modificar_producto.html', \
    datos=current_user.get_mis_datos(), \
    sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
    is_authenticated=current_user.is_authenticated, \
    rol='operador',\
    form=form,\
    form1=form1,\
    products=products)


@producto.route('/eliminar/producto', methods=['POST','GET'])
@login_required
def eliminar():
    if current_user.has_role('Operador'):
        id_producto = None
        id_marca = None
        id_um = None
        products = None
        form = EliminarProducto()
        form.producto.choices = [(descripcion.descripcion) for descripcion in Producto.query.all()]
        form.marca.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
        form.uMedida.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
        if form.validate_on_submit():
            id_producto = form.producto.data
            id_marca = form.marca.data
            id_um = form.uMedida.data
            products = consult_producto(form.producto.data,form.marca.data,form.uMedida.data)
            if products == -777:
                #flash("Se ha Eliminado el producto", 'warning')
                products = None
                flash("No se ha podido borrar el producto, producto invalido",'error')


        return render_template('form_eliminar_producto.html', \
        datos=current_user.get_mis_datos(), \
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
        is_authenticated=current_user.is_authenticated, \
        rol='operador',\
        products=products,\
        form=form)
    abort(403)


@producto.route('/exportar/producto', methods=['GET'])
@login_required
def exportar():
    if current_user.has_role('Operador'):
        id_producto = None
        id_marca = None
        id_um = None
        products = None
        form = ConsultarProducto()
        form.producto.choices = [(descripcion.descripcion) for descripcion in Producto.query.all()]
        form.marca.choices = [(descripcion.descripcion) for descripcion in Marca.query.all()]
        form.uMedida.choices = [(descripcion.descripcion) for descripcion in UnidadMedida.query.all()]
        if form.validate_on_submit():
            id_producto = form.producto.data
            id_marca = form.marca.data
            id_um = form.uMedida.data
            if form.validate_on_submit():
                if delete_producto(form.producto.data,form.marca.data,form.uMedida.data):
                    flash("Se ha Eliminado el producto", 'warning')
                else:
                    flash("No se ha podido borrar el producto, ha surgido un error",'error')

        return render_template('exportar_producto.html', \
        datos=current_user.get_mis_datos(), \
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
        is_authenticated=current_user.is_authenticated, \
        rol='operador')
    abort(403)

@producto.route('/producto/importar', methods=['POST', 'GET'])
@login_required
def importar_productos():
    if current_user.has_role('Operador'):
        print('DIRECTORIO ---- {}'.format(app.config['UPLOAD_FOLDER']))
        print('EXTENSIONES PERMITIDAS ---- {}'.format(app.config['UPLOAD_EXTENSIONS']))
        if 'file' not in request.files:
            pass
        else:
            file = request.files['file']
            filename = secure_filename(file.filename)
            print(filename)
            extension = filename.split('.')
            print('EXTENSION!!')
            print(extension[1])
            if extension[1] not in app.config['UPLOAD_EXTENSIONS']:
                flash('La extensión del archivo no es la correcta. Se aceptan: {}'.format(app.config['UPLOAD_EXTENSIONS']), 'error')
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path = app.config['UPLOAD_FOLDER'] + filename
                print('PATH: {}'.format(path))
                result = importar_productos_from_file(path)
                flash(result, 'warning')


        return render_template('importar_producto.html', \
            datos=current_user.get_mis_datos(), \
            sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
            is_authenticated=current_user.is_authenticated, \
            rol='operador', \
            site='Importar Producto')
    abort(403)


@producto.route('/listar/producto', methods=['GET', 'POST'])
@login_required
def listar_productos():
    page = request.args.get('page', 1, type=int)
    #productos = lista_de_productos().paginate(page,5,False)
    productos = db.session.query(Producto, Marca, TipoProducto,Lista_precio_producto, UnidadMedida, ProductoEnvase).filter(\
        ProductoEnvase.producto_id == Producto.producto_id).filter(\
        Producto.tipo_producto_id == TipoProducto.tipo_producto_id).filter(\
        ProductoEnvase.unidad_medida_id == UnidadMedida.unidad_medida_id).filter(\
        Producto.marca_id == Marca.marca_id).filter(\
        ProductoEnvase.producto_envase_id == Lista_precio_producto.producto_envase_id).filter(\
        ProductoEnvase.stock_real > 0).paginate( page, 5, False)


    return render_template('listar_productos.html', \
        datos=current_user.get_mis_datos(), \
        is_authenticated=current_user.is_authenticated, \
        rol=current_user.get_role(), \
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
        site='Listado de Productos', \
        producto=productos)

@producto.route('/detalle/producto', methods=['GET', 'POST'])
@login_required
def detalle_producto():
    producto = request.args.get('producto', type=str)
    marca = request.args.get('marca', type=str)
    if producto is not None and marca is not None:
        producto_id = get_producto_by_descripcion_marca(producto, marca)
    else:
        producto_envase_id = request.args.get('producto', type=int)
        producto_id = get_producto_id_from_producto_envase(producto_envase_id)
    productos = get_producto_envase_by_producto_id(producto_id[0]['producto_id'])
    print(productos, flush=True)

    form = FormAgregarProducto()
    if form.validate_on_submit():
        #obtengo los datos del cliente
        usuario_id = current_user.get_id()

        #recupero el pedido en estado pcc
        pedido_id = get_ultimo_pedido_id(usuario_id)
        print('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ')
        print(pedido_id)
        #recupero la cantidad de estados de ese pedido
        cantidad_estados = get_cantidad_estados_pedido(pedido_id)
        if cantidad_estados == 1:
            producto_id = request.args.get("producto")
            cantidad = form.cantidad.data
            insert_into_detalle_pedido(pedido_id=pedido_id, producto_envase_id=producto_envase_id, cantidad=cantidad)
            flash('Producto agregado', 'success')
    else:
        print(form.errors)
        flash(form.errors, 'errors')

    return render_template('detalle_producto.html',\
        form=form,\
        productos=productos,\
        datos=current_user.get_mis_datos(),\
        is_authenticated=current_user.is_authenticated, \
        sin_leer=get_cantidad_msj_sin_leer(current_user.get_id()),\
        rol=current_user.get_role(), \
        site='Detalle Producto')

@producto.route('/eliminar/productos', methods=['POST','GET'])
@login_required
def eliminar_producto():

    pro = request.args.get('producto')
    mar = request.args.get('marca')
    um = request.args.get('umed')

    print("producto {}".format(pro))
    print("marca {}".format(mar))
    print("umed {}".format(um))

    eli_producto(pro,mar,um)

    flash("Producto Eliminado",'warning')
    return redirect(url_for('producto.eliminar'))

@producto.route('/modificar/productos', methods=['POST','GET'])
@login_required
def modificar_producto():
    #a modificar
    pro = request.args.get('pro')
    mar = request.args.get('mar')
    umed = request.args.get('um')
    env = request.args.get('env')
    tp = request.args.get('tp')
    #ingresado por el user
    pro1 = request.args.get('pro1')
    mar1 = request.args.get('mar1')
    umed1 = request.args.get('um1')
    print("prod 1 {}".format(pro1))
    modific_producto(pro,mar,umed,env,tp,pro1,mar1,umed1)
    flash("Producto Modificado",'warning')

    return redirect(url_for('producto.modificar'))
