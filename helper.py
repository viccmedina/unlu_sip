# Importamos la instancia de la DB
from distribuidora import db

# Importamos los modelos
from distribuidora.models.estado_producto import Estado_producto
from distribuidora.models.lista_precio import Lista_precio
from distribuidora.models.precio import Precio
from distribuidora.models.producto import Producto
from distribuidora.models.provincia import Provincia
from distribuidora.models.localidad import Localidad
from distribuidora.models.tipo_dni import TipoDNI
from distribuidora.models.gestion_usuario import Usuario, Rol, Permiso
from distribuidora.models.domicilio import Domicilio
from distribuidora.models.persona import Persona

# Importamos settings
from distribuidora.models.tipo_producto import Tipo_producto
from distribuidora.settings import DB_PATH, DATOS_PATH

# Libería de Python
from pathlib import Path

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

"""
Aca debemos poner todas las inserciones a la base. Es recomendable tenerlas todas juntas
para poder ejecutar un único archivo que realiza una funcionalidad externar a la app.
Es una tarea de desarrollo y testing.

# creamo el tipo "numero dni"
descripcion = "DNI"
new_tipo_dni = TipoDNI(descripcion)
db.session.add(new_tipo_dni)
db.session.commit()


#creamo el tipo libreta civica
descripcion = "Libreta Cívica"
new_tipo_dni = TipoDNI(descripcion)
db.session.add(new_tipo_dni)
db.session.commit()


descripcion = "Libreta de Enrolamiento"
new_tipo_dni = TipoDNI(descripcion)
db.session.add(new_tipo_dni)
db.session.commit()

# Agregamos los tipos de Roles

descripcion = 'Cliente'
new_rol = Rol(descripcion, descripcion)
db.session.add(new_rol)
db.session.commit()

descripcion = 'Operador'
new_rol = Rol(descripcion, descripcion)
db.session.add(new_rol)
db.session.commit()

descripcion = 'Gerencial'
new_rol = Rol(descripcion, descripcion)
db.session.add(new_rol)
db.session.commit()
"""
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


def insertar_lista_precios():
	print('Importando Modelo Lista de Precios')
	lista_list_precios = []
	# Abrimos el archivo csv de Lista de precios
	with open(DATOS_PATH + 'lista_precio.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		# Por cada una de las filas que existene en el archivos,
		# vamos a crear un registro en la base
		for row in csv_reader:
			# Dado que row es un diccionario, podemos acceder a sus campos
			# como cualquier diccionario en Python
			print('Lista de Precios: {}'.format(row['descripcion']))
			print('-'*50)
			# Creamos el objeto Lista de precios y lo guardamos
			new_lista_precios = Lista_precio(descripcion=row['descripcion'],fecha=row['fecha'])
			lista_list_precios.append(new_lista_precios)
		db.session.add_all(lista_list_precios)
		db.session.commit()

def insertar_estado_productos():
	print('Importando Modelo estado de productos')
	lista_estado_prod = []
	# Abrimos el archivo csv de Estado de productos
	with open(DATOS_PATH + 'estado_producto.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		# Por cada una de las filas que existene en el archivos,
		# vamos a crear un registro en la base
		for row in csv_reader:
			# Dado que row es un diccionario, podemos acceder a sus campos
			# como cualquier diccionario en Python
			print('Estado de producto: {}'.format(row['descripcion']))
			print('-'*50)
			# Creamos el objeto estado de producto y lo guardamos
			new_estado_prodcuto = Estado_producto(descripcion=row['descripcion'])
			lista_estado_prod.append(new_estado_prodcuto)
		db.session.add_all(lista_estado_prod)
		db.session.commit()



def insertar_tipo_producto():
	print('Importando Modelo tipo de producto')
	lista_tipo_prod = []
	# Abrimos el archivo csv de Tipo de producto
	with open(DATOS_PATH + 'tipo_producto.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		# Por cada una de las filas que existene en el archivos,
		# vamos a crear un registro en la base
		for row in csv_reader:
			# Dado que row es un diccionario, podemos acceder a sus campos
			# como cualquier diccionario en Python
			print('Tipo de producto: {}'.format(row['descripcion']))
			print('-'*50)
			# Creamos el objeto estado de producto y lo guardamos
			new_tipo_prodcuto = Tipo_producto(descripcion=row['descripcion'])
			lista_tipo_prod.append(new_tipo_prodcuto)
		db.session.add_all(lista_tipo_prod)
		db.session.commit()



def insertar_precios():
	print('Importando Modelo Precios')
	lista_precio = []
	# Abrimos el archivo csv de Precios
	with open(DATOS_PATH + 'precio.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('Precio: {}'.format(row['valor']))
			print('-'*50)
			new_precio = Precio(descripcion=row['descripcion'], valor=row['valor'],
								lista_precio_id=row['lista_precio_id'])
			lista_precio.append(new_precio)
		db.session.add_all(lista_precio)
		db.session.commit()


def insertar_loclidades():
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
	with open(DATOS_PATH + 'usuario.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('Usuario: {}'.format(row['username']))
			print('-'*50)
			rol = Rol.query.filter_by(nombre=row['rol']).first()
			persona = Persona.query.filter_by(email=row['persona']).first()
			print(rol)
			print(persona.persona_id)
			new_usuario = Usuario(username=row['username'], password=row['password'], persona_id=persona.persona_id)
			new_usuario.usuario_rol.append(rol)
			lista_usuario.append(new_usuario)
	db.session.add_all(lista_usuario)
	db.session.commit()

def insertar_productos():
	print('Importando Modelo de productos')
	lista_producto = []
	with open(DATOS_PATH + 'producto.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('Producto: {}'.format(row['descripcion']))
			print('-' * 50)
			estado_producto = Estado_producto.query.filter_by(descripcion=row['estado_producto']).first()
			tipo_producto = Tipo_producto.query.filter_by(descripcion=row['tipo_producto']).first()
			print('tipo prod: {}'.format(row['tipo_producto']))
			print('tipo prod: {}'.format(tipo_producto.tipo_producto_id))

			new_producto = Producto(descripcion=row['descripcion'],
									precio_id=row['precio_id'],
									estado_producto_id=estado_producto.estado_producto_id,
									tipo_producto_id=tipo_producto.tipo_producto_id)
			lista_producto.append(new_producto)
	db.session.add_all(lista_producto)
	db.session.commit()

if __name__ == '__main__':
	insertar_provincias()
	print('#'*50)
	insertar_loclidades()
	print('#'*50)
	insertar_roles()
	print('#'*50)
	insertar_permisos()
	print('#'*50)
	insertar_personas()
	print('#'*50)
	insertar_usuarios()
	print('#' * 50)
	insertar_lista_precios()
	print('#' * 50)
	insertar_precios()
	print('#' * 50)
	insertar_estado_productos()
	print('#' * 50)
	insertar_tipo_producto()
	print('#' * 50)
	insertar_productos()