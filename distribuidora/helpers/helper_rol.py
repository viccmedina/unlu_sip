from distribuidora import db
from distribuidora.models.gestion_usuario import Rol
"""
En este archivito cargaremos los distrintos roles que cuenta la empresa
"""

#este es el rol de adminastracion
descripcion = "adminastracion"
new_rol = Rol(descripcion)
db.session.add(new_rol)
db.session.commit()

#este es el rol de operador
descripcion = "operador"
new_rol = Rol(descripcion)
db.session.add(new_rol)
db.session.commit()

#este es el rol de distribucion
descripcion = "distribucion"
new_rol = Rol(descripcion)
db.session.add(new_rol)
db.session.commit()

# este es el rol del cliente
descripcion = "cliente"
new_rol = Rol(descripcion)
db.session.add(new_rol)
db.session.commit()