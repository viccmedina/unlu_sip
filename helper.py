# Importamos la instancia de la DB
from distribuidora import db

# Importamos los modelos
from distribuidora.models.provincia import Provincia
from distribuidora.models.localidad import Localidad
from distribuidora.models.tipo_dni import TipoDNI
from distribuidora.models.gestion_usuario import Usuario, Rol, Permiso
from distribuidora.models.domicilio import Domicilio
from distribuidora.models.persona import Persona

# Importamos settings
from distribuidora.settings import DB_PATH

# Libería de Python
from pathlib import Path

# Librería del OS
import os

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
"""

descripcion = "Buenos Aires"
new_provincia = Provincia(descripcion)
db.session.add(new_provincia)
db.session.commit()



#Agregamos la localidad de paso del rey de la PROVINCIA de Bs As
descripcion = "Paso del rey"

provincia = Provincia.query.filter_by(descripcion="Buenos Aires").first()
print('Se ha insertado: {}'.format(provincia.provincia_id))

new_localidad = Localidad(descripcion, provincia.provincia_id)
db.session.add(new_localidad)
db.session.commit()

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

descripcion = 'Administrador'
new_rol = Rol(descripcion, descripcion)
db.session.add(new_rol)
db.session.commit()

descripcion = 'Gerencial'
new_rol = Rol(descripcion, descripcion)
db.session.add(new_rol)
db.session.commit()