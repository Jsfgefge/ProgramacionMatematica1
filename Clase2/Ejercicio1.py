from swampy.TurtleWorld import*

world = TurtleWorld()
#Def dibujo
def dibujar_poligono(tortuga,lados,size):
    print(tortuga)
    for x in range(lados):
        fd(tortuga,size)
        lt(tortuga,360/lados)

bob=Turtle()
bob.delay = 0.00001
dibujar_poligono(bob,1024, 0.3)
wait_for_user()