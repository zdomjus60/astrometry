import math
from time_func import *
from trigon import *

class Planet:

    def __init__(self, planet, year, month, day, hour=0, minute=0, second=0):
        self.planet = planet
        self.d = cal2jul(year, month, day, hour, minute, second) - cal2jul(1999,12,31)
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.elements = {'Sun':{}, 'Moon':{}, 'Mercury':{},
                        'Venus':{}, 'Mars':{}, 'Jupiter':{},
                        'Saturn':{}, 'Uranus':{}, 'Neptune':{},
                        'Pluto':{}}
       
        self.elements[self.planet] = {
                 'N' : 0.0,
                 'i' : 0.0,
                 'w' : 282.9404 + 4.70935e-5 * self.d,
                 'a' : 1.000000,
                 'e' : 0.016709 - 1.151e-9 * self.d,
                 'M' : 356.0470 + 0.9856002585 * self.d}
        
        self.elements ['Moon'] = {
                 'N' : 125.1228 - 0.0529538083 * self.d,
                 'i' : 5.1454,
                 'w' : 318.0634 + 0.1643573223 * self.d,
                 'a' : 60.2666,
                 'e' : 0.054900,
                 'M' : 115.3654 + 13.0649929509 * self.d}

        self.elements['Mercury'] = {
                'N' :  48.3313 + 3.24587e-5 * self.d,
                'i' : 7.0047 + 5.00e-8 * self.d,
                'w' :  29.1241 + 1.01444e-5 * self.d,
                'a' : 0.387098,
                'e' : 0.205635 + 5.59e-10 * self.d,
                'M' : 168.6562 + 4.0923344368 * self.d}

        self.elements['Venus'] = {
                'N' :  76.6799 + 2.46590e-5 * self.d,
                'i' : 3.3946 + 2.75e-8 * self.d,
                'w' :  54.8910 + 1.38374e-5 * self.d,
                'a' : 0.723330,
                'e' : 0.006773 - 1.302e-9 * self.d,
                'M' :  48.0052 + 1.6021302244 * self.d}

        self.elements['Mars'] = {
                'N' :  49.5574 + 2.11081e-5 * self.d,
                'i' : 1.8497 - 1.78e-8 * self.d,
                'w' : 286.5016 + 2.92961e-5 * self.d,
                'a' : 1.523688,
                'e' : 0.093405 + 2.516e-9 * self.d,
                'M' :  18.6021 + 0.5240207766 * self.d}

        self.elements['Jupiter'] = {
                'N' : 100.4542 + 2.76854e-5 * self.d,
                'i' : 1.3030 - 1.557e-7 * self.d,
                'w' : 273.8777 + 1.64505e-5 * self.d,
                'a' : 5.20256,
                'e' : 0.048498 + 4.469e-9 * self.d,
                'M' :  19.8950 + 0.0830853001 * self.d}
            
        self.elements['Saturn'] = {
                'N' : 113.6634 + 2.38980e-5 * self.d,
                'i' : 2.4886 - 1.081e-7 * self.d,
                'w' : 339.3939 + 2.97661e-5 * self.d,
                'a' : 9.55475,
                'e' : 0.055546 - 9.499e-9 * self.d,
                'M' : 316.9670 + 0.0334442282 * self.d},
            
        self.elements['Uranus'] = {
                'N' :  74.0005 + 1.3978e-5 * self.d,
                'i' : 0.7733 + 1.9e-8 * self.d,
                'w' :  96.6612 + 3.0565e-5 * self.d,
                'a' : 19.18171 - 1.55e-8 * self.d,
                'e' : 0.047318 + 7.45e-9 * self.d,
                'M' : 142.5905 + 0.011725806 * self.d},
            
        self.elements['Neptune'] = {
                'N' : 131.7806 + 3.0173e-5 * self.d,
                'i' : 1.7700 - 2.55e-7 * self.d,
                'w' : 272.8461 - 6.027e-6 * self.d,
                'a' : 30.05826 + 3.313e-8 * self.d,
                'e' : 0.008606 + 2.15e-9 * self.d,
                'M' : 260.2471 + 0.005995147 * self.d}

    def position(self):
        if self.planet == 'Sun':
            obl_ecl = 23.4393 - 3.563e-7 * self.d
            w = self.elements[self.planet]['w']
            a = self.elements[self.planet]['a']
            M = self.elements[self.planet]['M']
            e = self.elements[self.planet]['e']
            L = w + M
            E = M + math.degrees(e) * sin(M) * (1.0 + e * cos(M))
            xv = cos(E) - e
            yv = math.sqrt(1.0 - e*e) * sin(E)
            r = math.sqrt(xv*xv + yv*yv)
            self.elements[self.planet]['distance']=r
            v = atan2( yv, xv )
            lon = reduce360(v + w)
            lat = 0
            xs = r * cos(lon)
            ys = r * sin(lon)
            zs = 0
            xe = xs
            ye = ys * cos(obl_ecl)
            ze = ys * sin(obl_ecl)
            RA  = atan2(ye, xe)
            Decl = atan2(ze, math.sqrt(xe*xe+ye*ye))
            self.elements[self.planet]['longitude'] = ddd2dms(lon)
            self.elements[self.planet]['latitude'] = ddd2dms(lat)
            self.elements[self.planet]['right ascension'] = ddd2dms(RA)
            self.elements[self.planet]['declination'] = ddd2dms(Decl)
            
            return  (self.elements[self.planet]['distance'],
                     self.elements[self.planet]['longitude'],
                     self.elements[self.planet]['latitude'],
                     self.elements[self.planet]['right ascension'],
                     self.elements[self.planet]['declination'])
    
                 
                 
    
