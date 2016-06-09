import math
from tools import *
class Sun:
    """
    See the following pages from Paul Schlyter:
        http://www.stjarnhimlen.se/comp/ppcomp.html
        http://www.stjarnhimlen.se/comp/tutorial.html
    Here the Sun position is determined according to the astronomical laws
    of elliptic motion.
    """
    
    def __init__(self, year, month, day, hour=0, minute=0, second=0):
        # no of days from epoch 1999/12/31 00hh00mm00ss
        self.d = cal2jul(year, month, day, hour, minute, second) - cal2jul(1999,12,31)
        #Orbital elements of the Sun:
        self.N = 0.0
        self.i = 0.0
        self.w = 282.9404 + 4.70935e-5 * self.d
        self.a = 1.0  
        self.e = 0.016709 - 1.151e-9 * self.d
        self.M = 356.0470 + 0.9856002585 * self.d
        self.obl_ecl = 23.4393 -3.563e-7 * self.d        
        self.L = self.w + self.M
        
    def params(self):
        E = self.M + 180.0/math.pi * self.e * sin(self.M)*(1 + self.e * cos(self.M)) 
        x = cos(E) - self.e
        y = sin(E) * math.sqrt(1 - self.e * self.e)
        mean_anomaly = atan2(y,x)
        r = math.sqrt(x*x+y*y)
        return (mean_anomaly, r)

    def longitude(self):
        hour, minute, second = ddd2dms(reduce360(self.params()[0] + self.w))
        return (hour, minute, second)

    def latitude(self):
        return (0,0,0)
    
    
