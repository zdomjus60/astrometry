import math
from time_fn import *
from trigon import *
from earth import Earth
from mercury import Mercury
from venus import Venus
from mars import Mars
from jupiter import Jupiter
from saturn import Saturn
from uranus import Uranus
from neptune import Neptune

class Planet:

    def __init__(self, planet, year, month, day, hour=0, minute =0, second=0):
        self.planet = planet
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.planet_list = {'Earth':Earth, 'Mercury':Mercury, 'Venus':Venus, 'Mars':Mars,
                            'Jupiter':Jupiter, 'Saturn':Saturn, 'Uranus':Uranus, 'Neptune':Neptune}


    def calc(self):
        t = julian_millennia(self.year, self.month, self.day,
                             self.hour, self.minute, self.second)
        if self.planet in self.planet_list:
            body = self.planet_list[self.planet](t).calculate()
            earth = self.planet_list['Earth'](t).calculate()
            x = body[0]-earth[0]
            y = body[1]-earth[1]
            z = body[2]-earth[2]
            r = math.sqrt(x*x + y*y + z*z)
            longitude = atan2(y,x) % 360 
            latitude = atan2(z, math.sqrt(x*x + y*y))
            obl_ecl = obl_ecl_Laskar(self.year, self.month, self.day, self.hour, self.minute, self.second)
            f0 = sin(obl_ecl)*sin(longitude)*cos(latitude) + cos(obl_ecl)*sin(latitude)
            f1 = cos(longitude)*cos(latitude)
            f2 = cos(obl_ecl)*sin(longitude)*cos(latitude) - sin(obl_ecl)*sin(latitude)
            RA = atan2(f2,f1) % 360
            r0 = math.sqrt(f1*f1 + f2*f2)
            Decl = atan2(f0,r0)
            return (r, longitude, latitude, RA, Decl)
        
        
if __name__ == '__main__':
    for i in ('Mercury', 'Venus', 'Mars', 'Jupiter',
              'Saturn', 'Uranus', 'Neptune'):
        year, month, day = 2011,4,19
        planet = Planet(i, year, month, day).calc()
        print i, ddd2dms(planet[3]/15), ddd2dms(planet[4])
