import math
from trigon import *

def ecl2rect_ecl(longitude, latitude, r, obl_ecl):
    x = r * cos(longitude)
    y = r * sin(longitude)
    z = 0.0
    return (x,y,z)

def rect_ecl2equat(x,y,z):
    xequat = x
    yequat = y * cos(obl_ecl) 
