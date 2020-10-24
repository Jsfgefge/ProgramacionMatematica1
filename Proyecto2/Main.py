import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

UI_info= """
<ui>
	<menubar name = 'menuBar'>
		<menu action='archivo'>
			<menu action='cargarIni' />
			<menu action='guardarSim' />
			<menu action='random' />
		</menu>	
		<menu action='config' >
			<menu action='frontNom' />
			<menu action='frontToro' />
			<menu action='actInterval' />
		</menu>
		<menu action='help' >
			<menu action='about' />
			<menu action='code' />
		</menu>
	</menubar>
</ui>
"""


class ventana(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title='El juego de la vida')
		self.set_default_size(1000,1000)
		action = Gtk.ActionGroup(name='action')
		self.menuArchivo(action)
		self.menuConfig(action)
		self.menuAyuda(action)


		uimanager = self.create_ui_manager()
		uimanager.insert_action_group(action)

		menubar = uimanager.get_widget('/menuBar')

		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		box.pack_start(menubar, False, False, 0)

		self.add(box)

	def create_ui_manager(self):
		uimanager = Gtk.UIManager()

		# Throws exception if something went wrong
		uimanager.add_ui_from_string(UI_info)

		# Add the accelerator group to the toplevel window
		accelgroup = uimanager.get_accel_group()
		self.add_accel_group(accelgroup)
		return uimanager

	def menuArchivo(self, action_group):
		menuArchivo = Gtk.Action(name='menuArchivo', label='Archivo')
		action_group.add_action(menuArchivo)

		nuevoEstado = Gtk.Action(name='Estado', stock_id=Gtk.STOCK_NEW)
		action_group.add_action(nuevoEstado)

win = ventana()
win.show_all()
Gtk.main()