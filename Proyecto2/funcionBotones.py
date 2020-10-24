import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import matplotlib.pyplot as plt #Para el grid
from matplotlib import colors #Para los colores de las celulas
import matplotlib.animation as animation
import numpy as np #Tengo entendido que para el uso de matrices

ON = 1
OFF = 0
pause = False
def reglas(frame, img, tabla, N):
	nTabla = tabla.copy()
	for i in range(N):
		for j in range(N):
			total = int((tabla[i, (j - 1) % N] + tabla[i, (j + 1) % N] +
						 tabla[(i - 1) % N, j] + tabla[(i + 1) % N, j] +
						 tabla[(i - 1) % N, (j - 1) % N] + tabla[(i - 1) % N, (j + 1) % N] +
						 tabla[(i + 1) % N, (j - 1) % N] + tabla[(i + 1) % N, (j + 1) % N]))


			#Reglas del juego
			if tabla[i, j] == 0 and total == 3:
				nTabla[i, j] = 1
			elif tabla[i,j] == 1 and (total < 2 or total > 3):
				nTabla[i, j] = 0

		# update data
	img.set_data(nTabla)
	tabla[:] = nTabla[:]
	return img,

def main():
	N = 10
	updateInterval = 10
	data = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
			[1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
			[0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
	grid = np.array(data)
	# Basicamente para colorear
	cmap = colors.ListedColormap(['blue','red'])  # Para seleccionar que color queremos
	bounds = [0, 1, 2]  # Para verificar que valores tienen que ser rojo y cuales azules (0=azul,1=rojo)
	norm = colors.BoundaryNorm(bounds, cmap.N)  # Para colorear el grid
	#Generacion del Grid y su animacion
	fig, ax = plt.subplots()
	img = ax.imshow(grid, cmap=cmap, norm=norm)
	ani = animation.FuncAnimation(fig, reglas, fargs=(img, grid, N,),
								  frames=20,
								  interval=updateInterval,
								  save_count=50,
								  repeat=True)

	anim_running = True
	def onClick(event):
		nonlocal anim_running
		if anim_running:
			ani.event_source.stop()
			anim_running = False
		else:
			ani.event_source.start()
			anim_running = True

	fig.canvas.mpl_connect('button_press_event', onClick)

	ax.set_xticks(np.arange(0.48, 10, 1))
	ax.set_yticks(np.arange(0.48, 10, 1))

	ax.set_yticklabels([])
	ax.set_xticklabels([])
	plt.grid()
	plt.tight_layout()
	plt.show()



main()