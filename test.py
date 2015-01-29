# calculate Sun longitude according to Paul Schlyter formulas
from time_func import *
from sun_schlyter import Sun
sun = Sun(1990,4,19)
print sun.longitude()
sun = Sun(1960,6,8,19,20,0)
print sun.longitude()
