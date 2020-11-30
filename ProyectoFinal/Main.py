import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import time
import random
import math

from PIL import Image,ImageFont,ImageDraw, ImageOps, ImageChops

import numpy as np #Tengo entendido que para el uso de matrices
from numpy import save

import os
import webbrowser
from datetime import datetime


UI_INFO = """
<ui>
  <menubar name='menuBar'>
    <menu action='archivo'>
      <menuitem action='cargarImagen' />
      <menuitem action='guardarASCII' />
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='Twitter'>
      <menuitem action='SignIn' />
      <menuitem action='LogOut' />
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
		Gtk.Window.__init__(self, title='ASCII art')

		self.state = False
		self.img = Gtk.Image()
		self.imgRes = Gtk.Image()
		self.imgPIL = Image.Image
		st = '"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^.'
		#st = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\^'
		self.charsList = list(st)
		self.chars = self.charsList


		btnConvertir = Gtk.Button(label='Convertir')
		btnConvertir.connect('clicked', self.convertir)
		btnInvertir = Gtk.ToggleButton(label='Invertir')
		btnInvertir.connect('toggled', self.invertir,'1')
		self.btnGuardar = Gtk.Button(label='Guardar')
		self.btnGuardar.connect('clicked', self.guardar)
		self.btnGuardar.set_sensitive(False)
		btnSubir = Gtk.Button(label='Subir')
		btnSubir.connect('clicked', self.subir)
		btnGrises = Gtk.Button(label='Grises')
		btnGrises.connect('clicked', self.grises)

		btnPrueba = Gtk.Button(label='Prueba')
		btnPrueba.connect('clicked', self.prueba)

		#Tamaño de la ventana
		self.set_default_size(700,00)
		#Para el barmenu
		self.action = Gtk.ActionGroup(name='action')
		self.menuArchivo(self.action)
		self.menuConfig(self.action)
		self.menuAyuda(self.action)
		self.uimanager = self.create_ui_manager()
		self.uimanager.insert_action_group(self.action)
		menubar = self.uimanager.get_widget('/menuBar')
		#Para desabilidar el boton guardar en el inicio del programa
		l = self.action.list_actions()
		for i in l:
			if i.get_name() == 'guardarASCII':
				i.set_sensitive(False)

		self.buffer = Gtk.TextBuffer()
		display = Gtk.TextView(buffer=self.buffer)
		display.set_justification(Gtk.Justification.LEFT)
		display.set_size_request(350, 550)

		#Grid donde estara toda la interfaz
		container = Gtk.Grid()
		container.set_row_spacing(5)
		container.set_column_spacing(5)
		container.attach(menubar, 0, 0, 150, 1)
		container.attach(self.img, 0, 1, 73, 95)
		container.attach(self.imgRes, 77, 1, 73, 95)
		container.attach(btnConvertir, 74, 25, 3, 1)
		container.attach(btnInvertir, 74, 26, 3, 1)
		container.attach(self.btnGuardar, 74, 27, 3, 1)
		container.attach(btnSubir, 74, 28, 3, 1)
		container.attach(btnGrises, 74, 29, 3, 1)
		#container.attach(btnPrueba, 74, 30, 3, 1)
		self.add(container)

		self.set_default_size(-1,500)
		self.set_resizable(False)




	def imprimirCaptura(self, event):
		'''
		Para tomar una foto del estado actual del ScrolledWindow
		:param event:
		:return:
		'''
		now = datetime.now()
		titulo = str(now.day) + '-' + str(now.month) + '-' + str(now.day) + '  ' + str(now.hour) + ':' + str(now.minute)
		self.figure.savefig(os.getcwd()+'/capturas/'+titulo+'.png')

	def create_ui_manager(self):
		'''
		Para el uso del barmenu
		:return:
		'''
		uimanager = Gtk.UIManager()
		uimanager.add_ui_from_string(UI_INFO)
		accelgroup = uimanager.get_accel_group()
		self.add_accel_group(accelgroup)
		return uimanager


	def resize(self,img, new_width=100):
		im = self.imgPIL
		w,h = im.size
		new_height = math.ceil(new_width * h / w)
		return im.resize((new_width, new_height))

	def imGris(self,img):
		return  img.convert('L')

	def ASCII(self, img,chars):
		rango = math.ceil(255/len(chars))
		im = list(img.getdata())
		pixels_ascii=[]
		for pixel in im:
			temp = math.floor(pixel / rango)
			pixels_ascii.append(chars[temp])
		return ''.join(pixels_ascii)


	def convertir(self,widget):
		w1,h1=self.imgPIL.size
		img = self.resize(self.imgPIL.convert('L'),new_width=w1)
		img = self.imGris(img)

		if self.state == True:
			self.chars = self.charsList[::-1]
		else:
			self.chars = self.charsList


		w,h = img.size
		caract = self.ASCII(img,self.chars)
		font = ImageFont.load_default()
		outImage = Image.new('RGB',(10*w,12*h),color=(255,255,255))
		drawImage = ImageDraw.Draw(outImage)

		for i in range(h):
			for j in range(w):
				drawImage.text((10*j,12*i),caract[j+i*w],font=font, fill=(0, 0, 0))

		nombregenerico = 'hola.jpg'
		outImage.save(nombregenerico)

		ruta=os.getcwd()
		ruta+='/'+nombregenerico

		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=ruta,
			width=350,
			height=550,
			preserve_aspect_ratio=True)
		self.imgRes.set_from_pixbuf(pixbuf)
		#os.remove(ruta)

		l = self.action.list_actions()
		for i in l:
			if i.get_name() == 'guardarASCII':
				i.set_sensitive(True)
		self.btnGuardar.set_sensitive(True)

	def grises(self, widget):
		pass

	def invertir(self,widget,name):
		if widget.get_active():
			self.state = True
		else:
			self.state = False


	def guardar(self,widget):
		'''
		Cosas
		:param widget:
		:return:
		'''
		img = self.resize(self.imgPIL.convert('L'))
		img = self.imGris(img)

		if self.state == True:
			self.chars = self.charsList[::-1]
		else:
			self.chars = self.charsList

		w, h = img.size
		caract = self.ASCII(img, self.chars)

		l = len(caract)

		imageAscii = [caract[i: i + w] for i in
					  range(0, l, w)]


		cadenaASCII = ''
		for i in range(len(imageAscii)):
			cadenaASCII += imageAscii[i] + '\n'

		fo = open('result.txt', 'w')
		fo.write(cadenaASCII)
		fo.close()

	def subir(self,widget):
		pass

	def prueba(self,widget):
		pass

	def grises(self,widget):
		def clicked(button):
			self.charsList = list(textBox.get_text())
			self.chars = self.charsList
			b.close()
			return self.chars
		b = Gtk.Window()
		textBox = Gtk.Entry()
		btnOk = Gtk.Button(label='Ok')
		btnOk.connect('clicked', clicked)
		label = Gtk.Label(label="Ingrese la escala de grises deseada")

		container = Gtk.Grid()
		container.set_row_spacing(5)
		container.set_column_spacing(5)
		container.attach(label, 0, 0, 1, 1)
		container.attach(textBox, 0, 1, 1, 1)
		container.attach(btnOk, 1, 0, 2, 2)
		b.add(container)
		b.set_default_size(-1, -1)
		b.set_resizable(False)
		b.show_all()


	def menuArchivo(self, action_group):
		'''
		Pestaña 'Archivo'
		:param action_group:
		:return:
		'''
		action_group.add_actions(
			[
				("archivo", None, "Archivo"),
				("cargarImagen", None, 'Cargar', '<control>N', None, self.cargaImagen),
				("guardarASCII", None, 'Guardar ASCII', "<control>G", None, self.guardar),
			]
		)

		action_filequit = Gtk.Action(name="FileQuit", stock_id=Gtk.STOCK_QUIT)
		action_filequit.connect("activate", self.cerrarVentana)
		action_group.add_action(action_filequit)

	def menuConfig(self, action_group):
		'''
		Pestaña 'Configuracion'
		:param action_group:
		:return:
		'''
		action_group.add_action(Gtk.Action(name="Twitter", label="Twitter"))

		action_group.add_radio_actions(
			[
				("SignIn", None, "SignIn", None, None, 1),
				("LogOut", None, "LogOut", None, None, 2),
			],
			1,
			#self.superficie,
		)

	def menuAyuda(self, action_group):
		'''
		Pestaña 'Ayuda'
		:param action_group:
		:return:
		'''
		action_group.add_actions(
			[
				("help", None, "Ayuda"),
				("about", None, 'Acerca de', None, None, self.acercaDe),
				("code", None, 'Codigo', None, None, self.codigoVida),
			]
		)




	def cargaImagen(self, widget):
		'''
		Selecciona un archivo para cargar en el ScrolledWindow
		:param widget:
		:return:
		'''
		dialog = Gtk.FileChooserDialog(
			title='Seleccione una imagen', parent=self, action=Gtk.FileChooserAction.OPEN,
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
			self.imgPIL = Image.open(self.ruta)
			pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
				filename=self.ruta,
				width=350,
				height=550,
				preserve_aspect_ratio=True)
			self.img.set_from_pixbuf(pixbuf)
		elif response == Gtk.ResponseType.CANCEL:
			pass

		l = self.action.list_actions()
		for i in l:
			if i.get_name() == 'guardarASCII':
				i.set_sensitive(False)
		self.btnGuardar.set_sensitive(False)
		self.imgRes.clear()
		dialog.destroy()



	def cerrarVentana(self, widget):
		#Cierra ventana
		Gtk.main_quit()

	def acercaDe(self, widget):
		#Abre una ventana
		acercaDe = Gtk.AboutDialog()
		acercaDe.set_program_name('El juego de la vida')
		acercaDe.set_authors(['Jsfgefge/AngelMarroquin'])
		acercaDe.set_comments('Herramientas usadas:\n'
			'-Python v3.8.5\n'
			'-Gtk v3.0\n'
			'-Matplotlib v3.3.2\n'
			'-Numpy v1.19.2\n')
		acercaDe.set_title('uwu')
		acercaDe.run()
		acercaDe.destroy()

	def codigoVida(self, widget):
		webbrowser.open_new_tab("https://github.com/Jsfgefge/ProgramacionMatematica1/blob/master/Proyecto2/Main.py")









win = ventana()
win.connect("destroy", Gtk.main_quit)
win.show_all()

Gtk.main()