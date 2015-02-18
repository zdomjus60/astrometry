from time_func import *
import math
import random
import ephem
import numpy
import time, datetime
import swisseph
from vsop87c.planets import Planet 
planets = {'Earth': ephem.Sun, 'Mercury':ephem.Mercury, 'Venus':ephem.Venus,
           'Mars':ephem.Mars, 'Jupiter':ephem.Jupiter, 'Saturn':ephem.Saturn,
           'Uranus':ephem.Uranus, 'Neptune':ephem.Neptune}
swe_plan = {'Earth': 0, 'Mercury':2, 'Venus':3,
           'Mars':4, 'Jupiter':5, 'Saturn':6,
           'Uranus':7, 'Neptune':8}
c = []; d = []; e = []
for n in range(1000):
    year = random.randrange(-3000,3000)
    doty = random.randrange(1,365)
    date = cal2jul(year,1,1)+doty
    cal_date = jul2cal(date)
    year = cal_date[0]
    month = cal_date[1]
    day = cal_date[2]
#    print "\njulian date: %d calendar_date %s" % (date , str(cal_date))
#    print "%20s %12s %12s %12s %12s %12s %12s" % ('body','ephem','vsop87c','swisseph','diff1-2','diff2-3', 'diff1-3') 
    for body in planets:
        body_selected = planets[body](str(year)+"/"+str(month)+"/"+str(day), epoch = str(year)+"/"+str(month)+"/"+str(day))
        pos1 = math.degrees(ephem.Ecliptic(body_selected).lon)
        vsop87c_body = Planet(body, year, month, day)
        pos2 = vsop87c_body.calc()[1]
        diff12 = (pos2 - pos1)*3600
        pos3 = swisseph.calc(date, swe_plan[body])[0]
        diff23 = (pos3 - pos2)*3600
        diff13 = (pos3 - pos1)*3600
#        print "%20s %12.4f %12.4f %12.4f %12.4f %12.4f %12.4f" % (body, pos1, pos2, pos3, diff12, diff23, diff13)
        c.append(diff12)
        d.append(diff23)
        e.append(diff13)
print "\n" * 2
print "mean(stdev) ephem-vsop87c      %12.4f(%12.4f)" % (numpy.mean(c), numpy.std(c))
print "mean(stdev) vsop87c-swisseph   %12.4f(%12.4f)" % (numpy.mean(d), numpy.std(d))
print "mean(stdev) ephem-swisseph     %12.4f(%12.4f)" % (numpy.mean(e), numpy.std(e))

