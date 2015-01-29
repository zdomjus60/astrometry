# calculate Sun longitude according to Paul Schlyter formulas
from time_func import *
from sun_schlyter import Sun
sun = Sun(1990,4,19)
print sun.longitude()
