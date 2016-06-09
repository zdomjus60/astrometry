# -*- coding: utf-8 -*-
from tools import *
#### testing unified tools ####
### trigonometric functions
print """function sin (in degrees) of
         0  : {}
         30 : {}
         60 : {}
         90 : {}
         120: {}
         150: {}
         180: {}
         270: {}
         360: {}""".format(
                 sin(0.),
                 sin(30.),
                 sin(60.),
                 sin(90.),
                 sin(120.),
                 sin(150.),
                 sin(180.),
                 sin(270.),
                 sin(360.))

print """function cos (in degrees) of
         0  : {}
         30 : {}
         60 : {}
         90 : {}
         120: {}
         150: {}
         180: {}
         270: {}
         360: {}""".format(
                 cos(0.),
                 cos(30.),
                 cos(60.),
                 cos(90.),
                 cos(120.),
                 cos(150.),
                 cos(180.),
                 cos(270.),
                 cos(360.))

print """atan2 of
        1     /   2: {}
        2     /   3: {}
        10    /   7: {}
        1000  / 239: {}""".format(
                atan2(1,2),
                atan2(2,3),
                atan2(10,7),
                atan2(1000,239))

print """convert negative angles to positive:
        -12.34  :  {}
        -45.26  :  {}
        -120.54 :  {}
        -198.22 :  {}
        -275.89 :  {}""".format(
                reduce360(-12.34),
                reduce360(-45.26),
                reduce360(-120.54),
                reduce360(-198.22),
                reduce360(-275.89))

### decimal to sexagesimal and viceversa

print '''convert 10° 20' 30" to  decimal:''',
conv = dms2ddd(10,20,30)
print conv
print '''   and viceversa to sexagesimal:''',
reconv = ddd2dms(conv)
print reconv

### julian date
print '''julian date of :
        01/01/1200 15h 43m 28s {}
        04/10/1582 00h 00m 00s {}
        15/10/1582 00h 00m 00s {}
        12/09/1785 12h 56m     {}
        01/06/2025 07h 12m     {}
        18/10/3045             {}'''.format(
            cal2jul(1200,1,1,15,43,28),
            cal2jul(1582,10,4,0,0,0),
            cal2jul(1582,10,15,0,0,0),
            cal2jul(1785,9,12,12,56),
            cal2jul(2025,6,1,7,12),
            cal2jul(3045,10,18))
print '''calendar date of jd:
        2159358.15519 {}
        2299159.5     {}
        2299160.5     {}
        2373273.03889 {}
        2460827.8     {}
        2833513.5     {}'''.format(
            jul2cal(2159358.15519),
            jul2cal(2299159.5),
            jul2cal(2299160.5 ),
            jul2cal(2373273.03889),
            jul2cal(2460827.8),
            jul2cal(2833513.5))
### day_of_the_week
test_date = (2016,1,1)
print "day of the week of 01/01/2016 :",day_of_the_week(2016,1,1)

### ecliptic obliquity JPL
print "ecliptic obliquity 01/01/2016 (JPL):    ", obl_ecl_JPL(2016,1,1)
print "ecliptic obliquity 01/01/2016 (Laskar): ", obl_ecl_Laskar(2016,1,1) 

### testing sin, cos, atan2
for i in range(360):
    print "angle {}, sin {}, cos {}, atan2 {}".format(
        i, sin(i), cos(i), reduce360(atan2(sin(i), cos(i))))

### testing conversion rectangular equatorial to ecliptic and viceversa
for xs in range(-100,100,100):
    for ys in range(-100,100,100):
        for zs in range(-100,100,100):
            r, ar, de = rect_equat2rect_ecl(xs,ys,zs,2000,1,1)
            x,  y,  z = rect_ecl2rect_equat(r,ar,de,2000,1,1)
            print xs,ys,zs,r,ar,de," - ",x,y,z

### testing spherical to rectangular and viceversa
xs = 1
ys = 2
zs = 3
print "x {}, y {}, z {}".format(xs,ys,zs)
r, longitude, latitude = rect_ecl2sph_ecl(x,y,z)
print "r {}, lg {}, lt {}".format(r,longitude, latitude)
x, y, z = sph_ecl2rect_ecl(r, longitude, latitude)
print "x {}, y {}, z {}".format(x,y,z)
