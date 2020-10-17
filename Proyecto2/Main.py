import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


import matplotlib.pyplot as plt #Para el grid
from matplotlib import colors #Para los colores de las celulas
import numpy as np #Tengo entendido que para el uso de matrices


#Matriz que me dice que celulas estan vivas y cuales muertas
data = [[0, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 1, 1, 0, 1, 0, 1],
        [1, 1, 0, 0, 1, 0, 1, 1, 0, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 0, 1]]

#Basicamente para colorear
cmap = colors.ListedColormap(['blue', 'red']) #Para seleccionar que color queremos
bounds = [0,1,2] #Para verificar que valores tienen que ser rojo y cuales azules (0=azul,1=rojo)
norm = colors.BoundaryNorm(bounds, cmap.N) #Para colorear el grid

fig, ax = plt.subplots()
ax.imshow(data, cmap=cmap, norm=norm)

# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
ax.set_xticks(np.arange(-.5, 10, 1));
ax.set_yticks(np.arange(-.5, 10, 1));

# Turn off tick labels
ax.set_yticklabels([])
ax.set_xticklabels([])

plt.show()






