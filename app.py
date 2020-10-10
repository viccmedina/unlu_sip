from distribuidora import app, db
from distribuidora.models.provincia import Provincia
from distribuidora.models.localidad import Localidad
from distribuidora.models.gestion_usuario import Rol, Permiso, Usuario
from distribuidora.models.tipo_dni import TipoDNI
from distribuidora.models.persona import Persona
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app)
admin.add_view(ModelView(Provincia, db.session))
admin.add_view(ModelView(Localidad, db.session))
admin.add_view(ModelView(Usuario, db.session))
admin.add_view(ModelView(Rol, db.session))
admin.add_view(ModelView(Permiso, db.session))
admin.add_view(ModelView(Persona, db.session))


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
