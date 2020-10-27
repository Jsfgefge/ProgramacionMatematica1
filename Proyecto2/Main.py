import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import matplotlib.pyplot as plt #Para el grid
import matplotlib as mlp
from matplotlib import colors #Para los colores de las celulas
import matplotlib.animation as animation
import numpy as np #Tengo entendido que para el uso de matrices

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure

UI_INFO = """
<ui>
  <menubar name='menuBar'>
    <menu action='archivo'>
      <menuitem action='cargarInicio' />
      <menuitem action='guardarSimulacion' />
      <menuitem action='random' />
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='config'>
      <menuitem action='fronteraNorm' />
      <menuitem action='fronteraToro' />
      <separator />
      <menuitem action='actualizarIntervalo' />
    </menu>
    <menu action='help'>
      <menuitem action='about'/>
      <menuitem action='code'/>
    </menu>
  </menubar>
</ui>
"""

class ventana(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title='El juego de la vida')

		self.fronteras = 'Normal'
		self.intervaloActu = 100
		self.dimensionMatriz = 10
		self.conteo = 1

		self.ruta = ''

		self.set_default_size(700,00)

		action = Gtk.ActionGroup(name='action')

		self.menuArchivo(action)
		self.menuConfig(action)
		self.menuAyuda(action)

		uimanager = self.create_ui_manager()
		uimanager.insert_action_group(action)

		menubar = uimanager.get_widget('/menuBar')

		grid = Gtk.Grid()
		grid.set_row_spacing(5)
		grid.set_column_spacing(5)
		grid.attach(menubar, 0, 0, 10, 1)
		self.add(grid)

		sw = Gtk.ScrolledWindow()
		grid.attach(sw, 0, 1, 60, 90)
		sw.set_border_width(1)
		canvas1 = self.animacion()
		#canvas1.set_size_request(100, 100)

		sw.add(canvas1)


	def create_ui_manager(self):
		uimanager = Gtk.UIManager()

		# Throws exception if something went wrong
		uimanager.add_ui_from_string(UI_INFO)

		# Add the accelerator group to the toplevel window
		accelgroup = uimanager.get_accel_group()
		self.add_accel_group(accelgroup)
		return uimanager

	def menuArchivo(self, action_group):
		action_group.add_actions(
			[
				("archivo", None, "Archivo"),
				("cargarInicio", None, 'Cargar', '<control>N', None, self.cargaEstado),
				("guardarSimulacion", None, 'Guardar Estado', "<control>G", None, self.guardarEstado),
				("random",None, 'Configuracoin Random', "<control>R", None, self.random),
			]
		)
		action_filequit = Gtk.Action(name="FileQuit", stock_id=Gtk.STOCK_QUIT)
		action_filequit.connect("activate", self.cerrarVentana)
		action_group.add_action(action_filequit)

	def menuConfig(self, action_group):
		action_group.add_action(Gtk.Action(name="config", label="Configuracion"))

		action_group.add_radio_actions(
			[
				("fronteraNorm", None, "Normal", None, None, 1),
				("fronteraToro", None, "Toroidal", None, None, 2),
			],
			1,
			self.superficie,
		)
		intervalo = Gtk.Action(name='actualizarIntervalo', label='Intervalo')
		intervalo.connect('activate', self.intervalo)
		action_group.add_action(intervalo)

	def menuAyuda(self, action_group):
		action_group.add_actions(
			[
				("help", None, "Ayuda"),
				("about", None, 'Acerca de', None, None, self.acercaDe),
				("code", None, 'Codigo', None, None, self.codigoVida),
			]
		)

	def superficie(self, widget, current):
		if self.fronteras == 'Toro':
			self.fronteras = 'Normal'
		else:
			self.fronteras = 'Toro'

	def intervalo(self):
		pass

	def cargaEstado(self, widget):
		dialog = Gtk.FileChooserDialog(
			title='Seleccione un estado a cargar', parent=self, action=Gtk.FileChooserAction.OPEN,
		)
		dialog.add_buttons(
			Gtk.STOCK_CANCEL,
			Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN,
			Gtk.ResponseType.OK
		)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.ruta = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			pass

		dialog.destroy()

	def guardarEstado(self, widget):
		print('coso guardar')

	def random(self, widget):
		print('random')

	def cerrarVentana(self, widget):
		Gtk.main_quit()

	def acercaDe(self, widget):
		pass

	def codigoVida(self, widget):
		pass

	def randomGrid(self,N):

		"""returns a grid of NxN random values"""
		return np.random.choice([1,0], N * N, p=[0.2, 0.8]).reshape(N, N)

	def animacion(self):
		figure = mlp.figure.Figure()
		canvas = FigureCanvas(figure)
		N = self.dimensionMatriz
		updateInterval = 100
		data = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
				[1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
		#grid = self.randomGrid(N)
		grid = np.array(data)

		'''
		Anotacion mental:
		Inicializar el grid con una matriz NxN filleada con ceros y mediante eventos indicar que se llene de forma 
		random o que se llene con la matriz indicada en la ruta uwu
		
		***Pendientes:
			-Toda la pestaña 'Archivo' y todo lo que implica menos random
			-Configuracion =>Intervalo
			-Toda la pestaña 'Ayuda'		
		'''

		if self.ruta == '':
			grid = self.randomGrid(N)
		else:
			grid = np.zeros((N, N), dtype=int)

		def sumaToro(tabla, N):
			nTabla = tabla.copy()
			for i in range(N):
				for j in range(N):
					total = int((tabla[i, (j - 1) % N] + tabla[i, (j + 1) % N] +
								 tabla[(i - 1) % N, j] + tabla[(i + 1) % N, j] +
								 tabla[(i - 1) % N, (j - 1) % N] + tabla[(i - 1) % N, (j + 1) % N] +
								 tabla[(i + 1) % N, (j - 1) % N] + tabla[(i + 1) % N, (j + 1) % N]))

					# Reglas del juego
					if tabla[i, j] == 0 and total == 3:
						nTabla[i, j] = 1
					elif tabla[i, j] == 1 and (total < 2 or total > 3):
						nTabla[i, j] = 0

			return nTabla

		def sumaNormal(tabla, N):
			nTabla = tabla.copy()
			for i in range(0, N):
				for j in range(0, N):
					total = 0
					# **Verificacion de cada celda adyacente por su estado.
					# **En el caso que sea j==N, entonces j+1=N+1 por lo tanto da error, en ese caso se usa un try except para
					# considerar ese caso.
					# **En el caso que sea j==0, entonces j-1=0-1 por lo tanto me considera una celda que no es adyacente, en ese
					# caso devuelte una celula muerta.
					try:
						if j - 1 > -1 and int(tabla[i, (j - 1)]) == 1:
							total += 1
						else:
							total += 0
					except:
						total += 0
					try:
						if int(tabla[i, (j + 1)]) == 1: total += 1
					except:
						total += 0
					try:
						if i - 1 > -1 and int(tabla[(i - 1), j]) == 1:
							total += 1
						else:
							total += 0
					except:
						total += 0
					try:
						if int(tabla[(i + 1), j]) == 1: total += 1
					except:
						total += 0
					try:
						if i - 1 > -1 and j - 1 > -1 and int(tabla[(i - 1), (j - 1)]) == 1:
							total += 1
						else:
							total += 0
					except:
						total += 0
					try:
						if i - 1 > -1 and int(tabla[(i - 1), (j + 1)]) == 1:
							total += 1
						else:
							total += 0
					except:
						total += 0
					try:
						if j - 1 > -1 and int(tabla[(i + 1), (j - 1)]) == 1:
							total += 1
						else:
							total += 0
					except:
						total += 0
					try:
						if int(tabla[(i + 1), (j + 1)]) == 1: total += 1
					except:
						total += 0

					# Reglas del juego
					if tabla[i, j] == 0 and total == 3:
						nTabla[i, j] = 1
					elif tabla[i, j] == 1 and (total < 2 or total > 3):
						nTabla[i, j] = 0

			return nTabla

		def reglas(frame, img, tabla, N):
			if self.fronteras == 'Normal':
				nTabla = sumaNormal(tabla, N)
			if self.fronteras == 'Toro':
				nTabla = sumaToro(tabla, N)

			# update data
			img.set_data(nTabla)
			tabla[:] = nTabla[:]
			return img,

		# Basicamente para colorear
		cmap = colors.ListedColormap(['blue', 'red'])  # Para seleccionar que color queremos
		bounds = [0, 1, 2]  # Para verificar que valores tienen que ser rojo y cuales azules (0=azul,1=rojo)
		norm = colors.BoundaryNorm(bounds, cmap.N)  # Para colorear el grid
		# Generacion del Grid y su animacion
		ax = figure.subplots()
		img = ax.imshow(grid, cmap=cmap, norm=norm)


		self.ani = animation.FuncAnimation(figure, reglas, fargs=(img, grid, N,),
										   frames=10,
										   interval=updateInterval,
										   save_count=1,
										   repeat=True)

		anim_running = False

		def onClick(event):
			nonlocal anim_running
			if anim_running:
				self.ani.event_source.stop()
				anim_running = False
			else:
				self.ani.event_source.start()
				anim_running = True

		def onStart(event):
			if anim_running==False:
				self.ani.event_source.stop()
			else:
				pass

		def iniConteo(event):
			if anim_running:
				self.conteo+=1
				print(self.conteo)

		figure.canvas.mpl_connect('button_press_event', onClick)
		figure.canvas.mpl_connect('draw_event', onStart)
		figure.canvas.mpl_connect('draw_event', iniConteo)

		return canvas

class  FileChooserWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title='Seleccion de estado')

		box = Gtk.Box(spacing=6)
		self.add(box)

		button1=Gtk.Button(label='Seleccione estado')
		button1.connect('clicked', self.on_file_clicked)
		box.add(button1)

		button2 = Gtk.Button(label='Seleccione folder')
		button2.connect('clicked', self.on_folder_clicked)
		box.add(button2)

	def on_file_clicked(self, widget):
		dialog = Gtk.FileChooserDialog(
			title='Seleccione un estado a cargar', parent=self, action=Gtk.FileChooserAction.OPEN
		)
		dialog.add_buttons(
			Gtk.STOCK_CANCEL,
			Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN,
			Gtk.ResponseType.OK
		)

		self.add_filters(dialog)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print('Open clicked')
			print('File selected: ', dialog.get_filename())
		elif response == Gtk.ResponseType.CANCEL:
			print('Cancel clicked')

		dialog.destroy()

	def add_filters(self, dialog):
		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)

	def on_folder_clicked(self, widget):
		dialog = Gtk.FileChooserDialog(
			title="Please choose a folder",
			parent=self,
			action=Gtk.FileChooserAction.SELECT_FOLDER,
		)
		dialog.add_buttons(
			Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
		)
		dialog.set_default_size(800, 400)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("Select clicked")
			print("Folder selected: " + dialog.get_filename())
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")

		dialog.destroy()


win = ventana()
win.connect("destroy", Gtk.main_quit)
win.show_all()

Gtk.main()