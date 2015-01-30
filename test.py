# -*- coding: utf-8 -*-
# calculate Sun longitude according to Paul Schlyter formulas
from trigon import *
from planets import Planet
sun = Planet('Sun', 1990, 4, 19)
print sun.position()
moon = Planet('Moon', 1990, 4, 19)
print moon.position()
mercury = Planet('Mercury', 1990, 4, 19)
print mercury.position()
venus = Planet('Venus', 1990, 4, 19)
print venus.position()
mars = Planet('Mars', 1990, 4, 19)
print mars.position()
jupiter = Planet('Jupiter', 1990, 4, 19)
print jupiter.position()
saturn = Planet('Saturn', 1990, 4, 19)
print saturn.position()
uranus = Planet('Uranus', 1990, 4, 19)
print uranus.position()
neptune = Planet('Neptune', 1990, 4, 19)
print neptune.position()
pluto = Planet('Pluto', 1990, 4, 19)
print pluto.position()
