import swisseph
from planets import *
from tools import *
from moon_meeus import moon_meeus

year = 1960
month = 3
print "Date(Y/M/A)\tlong_planets\tlong_moon_meeus\tlong_swisseph\t   diff1:3\t   diff2:3"
for day in range(1,32):
    g1 = Planet('Moon', year, month, day).position()[1]
    g2 = moon_meeus(year, month, day)[1]
    g3 = swisseph.calc(swisseph._julday(year, month, day, 0, 0, 0),1)[0]
    d13 = (g3-g1)*3600
    d23 = (g3-g2)*3600
    print "%4d %2d %2d %15.4f %15.4f %15.4f %15.4f %15.4f" % (year, month, day, g1, g2, g3, d13, d23)
    

        
