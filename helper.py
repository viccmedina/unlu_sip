# Importamos la instancia de la DB
from distribuidora import db

# Importamos los modelos
from distribuidora.models.provincia import Provincia
from distribuidora.models.localidad import Localidad
from distribuidora.models.tipo_dni import TipoDNI
from distribuidora.models.gestion_usuario import Usuario, Rol, Permiso
from distribuidora.models.domicilio import Domicilio
from distribuidora.models.persona import Persona
from distribuidora.models.cuenta_corriente import TipoMovimientoCtaCorriente, \
	CuentaCorriente, MovimientoCtaCorriente, EstadoCtaCorriente, ComprobantePago, \
    EstadoComprobantePago
from distribuidora.models.producto import Marca, TipoProducto, Envase, UnidadMedida, \
	Producto, ProductoEnvase
from distribuidora.models.precio import Lista_precio, Lista_precio_producto
from distribuidora.models.pedido import PedidoEstado, DetallePedido, Pedido, \
	HistorialPedidoEstado
from distribuidora.models.devolucion import EstadoDevolucion, Devolucion, DetalleDevolucion
from distribuidora.models.stock import TipoMovimientoStock, Movimiento_Stock
from distribuidora.query import CREATE_TRIGGER_BUmov_stock, CREATE_TRIGGER_BIPedido, \
CREATE_TRIGGER_BU_Pedido, CREATE_TRIGGER_BU_Pedido2

# Importamos settings
from distribuidora.settings import DB_PATH, DATOS_PATH

# Libería de Python
from pathlib import Path
from datetime import datetime

# Librería del OS
import os
import csv

# Verificamos que la base de datos exista

if Path(DB_PATH).exists():
    print('La Base Existe, será eliminada y vuelta a generar')
    os.remove(DB_PATH)
    open(DB_PATH, 'w')
else:
    print('La Base NO existe, se generará el archivo en: {}'.format(DB_PATH))

db.create_all()
db.session.commit()

print('Base de Datos Creada')

print('#'*60)

print('Se comienza la carga de del juego de datos DEMO')


