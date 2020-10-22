import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ventana(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title='El juego de la vida')
		self.interfaz()
		

	def interfaz(self):
		grid = Gtk.Grid()
		self.add(grid)

win = ventana()
win.show_all()
Gtk.main()