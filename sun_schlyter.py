import math
from time_func import *
from trigon import *
class Sun:
    
    def __init__(self, year, month, day, hour=0, minute=0, second=0):
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
        
   
    def v(self):
        E = self.M + 180.0/math.pi * self.e * sin(self.M)*(1 + self.e * cos(self.M))
        x = cos(E) - self.e
        y = sin(E) * math.sqrt(1 - self.e*self.e)
        r = math.sqrt(x*x+y*y)
        return atan2(y,x)

    def longitude(self):
        return ddd2dms(reduce360(self.v() + self.w))
        
    
    
