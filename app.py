from distribuidora import app, db
from distribuidora.models.provincia import Provincia
from distribuidora.models.localidad import Localidad
from distribuidora.models.gestion_usuario import Rol, Permiso, Usuario
from distribuidora.models.domicilio import Domicilio
from distribuidora.models.tipo_dni import TipoDNI
from distribuidora.models.persona import Persona
from distribuidora.models.cuenta_corriente import CuentaCorriente, MovimientoCtaCorriente
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from flask_admin.menu import MenuLink


class MyAdminIndexView(AdminIndexView):


	def is_accessible(self):
		print(current_user, flush=True)
		if current_user.is_authenticated:
			print('AUTENTICADO', flush=True)
			return current_user.has_role('Gerencia')
		else:
			print('NO AUTENTICADO', flush=True)

class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated


admin=Admin(app, index_view=MyAdminIndexView())
admin.add_link(LogoutMenuLink(name='Cerrar Sesión', category='', url="/logout"))
admin.add_view(ModelView(Provincia, db.session))
admin.add_view(ModelView(Localidad, db.session))
admin.add_view(ModelView(Usuario, db.session))
admin.add_view(ModelView(Rol, db.session))
admin.add_view(ModelView(Permiso, db.session))
admin.add_view(ModelView(Persona, db.session))
admin.add_view(ModelView(MovimientoCtaCorriente, db.session))


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
