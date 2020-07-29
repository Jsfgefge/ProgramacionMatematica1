from swampy.TurtleWorld import *
####################################################################################################
World = TurtleWorld()
bob = Turtle()
print(bob)
'''
#Dibujando un cuadradowo
fd(bob, 100)
lt(bob)
fd(bob, 100)
lt(bob)
fd(bob,100)
lt(bob)
fd(bob,100)
'''

for x in range(0,4):
    fd(bob, 100)
    lt(bob)

lt(bob,30)
fd(bob,50)
wait_for_user()

