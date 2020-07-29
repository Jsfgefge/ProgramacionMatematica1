from swampy.TurtleWorld import *
from math import pi

World=TurtleWorld()
Tor=Turtle()
Tor.delay = 0.0001
print(Tor)
def dibujar_circulo(tortuga,r):
    cir=2*pi*r
    lado=cir/1024
    for x in range(1024):
        fd(tortuga,lado)
        lt(tortuga,360/1024)

dibujar_circulo(Tor,90)
wait_for_user()