import math
import swisseph
from planets import *
from time_func import *
from trigon import *
from vsop87 import earth, mercury, venus, mars, jupiter, saturn, uranus, neptune
import random

print "Date(Y/M/A)\tlong_planets\tlong_vsop87\tlong_swisseph\t   diff1:3\t   diff2:3\t   diff1:2"
for i in range(10):

    year = random.randint(1600, 2100)
    month = random.randint(1,12)
    day = random.randint(1,30)
    g1 = Planet('Saturn', year, month, day).position()[1]
    t = jul_millennia(year, month, day)
    pos = earth.Earth(t).calculate()
    lt = pos[0]
    bt = pos[1]
    rt = pos[2]
    pos = saturn.Saturn(t).calculate()
    lp = pos[0]
    bp = pos[1]
    rp = pos[2]
    x = rp*math.cos(bp)*math.cos(lp)-rt*math.cos(bt)*math.cos(lt)
    y = rp*math.cos(bp)*math.sin(lp)-rt*math.cos(bt)*math.sin(lt)
    z = rp*math.sin(bp)-rt*math.sin(bt)
    longitude = math.atan2(y,x)
    if longitude < 0:
        longitude += 2*math.pi
    latitude = math.atan(z/math.sqrt(x*x+y*y))
    longitude = math.degrees(longitude)
    latitude = math.degrees(latitude)
    g2 = longitude
    g3 = swisseph.calc(swisseph._julday(year, month, day,0,0,0),6)[0]
    d13 = (g3-g1)*3600
    d23 = (g3-g2)*3600
    d12 = (g2-g1)*3600
    print "%4d %2d %2d %15.4f %15.4f %15.4f %15.4f %15.4f %15.4f" % (year, month, day, g1, g2, g3, d13, d23, d12)
    

        
