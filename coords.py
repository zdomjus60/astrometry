import math
from time_func import *
from trigon import *

""" Some conversion utilities between various coordinate systems """

def sph_ecl2rect_ecl(r, longitude, latitude):
    x = r * cos(latitude) * cos(longitude)
    y = r * cos(latitude) * sin(longitude)
    z = r * sin(latitude)
    return (x,y,z)

def rect_ecl2sph_ecl(x,y,z):
    r = math.sqrt(x*x + y*y +z*z)
    longitude = atan2(y,x)
    latitude = atan2(z, math.sqrt(x*x + y*y))
    return (r, longitude, latitude)

def sph_equat2rect_equat(r, RA, Declination):
    x = r * cos(Declination) * cos(RA)
    y = r * cos(Declination) * sin(RA)
    z = r * sin(Declination)
    return (x,y,x)

def rect_equat2sph_equat(x,y,z):
    r = math.sqrt(x*x + y*y +z*z)
    RA = atan2(y,x)
    Decl = atan2(z, math.sqrt(x*x + y*y))
    return (r, RA, Decl)
    
def rect_ecl2equat(xeclip, yeclip, zeclip):
    xequat = xeclip
    yequat = y * cos(obl_ecl)- zeclip * sin(obl_ecl)
    zequat = yeclip * sin(obl_ecl) + zeclip * cos(obl_ecl)
    return (xequat, yequat, zequat)

if __name__ == '__main__':
    x,y,z = (sph_ecl2rect_ecl(5,60, 30))
    print x,y,z
    print rect_ecl2sph_ecl(x,y,z)
    
