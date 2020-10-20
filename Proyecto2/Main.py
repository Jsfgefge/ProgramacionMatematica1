import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import matplotlib.pyplot as plt #Para el grid
from matplotlib import colors #Para los colores de las celulas
import matplotlib.animation as animation
import numpy as np #Tengo entendido que para el uso de matrices

ON = 255
OFF = 0
pause = False
def update(frame, img, grid, N):
	newGrid = grid.copy()
	for i in range(N):
		for j in range(N):
			total = int((grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
						 grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
						 grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
						 grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255)


			#Reglas del juego
			if grid[i, j] == OFF and total == 3:
				newGrid[i, j] = ON
			elif grid[i,j] == ON and (total < 2 or total > 3):
				newGrid[i, j] = OFF

		# update data
	img.set_data(newGrid)
	grid[:] = newGrid[:]
	return img,

def main():
	N = 10
	updateInterval = 10
	data = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[255, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 255, 255, 0, 0, 0, 0, 0, 0, 0],
			[255, 255, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
	grid = np.array(data)


	# Basicamente para colorear
	cmap = colors.ListedColormap(['blue', 'red'])  # Para seleccionar que color queremos
	bounds = [0, 1, 2]  # Para verificar que valores tienen que ser rojo y cuales azules (0=azul,1=rojo)
	norm = colors.BoundaryNorm(bounds, cmap.N)  # Para colorear el grid

	fig, ax = plt.subplots()
	img = ax.imshow(grid, cmap=cmap, norm=norm)
	ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,),
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

	plt.show()



main()