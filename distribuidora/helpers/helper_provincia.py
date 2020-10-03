from distribuidora import db
from distribuidora.models.provincia import Provincia

"""
En este archivito crearemos algunas provincias en la db
"""

descripcion = "Buenos Aires"
new_provincia = Provincia(descripcion)
db.session.add(new_provincia)
db.session.commit()

descripcion = "Santa Fe"
new_provincia = Provincia(descripcion)
db.session.add(new_provincia)
db.session.commit()

descripcion = "Entre Rios"
new_provincia = Provincia(descripcion)
db.session.add(new_provincia)
db.session.commit()

descripcion = "La pampa"
new_provincia = Provincia(descripcion)
db.session.add(new_provincia)
db.session.commit()

descripcion = "Cordoba"
new_provincia = Provincia(descripcion)
db.session.add(new_provincia)
db.session.commit()