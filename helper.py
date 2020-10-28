# Importamos la instancia de la DB
from distribuidora import db

# Importamos los modelos
from distribuidora.models.provincia import Provincia
from distribuidora.models.localidad import Localidad
from distribuidora.models.tipo_dni import TipoDNI
from distribuidora.models.gestion_usuario import Usuario, Rol, Permiso
from distribuidora.models.domicilio import Domicilio
from distribuidora.models.persona import Persona
from distribuidora.models.pedido import TipoEstadoPedido

# Importamos settings
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
			new_usuario = Usuario(username=row['username'], password=row['password'], \
				persona_id=persona.persona_id)
			new_usuario.usuario_rol.append(rol)
			lista_usuario.append(new_usuario)
	db.session.add_all(lista_usuario)
	db.session.commit()


def insertar_tipo_estado_pedido():
	print('Importando Modelo de Tipo de Estados de Pedidos')
	estados =	[]
	with open(DATOS_PATH + 'tipo_estado_pedido.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			print('Estado Pedido: {}'.format(row['descripcion']))
			print('-'*50)
			tipos_estado_pedido = TipoEstadoPedido(descripcion=row['descripcion'], \
				descripcion_corta=row['descripcion_corta'])

			estados.append(tipos_estado_pedido)
	db.session.add_all(estados)
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
	print('#'*50)
	insertar_tipo_estado_pedido()
	print('#'*50)
	insertar_tipo_dni()
