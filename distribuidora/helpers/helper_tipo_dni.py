from distribuidora import db
from distribuidora.models.tipo_dni import TipoDNI

"""
Crearemos este archivo con el fin de cargar los distintos tipos de dni en la db

"""
# creamo el tipo "numero dni"
descripcion = "numero dni"
new_tipo_dni = TipoDNI(descripcion)
db.session.add(new_tipo_dni)
db.session.commit()

#creamo el tipo libreta civica
descripcion = "libreta civica"
new_tipo_dni = TipoDNI(descripcion)
db.session.add(new_tipo_dni)
db.session.commit()


descripcion = "libreta de enrolamiento"
new_tipo_dni = TipoDNI(descripcion)
db.session.add(new_tipo_dni)
db.session.commit()