def insertar_tipo_dni():
	print('Importando Modelo TipoDNI')
	tipos = []
	with open(DATOS_PATH + 'tipo_dni.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			tipo_dni = TipoDNI(descripcion=row['descripcion'])
	tipos.append(tipo_dni)
	db.session.add_all(tipos)
	db.session.commit()


def insertar_provincias():
	print('Importando Modelo Provincias')
	lista_prov = []
	# Abrimos el archivo csv de Provincias
	with open(DATOS_PATH + 'provincia.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		# Por cada una de las filas que existene en el archivos,
		# vamos a crear un registro en la base
		for row in csv_reader:
			# Dado que row es un diccionario, podemos acceder a sus campos
			# como cualquier diccionario en Python
			# Creamos el objeto Provincia y lo guardamos
			new_provincia = Provincia(descripcion=row['descripcion'])
	lista_prov.append(new_provincia)
	db.session.add_all(lista_prov)
	db.session.commit()


def insertar_localidades():
	print('Importando Modelo Localidades')
	lista_loc = []
	# Abrimos el archivo csv de Localidades
	with open(DATOS_PATH + 'localidad.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			new_localidad = Localidad(descripcion=row['descripcion'], provincia_id=row['provincia_id'])
			lista_loc.append(new_localidad)
	db.session.add_all(lista_loc)
	db.session.commit()


def insertar_roles():
	print('Importando Modelo Rol')
	lista_rol = []
	with open(DATOS_PATH + 'rol.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			new_rol = Rol(nombre=row['nombre'], descripcion=row['descripcion'])
			lista_rol.append(new_rol)
	db.session.add_all(lista_rol)
	db.session.commit()


def insertar_permisos():
	print('Importando Modelo Permiso')
	lista_permiso =	[]
	with open(DATOS_PATH + 'permiso_rol.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			rol = Rol.query.filter_by(nombre=row['rol']).first()
			new_permiso = Permiso(nombre=row['nombre'], descripcion=row['descripcion'])
			new_permiso.rol_permiso.append(rol)
			lista_permiso.append(new_permiso)
	db.session.add_all(lista_permiso)
	db.session.commit()


def insertar_personas():
	print('Importando Modelo Persona')
	lista_persona =	[]
	with open(DATOS_PATH + 'persona.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			new_persona = Persona(nombre=row['nombre'], apellido=row['apellido'], \
			email=row['email'], telefono_ppal=row['telefono_principal'])

			lista_persona.append(new_persona)
	db.session.add_all(lista_persona)
	db.session.commit()


def insertar_usuarios():
	print('Importando Modelo Usuario')
	lista_usuario =	[]
	cta_corriente = []
	with open(DATOS_PATH + 'usuario.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			rol = Rol.query.filter_by(nombre=row['rol']).first()
			persona = Persona.query.filter_by(email=row['persona']).first()
			new_usuario = Usuario(username=row['username'], password=row['password'], \
			persona_id=persona.persona_id)
			new_usuario.usuario_rol.append(rol)
			lista_usuario.append(new_usuario)
	db.session.add_all(lista_usuario)
	db.session.add_all(cta_corriente)
	db.session.commit()


def insertar_tipo_movimiento_cta_corriente():
	"""
	Nos permite ingresar de forma masiva los tipos de movimientos
	que vamos a manejar dentro de las cuentas corrientes.
	"""
	print('Importando Modelo Tipos de Movimientos de Cuenta Corriente')
	tipos_movimientos =	[]
	with open(DATOS_PATH + 'tipo_movimiento_cta_corriente.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			tm = TipoMovimientoCtaCorriente(descripcion=row['descripcion'], \
			descripcion_corta=row['descripcion_corta'])
			tipos_movimientos.append(tm)
	db.session.add_all(tipos_movimientos)
	db.session.commit()


def insertar_cuenta_corriente():
	"""
	Nos permite ingresar una cuenta corriente.
	En este caso solamente será el único cliente por default.
	"""
	print('Importando Modelo de Cuenta Corriente')
	cuentas = []
	with open(DATOS_PATH + 'cta_corriente.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			c = CuentaCorriente(persona_id=row['persona_id'],
			estado_cta_corriente_id=row['estado_cta_corriente_id'])
			cuentas.append(c)
	db.session.add_all(cuentas)
	db.session.commit()


def insertar_movimientos_cta_corriente():
	"""
	Nos permite ingresar de forma masiva los movimientos
	de las cuentas corrientes.
	"""
	print('Importando Modelo Movimientos de Cuenta Corriente')
	movimientos = []
	descripcion = 'Mov Demo'
	with open(DATOS_PATH + 'movimiento_cta_corriente.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			usuario = Usuario.query.get(row['usuario_registrador'])
			tm = TipoMovimientoCtaCorriente.query.filter_by(descripcion=row['tipo_movimiento_cta_corriente']).first()
			cta_corriente = CuentaCorriente.query.get(row['cta_corriente'])
			if row['tipo_movimiento_cta_corriente'] == 'Deuda':
				saldo = float(row['saldo']) * (-1)
			else:
				saldo = float(row['saldo'])
			m = MovimientoCtaCorriente(descripcion=descripcion, usuario=usuario.id, tipo_movimiento_cta_corriente=tm.id, \
			cta_corriente=cta_corriente.cuenta_corriente_id, saldo=saldo)
			movimientos.append(m)
	db.session.add_all(movimientos)
	db.session.commit()


def insertar_estado_pedido():
	print('Importando Modelo de Estados de Pedidos')
	estados = []
	with open(DATOS_PATH + 'tipo_estado_pedido.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			tipos_estado_pedido = PedidoEstado(descripcion=row['descripcion'], descripcion_corta=row['descripcion_corta'], orden=row['orden'])

			estados.append(tipos_estado_pedido)
	db.session.add_all(estados)
	db.session.commit()


def parser_result(result):
    resp = []
    for row in result:
        resp.append(dict(row))
    return resp[0]


def insertar_datos_demo_producto():
	print('INSERTANDO PRODUCTO')
	QUERY_PRODUCTO = """ INSERT INTO producto (descripcion, tipo_producto_id, marca_id) VALUES """
	SELECT_MARCA = """ SELECT * FROM marca WHERE descripcion='{}'"""
	SELECT_TIPO_PRODUCTO = """ SELECT * FROM tipo_producto WHERE descripcion='{}'"""
	producto = list()
	with open(DATOS_PATH + 'datos_demo.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			if row['PRODUCTO'] not in producto:
				producto.append(row['PRODUCTO'])
				marca = db.engine.execute(SELECT_MARCA.format(row['MARCA']))
				marca = parser_result(marca)
				tipo_producto = db.engine.execute(SELECT_TIPO_PRODUCTO.format(row['TIPO_PRODUCTO']))
				tipo_producto=parser_result(tipo_producto)
				QUERY_PRODUCTO += "('{}', '{}', '{}'),".format(row['PRODUCTO'],\
					tipo_producto['tipo_producto_id'], marca['marca_id'])
	db.engine.execute(QUERY_PRODUCTO[:-1] + ';')


def insertar_datos_demo_producto_envase():
	#producto_id, envase_id, unidad_medida_id,stock_real
	print('INSERTANDO PRODUCTO ENVASE')
	QUERY_PRODUCTO_ENVASE = """ INSERT INTO producto_envase (producto_id, envase_id,unidad_medida_id, stock_real) VALUES """
	f_desde = datetime.strptime('15/06/2020', "%d/%m/%Y")
	f_hasta = datetime.strptime('15/06/2021', "%d/%m/%Y")
	QUERY_LISTA_PRECIO = """INSERT INTO lista_precio (fecha_desde, fecha_hasta) VALUES ('{}', '{}');""".\
		format(f_desde, f_hasta)
	db.engine.execute(QUERY_LISTA_PRECIO)
	lista_precio = '1'
	id_producto_envase = 1
	QUERY_PRECIO = """ INSERT INTO lista_precio_producto (producto_envase_id, precio_id, precio, fecha_inicio, fecha_fin) VALUES """
	SELECT_ENVASE = """ SELECT * FROM envase WHERE descripcion='{}'"""
	SELECT_PRODUCTO = """ SELECT * FROM producto WHERE descripcion='{}'"""
	SELECT_TIPO_UNIDAD_MEDIDA = """ SELECT * FROM unidad_medida WHERE descripcion='{}'"""
	with open(DATOS_PATH + 'datos_demo.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			envase = db.engine.execute(SELECT_ENVASE.format(row['ENVASE']))
			envase = parser_result(envase)
			producto = db.engine.execute(SELECT_PRODUCTO.format(row['PRODUCTO']))
			producto = parser_result(producto)
			unidad_medida = db.engine.execute(SELECT_TIPO_UNIDAD_MEDIDA.format(row['UNIDAD']))
			unidad_medida = parser_result(unidad_medida)
			QUERY_PRODUCTO_ENVASE += "('{}', '{}', '{}', '{}'),".format(producto['producto_id'],\
				envase['envase_id'], unidad_medida['unidad_medida_id'], row['CANTIDAD'])
			# producto_envase_id, precio_id, precio, fecha_inicio, fecha_fin
			QUERY_PRECIO += "('{}', '{}', '{}', '{}', '{}'),".format(id_producto_envase, lista_precio,\
				row['PRECIO'], f_desde, f_hasta)
			id_producto_envase += 1
	db.engine.execute(QUERY_PRODUCTO_ENVASE[:-1] + ';')
	db.engine.execute(QUERY_PRECIO[:-1] + ';')


def insertar_estado_devolucion():
	print('Importando Modelo Estados de la devolucion')
	estado_devolucion = []
	with open(DATOS_PATH + 'estado_devolucion.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			new_estado_devolucion = EstadoDevolucion(descripcion=row['descripcion'])
			estado_devolucion.append(new_estado_devolucion)
	db.session.add_all(estado_devolucion)
	db.session.commit()


def insertar_estado_cta_corriente():
	print('Importando Modelo de Estados de las cuentas corrientes')
	estado_cta_corriente = []
	with open(DATOS_PATH + 'estado_cta_corriente.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			new_estado_cta_corriente = EstadoCtaCorriente(descripcion=row['descripcion'],
			descripcion_corta=row['descripcion_corta'])
			estado_cta_corriente.append(new_estado_cta_corriente)
	db.session.add_all(estado_cta_corriente)
	db.session.commit()


def insertar_tipo_movimiento_stock():
	print('Importando Modelo de Tipo de moviemientos de stock')
	tipo_movimiento_stock = []
	with open(DATOS_PATH + 'tipo_movimiento_stock.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			new_tipo_movimiento_stock = TipoMovimientoStock(descripcion=row['descripcion'],
			descripcion_corta=row['descripcion_corta'])
			tipo_movimiento_stock.append(new_tipo_movimiento_stock)
	db.session.add_all(tipo_movimiento_stock)
	db.session.commit()


def insertar_pedido():
	print('Importando Modelo Pedido')
	pedido = []
	with open(DATOS_PATH + 'pedido.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('-'*50)
			new_pedido = Pedido(usuario_id=row['usuario_id'],estado_pedido_id=row['estado_pedido_id'])
			pedido.append(new_pedido)
	db.session.add_all(pedido)
	db.session.commit()



def insertar_historial_estado_pedido():
	print('Importando Modelo estadoPedido_pedido')
	estadoP_pedido = []
	with open(DATOS_PATH + 'estado_Pedido_PEDIDO.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			new_estadoP_pedido = HistorialPedidoEstado(pedido_estado_id=row['estado_pedido_id'],\
			pedido_id=row['pedido_id'])
	estadoP_pedido.append(new_estadoP_pedido)
	db.session.add_all(estadoP_pedido)
	db.session.commit()


def insertar_detalle_pedido():
	print('Importando Modelo Detalle de Pedido')
	detalle_pedido = []
	with open(DATOS_PATH + 'detalle_pedido.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			new_detalle_pedido = DetallePedido(pedido_id=row['pedido_id'],\
			producto_envase_id = row['producto_envase_id'],cantidad = row['cantidad'])
			detalle_pedido.append(new_detalle_pedido)
	db.session.add_all(detalle_pedido)
	db.session.commit()



def insertar_movimiento_stock():
	print('Importando Modelo movimiento de Stock')
	movimiento_stock = []
	with open(DATOS_PATH + 'movimiento_stock.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			new_movimiento_stock = Movimiento_Stock(detalle_pedido_id=row['detalle_pedido_id'],
			detalle_devolucion_id=row['detalle_devolucion_id'],
			tipo_movimiento_stock_id=row['tipo_movimiento_stock_id'],usuario_id=row['usuario_id'],
			producto_envase_id=row['producto_envase_id'],descripcion=row['descripcion'],
			cantidad=row['cantidad'])
			movimiento_stock.append(new_movimiento_stock)
	db.session.add_all(movimiento_stock)
	db.session.commit()



def insertar_comprobante_pago():
	print('Importando Modelo Comprobante de Pago')
	comprobante_pago = []
	with open(DATOS_PATH + 'comprobante_pago.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('-'*50)
			f_pago = datetime.strptime(row['fecha_pago'], "%d/%m/%Y")
			new_comprobante_pago = ComprobantePago(monto=row['monto'],
			pedido_id=row['pedido_id'],movimiento=row['movimiento_cta_corriente_id'],fecha_pago=f_pago)
			comprobante_pago.append(new_comprobante_pago)
	db.session.add_all(comprobante_pago)
	db.session.commit()



def insertar_devolucion():
	print('Importando Modelo Devoluciones')
	devolucion = []
	with open(DATOS_PATH + 'devolucion.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('-'*50)
			new_devolucion = Devolucion(descripcion=row['descripcion'],
			pedido_id=row['pedido_id'],estado_devolucion_id=row['estado_devolucion_id'])
			devolucion.append(new_devolucion)
	db.session.add_all(devolucion)
	db.session.commit()


def insertar_triggers():
	db.engine.execute(CREATE_TRIGGER_BUmov_stock)
	#db.engine.execute(CREATE_TRIGGER_BIPedido)
	db.engine.execute(CREATE_TRIGGER_BU_Pedido)




def insertar_detalle_devolucion():
	print('Importando Modelo Detalle de Devoluciones')
	detalle_devolucion = []
	with open(DATOS_PATH + 'detalle_devolucion.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('-'*50)
			new_detalle_devolucion = DetalleDevolucion(devolucion_id=row['devolucion_id'],
			producto_id=row['producto_id'],cantidad=row['cantidad'])
			detalle_devolucion.append(new_detalle_devolucion)
	db.session.add_all(detalle_devolucion)
	db.session.commit()


def insertar_estado_comprobante_pago():
	print('Insertando estados para el comprobante de pago')
	estados = list()
	e = EstadoComprobantePago('Adeuda', 'A')
	estados.append(e)
	e = EstadoComprobantePago('Pagado', 'P')
	estados.append(e)
	db.session.add_all(estados)
	db.session.commit()



def insertar_datos_demo():
	print('Insertando datos demo')

	QUERY_MARCA = """ INSERT INTO marca (descripcion) VALUES """
	QUERY_UNIDAD_MEDIDA = """ INSERT INTO unidad_medida (descripcion) VALUES """
	QUERY_ENVASE= """ INSERT INTO envase (descripcion) VALUES """
	QUERY_TIPO_PRODUCTO= """ INSERT INTO tipo_producto (descripcion) VALUES """
	envases = list()
	marcas = list()
	tipo_producto = list()
	unidad_medida = list()
	with open(DATOS_PATH + 'datos_demo.csv') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			for row in csv_reader:
				if row['MARCA'] not in marcas:
					marcas.append(row['MARCA'])
					QUERY_MARCA += "('{}'),".format(row['MARCA'])
				if row['UNIDAD'] not in unidad_medida:
					unidad_medida.append(row['UNIDAD'])
					QUERY_UNIDAD_MEDIDA += "('{}'),".format(row['UNIDAD'])
				if row['ENVASE'] not in envases:
					envases.append(row['ENVASE'])
					QUERY_ENVASE += "('{}'),".format(row['ENVASE'])
				if row['TIPO_PRODUCTO'] not in tipo_producto:
					tipo_producto.append(row['TIPO_PRODUCTO'])
					QUERY_TIPO_PRODUCTO += "('{}'),".format(row['TIPO_PRODUCTO'])

			print(QUERY_MARCA[:-1] + ';')
	db.engine.execute(QUERY_MARCA[:-1] + ';')
	db.engine.execute(QUERY_UNIDAD_MEDIDA[:-1] + ';')
	db.engine.execute(QUERY_ENVASE[:-1] + ';')
	db.engine.execute(QUERY_TIPO_PRODUCTO[:-1] + ';')


if __name__ == '__main__':
	
	insertar_datos_demo()
	insertar_datos_demo_producto()
	insertar_datos_demo_producto_envase()

	insertar_provincias()
	print('#'*50)
	insertar_localidades()
	print('#'*50)
	insertar_roles()
	print('#'*50)
	insertar_permisos()
	print('#'*50)
	insertar_personas()
	print('#'*50)
	insertar_usuarios()
	print('#'*50)
	insertar_tipo_movimiento_cta_corriente()
	print('#'*50)
	insertar_estado_pedido()
	print('#'*50)
	insertar_tipo_dni()
	print('#'*50)
	insertar_cuenta_corriente()
	print('#'*50)
	#insertar_movimientos_cta_corriente()
	insertar_estado_devolucion()
	print('#'*50)
	insertar_estado_cta_corriente()
	print('#'*50)
	insertar_tipo_movimiento_stock()
	print('#'*50)
	#insertar_pedido()
	print('#'*50)
	#insertar_historial_estado_pedido()
	print('#'*50)
	#insertar_detalle_pedido()
	print('#'*50)
	insertar_movimiento_stock()
	print('#'*50)
	#insertar_triggers()
	#insertar_comprobante_pago()
	print('#'*50)
	#insertar_devolucion()
	print('#'*50)
	#insertar_detalle_devolucion()
	#print('#'*50)
	insertar_estado_comprobante_pago()
	