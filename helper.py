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
	CuentaCorriente, MovimientoCtaCorriente
from distribuidora.models.producto import Marca, TipoProducto, Envase, UnidadMedida
from distribuidora.models.precio import Lista_precio
from distribuidora.models.pedido import PedidoEstado

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
			print('Provincia: {}'.format(row['descripcion']))
			print('-'*50)
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
			print('Localidad: {}'.format(row['descripcion']))
			print('-'*50)
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
			print('Rol: {}'.format(row['nombre']))
			print('-'*50)
			new_rol = Rol(nombre=row['nombre'], descripcion=row['descripcion'])
			lista_rol.append(new_rol)
		db.session.add_all(lista_rol)
		db.session.commit()


def insertar_permisos():
	print('Importando Modelo Permiso')
	lista_permiso =	[]
	with open(DATOS_PATH + 'permiso.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('Permiso: {}'.format(row['nombre']))
			print('-'*50)
			rol = Rol.query.filter_by(nombre=row['rol']).first()
			print(rol)
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
			print('Persona: {}'.format(row['nombre']))
			print('-'*50)

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
			print('Usuario: {}'.format(row['username']))
			print('-'*50)
			rol = Rol.query.filter_by(nombre=row['rol']).first()
			persona = Persona.query.filter_by(email=row['persona']).first()
			print(rol)
			print(persona.persona_id)
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
			print('Tipo Movimiento: {}'.format(row['descripcion']))
			print('-'*50)
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
			c = CuentaCorriente(persona_id=row['persona'])
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
			print('Movimiento: {}'.format(row['tipo_movimiento_cta_corriente']))
			print('-'*50)
			usuario = Usuario.query.get(row['usuario_registrador'])
			print('USUARIO: {}'.format(usuario))
			tm = TipoMovimientoCtaCorriente.query.filter_by(descripcion=row['tipo_movimiento_cta_corriente']).first()
			print('TIPO MOVIMIENTO {}'.format(tm.id))
			cta_corriente = CuentaCorriente.query.get(row['cta_corriente'])
			print('CTA CORRIENTE {}'.format(cta_corriente))
			if row['tipo_movimiento_cta_corriente'] == 'Deuda':
				saldo = float(row['saldo']) * (-1)
			else:
				saldo = float(row['saldo'])
			m = MovimientoCtaCorriente(descripcion=descripcion, usuario=usuario.id, tipo_movimiento_cta_corriente=tm.id, \
				cta_corriente=cta_corriente.cuenta_corriente_id, saldo=saldo)
			movimientos.append(m)
	db.session.add_all(movimientos)
	db.session.commit()


def insertar_pedido_estado():
	print('Importando Modelo de Tipo de Estados de Pedidos')
	estados = []
	with open(DATOS_PATH + 'tipo_estado_pedido.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('Estado Pedido: {}'.format(row['descripcion']))
			print('-'*50)
			tipos_estado_pedido = PedidoEstado(descripcion=row['descripcion'], \
				descripcion_corta=row['descripcion_corta'])

			estados.append(tipos_estado_pedido)
	db.session.add_all(estados)
	db.session.commit()


def insertar_marca():
	"""
	Cargamos las marcas con las cuales trabaja la distribuidora.
	"""
	print('Importando Modelo de Marcas')
	marcas = []
	with open(DATOS_PATH + 'marca.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('Marca: {}'.format(row['descripcion']))
			print('-'*50)
			m = Marca(descripcion=row['descripcion'])

			marcas.append(m)
	db.session.add_all(marcas)
	db.session.commit()


#Cargamos la db con tipo de producto
def insertar_tipo_producto():
	print('Importando Modelo tipoProducto')
	tipoProd = []
	with open(DATOS_PATH + 'tipo_producto.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('Tipo Producto: {}'.format(row['descripcion']))
			print('-'*50)
			new_tipo_producto = TipoProducto(descripcion=row['descripcion'])
			tipoProd.append(new_tipo_producto)
		db.session.add_all(tipoProd)
		db.session.commit()

def insertar_envase():
	print('Importando Modelo Envase')
	envase = []
	with open(DATOS_PATH + 'envase.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('Envase: {}'.format(row['descripcion']))
			print('-'*50)
			new_envase = Envase(descripcion=row['descripcion'])
			envase.append(new_envase)
		db.session.add_all(envase)
		db.session.commit()


def insertar_envase():
	print('Importando Modelo Unidad de medido')
	unidad_medida = []
	with open(DATOS_PATH + 'unidad_medida.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('Unidad de medida: {}'.format(row['descripcion']))
			print('-'*50)
			new_unidad_medida = UnidadMedida(descripcion=row['descripcion'])
			unidad_medida.append(new_unidad_medida)
		db.session.add_all(unidad_medida)
		db.session.commit()


def insertar_lista_precio():
	print('Importando Modelo Unidad de medido')
	lista_precio = []
	with open(DATOS_PATH + 'lista_precio.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('Lista de precio: {}'.format(row['fecha_desde'],row['fecha_hasta']))
			print('-'*50)
			print("acaaaaa el string " + row['fecha_desde'])
			#f_desde = datetime.to_time(row['fecha_desde'])g
			stringg = row['fecha_desde']
			f_desde = datetime.strptime(stringg, "%d/%m/%Y")
			print(f_desde)
			stringg = row['fecha_hasta']
			f_hasta = datetime.strptime(stringg, "%d/%m/%Y")
			print(f_hasta)
			#desde = datetime.datetime.strptime(fecha_desde=row['fecha_desde'], "%y/%m/%d").date
			#hasta = datetime.datetime.strptime(fecha_hasta=row['fecha_hasta'], "%y/%m/%d")
			new_lista_precio = Lista_precio(f_desde,f_hasta)
			lista_precio.append(new_lista_precio)
		db.session.add_all(lista_precio)
		db.session.commit()


if __name__ == '__main__':
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
	insertar_pedido_estado()
	print('#'*50)
	insertar_tipo_dni()
	print('#'*50)
	insertar_cuenta_corriente()
	print('#'*50)
	insertar_movimientos_cta_corriente()
	print('#'*50)
	insertar_marca()
	print('#'*50)
	insertar_tipo_producto()
	print('#'*50)
	insertar_envase()
	print('#'*50)
	insertar_envase()
	print('#'*50)
	insertar_lista_precio()
