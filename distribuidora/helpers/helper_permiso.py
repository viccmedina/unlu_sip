from distribuidora import db
from distribuidora.models.gestion_usuario import Permiso

"""
En este archivo agregaremos los permisos a la bd
"""

# creamo el permiso "stock all"
descripcion = "stock.*"
new_permiso = Permiso(descripcion)
db.session.add(new_permiso)
db.session.commit()

# creamo el permiso "stock alta"
descripcion = "stock.alta"
new_permiso = Permiso(descripcion)
db.session.add(new_permiso)
db.session.commit()

# creamo el permiso "stock modificacion"
descripcion = "stock.modificacion"
new_permiso = Permiso(descripcion)
db.session.add(new_permiso)
db.session.commit()


