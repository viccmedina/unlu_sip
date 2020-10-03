from distribuidora import db
from distribuidora.models.localidad import Localidad
from distribuidora.models.provincia import Provincia

"""
Crearemos este archivo con el fin de cargar algunas localidades en la db
"""
#Agregamos la localidad de paso del rey de la PROVINCIA de Bs As
descripcion = "Paso del rey"
provincia = Provincia.query.filter_by(descripcion="Buenos Aires").first()
new_localidad = Localidad(descripcion, provincia)
db.session.add(new_localidad)
db.session.commit()

#Agregamos la localidad de Moreno de la PROVINCIA de Bs As
descripcion = "Moreno"
provincia = Provincia.query.filter_by(descripcion="Buenos Aires").first()
new_localidad = Localidad(descripcion, provincia)
db.session.add(new_localidad)
db.session.commit()

#Agregamos la localidad de Merlo de la PROVINCIA de Bs As
descripcion = "Merlo"
provincia = Provincia.query.filter_by(descripcion="Buenos Aires").first()
new_localidad = Localidad(descripcion, provincia)
db.session.add(new_localidad)
db.session.commit()

#Agregamos la localidad La reja de la PROVINCIA de Bs As
descripcion = "La reja"
provincia = Provincia.query.filter_by(descripcion="Buenos Aires").first()
new_localidad = Localidad(descripcion, provincia)
db.session.add(new_localidad)
db.session.commit()

#Agregamos la localidad de Moron de la PROVINCIA de Bs As
descripcion = "Ituzaingo"
provincia = Provincia.query.filter_by(descripcion="Buenos Aires").first()
new_localidad = Localidad(descripcion, provincia)
db.session.add(new_localidad)
db.session.commit()

#Agregamos la localidad de Moron de la PROVINCIA de Bs As
descripcion = "Moron"
provincia = Provincia.query.filter_by(descripcion="Buenos Aires").first()
new_localidad = Localidad(descripcion, provincia)
db.session.add(new_localidad)
db.session.commit()

#Agregamos la localidad de General Rodriguez de la PROVINCIA de Bs As
descripcion = "General Rodriguez"
provincia = Provincia.query.filter_by(descripcion="Buenos Aires").first()
new_localidad = Localidad(descripcion, provincia)
db.session.add(new_localidad)
db.session.commit()

#Agregamos la localidad de Lujan de la PROVINCIA de Bs As
descripcion = "Lujan"
provincia = Provincia.query.filter_by(descripcion="Buenos Aires").first()
new_localidad = Localidad(descripcion, provincia)
db.session.add(new_localidad)
db.session.commit()

#Agregamos la localidad de Mercedes de la PROVINCIA de Bs As/ hay que hacerlo famoso
descripcion = "Mercedes"
provincia = Provincia.query.filter_by(descripcion="Buenos Aires").first()
new_localidad = Localidad(descripcion, provincia)
db.session.add(new_localidad)
db.session.commit()

#Agregamos la localidad de Rosario de la PROVINCIA de Santa Fe
descripcion = "Rosario"
provincia = Provincia.query.filter_by(descripcion="Santa Fe").first()
new_localidad = Localidad(descripcion, provincia)
db.session.add(new_localidad)
db.session.commit()

#Agregamos la localidad de Gualeguaychu de la PROVINCIA de Entre Rios
descripcion = "Gualeguaychu"
provincia = Provincia.query.filter_by(descripcion="Entre Rios").first()
new_localidad = Localidad(descripcion, provincia)
db.session.add(new_localidad)
db.session.commit()