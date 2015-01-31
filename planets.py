import math
from time_func import *
from trigon import *

class Planet:
    """ Planets position computing (planets as Astrology classifyes them:
        Sun, Moon and solar sistem planets up to Pluto.
        Methods taken from Paul Schlyter pages:
        http://www.stjarnhimlen.se/comp/ppcomp.html   How to compute planetary positions
        http://www.stjarnhimlen.se/comp/tutorial.html Computing planetary positions - a tutorial with worked examples
    """    
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
       
        self.elements['Sun'] = {
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
                'M' : 316.9670 + 0.0334442282 * self.d}
            
        self.elements['Uranus'] = {
                'N' :  74.0005 + 1.3978e-5 * self.d,
                'i' : 0.7733 + 1.9e-8 * self.d,
                'w' :  96.6612 + 3.0565e-5 * self.d,
                'a' : 19.18171 - 1.55e-8 * self.d,
                'e' : 0.047318 + 7.45e-9 * self.d,
                'M' : 142.5905 + 0.011725806 * self.d}
            
        self.elements['Neptune'] = {
                'N' : 131.7806 + 3.0173e-5 * self.d,
                'i' : 1.7700 - 2.55e-7 * self.d,
                'w' : 272.8461 - 6.027e-6 * self.d,
                'a' : 30.05826 + 3.313e-8 * self.d,
                'e' : 0.008606 + 2.15e-9 * self.d,
                'M' : 260.2471 + 0.005995147 * self.d}

    def position(self):
        """ Given the planet name ('Sun' 'Moon' 'Mercury' 'Venus' 'Mars' 'Jupiter' 'Saturn'
            'Uranus' 'Neptune' 'Pluto'), this methods returns a tuple containing:
            - geocentric distance (UA for all planets excepts Moon (Earth radii)
            - longitude in degrees 
            - latitude in degrees 
            - right ascension in degrees
            - declination in degrees
            Call to this routine are made instantiating the class with the planet name and date
            (year, month, day) and time (hour, minute, second). By default time is set to 0h0000:
            print Planet('Saturn', 2001, 4, 1, 13, 20, 6).position()
            The orbital elements for the given date can also be accessed as a dictionary:
            Planet('Saturn', 2001, 4, 1, 13, 20, 6).elements['Saturn']
        """
        obl_ecl = 23.4393 - 3.563e-7 * self.d
        N = self.elements['Sun']['N']
        i = self.elements['Sun']['i']
        w = self.elements['Sun']['w']
        a = self.elements['Sun']['a']
        M = self.elements['Sun']['M']
        e = self.elements['Sun']['e']
 
        # Sun position computing
        L = w + M
        E = M + math.degrees(e) * sin(M) * (1.0 + e * cos(M))
        xv = cos(E) - e
        yv = math.sqrt(1.0 - e*e) * sin(E)
        r = math.sqrt(xv*xv + yv*yv)
        self.elements['Sun']['distance']=r
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
        self.elements['Sun']['x_eclip'] = xs
        self.elements['Sun']['y_eclip'] = ys
        self.elements['Sun']['z_eclip'] = zs 

        if self.planet == 'Sun':
            # when explicitely called 
            self.elements[self.planet]['longitude'] = reduce360(lon)
            self.elements[self.planet]['latitude'] = lat
            self.elements[self.planet]['right ascension'] = reduce360(RA)
            self.elements[self.planet]['declination'] = Decl
            
            return  (self.elements[self.planet]['distance'],
                     self.elements[self.planet]['longitude'],
                     self.elements[self.planet]['latitude'],
                     self.elements[self.planet]['right ascension'],
                     self.elements[self.planet]['declination'])
        elif self.planet != 'Pluto':
            N = self.elements[self.planet]['N']
            i = self.elements[self.planet]['i']
            w = self.elements[self.planet]['w']
            a = self.elements[self.planet]['a']
            M = self.elements[self.planet]['M']
            e = self.elements[self.planet]['e']

            E = M + math.degrees(e) * sin(M) * (1.0 + e * cos(M))
            E0 = E
            E1 = 0
            while (abs(E0-E1)>.001):
                E0 = E1
                E1 = E0 - ( E0 - math.degrees(e)* sin(E0) - M ) / ( 1 - e * cos(E0) )
            E = E1
            x = a * (cos(E) - e)
            y = a * math.sqrt(1 - e * e) * sin(E)
            r = math.sqrt( x*x + y*y )
            v = atan2( y, x )
            xeclip = r * ( cos(N) * cos(v+w) - sin(N) * sin(v+w) * cos(i) )
            yeclip = r * ( sin(N) * cos(v+w) + cos(N) * sin(v+w) * cos(i) )
            zeclip = r * sin(v+w) * sin(i)
            lon = atan2( yeclip, xeclip )
            lat = atan2( zeclip, math.sqrt(xeclip*xeclip+yeclip*yeclip) )
            # mean anomaly of Jupiter, Saturn, Uranus for later perturbations
            # computing
            Mj = self.elements['Jupiter']['M']
            Ms = self.elements['Saturn']['M']
            Mu = self.elements['Uranus']['M']
            if self.planet == 'Moon':

                E = M + math.degrees(e) * sin(M) * (1.0 + e * cos(M))
                E0 = E
                E1 = 0
                while (abs(E0-E1)>.001):
                    E0 = E1
                    E1 = E0 - ( E0 - math.degrees(e)* sin(E0) - M ) / ( 1 - e * cos(E0) )
                E = E1
                x = a * (cos(E) - e)
                y = a * math.sqrt(1 - e * e) * sin(E)
                r = math.sqrt( x*x + y*y )
                v = atan2( y, x )
                xeclip = r * ( cos(N) * cos(v+w) - sin(N) * sin(v+w) * cos(i) )
                yeclip = r * ( sin(N) * cos(v+w) + cos(N) * sin(v+w) * cos(i) )
                zeclip = r * sin(v+w) * sin(i)
                lon = atan2( yeclip, xeclip )
                lat = atan2( zeclip, math.sqrt(xeclip*xeclip+yeclip*yeclip) )
                # perturbations
                Ls = self.elements['Sun']['w'] + self.elements['Sun']['M']
                Lm = N+w+M
                Ms = self.elements['Sun']['M']
                Mm = M
                D = Lm - Ls
                F = Lm - N
                # in longitude            
                lon -= 1.274 * sin(Mm - 2*D)        #(Evection)
                lon += 0.658 * sin(2*D)             #(Variation)
                lon -= 0.186 * sin(Ms)              #(Yearly equation)
                lon -= 0.059 * sin(2*Mm - 2*D)
                lon -= 0.057 * sin(Mm - 2*D + Ms)
                lon += 0.053 * sin(Mm + 2*D)
                lon += 0.046 * sin(2*D - Ms)
                lon += 0.041 * sin(Mm - Ms)
                lon -= 0.035 * sin(D)               #(Parallactic equation)
                lon -= 0.031 * sin(Mm + Ms)
                lon -= 0.015 * sin(2*F - 2*D)
                lon += 0.011 * sin(Mm - 4*D)
                # in latitude
                lat -= 0.173 * sin(F - 2*D)
                lat -= 0.055 * sin(Mm - F - 2*D)
                lat -= 0.046 * sin(Mm + F - 2*D)
                lat += 0.033 * sin(F + 2*D)
                lat += 0.017 * sin(2*Mm + F)
                # in distance (Earth radii)
                r -= 0.58 * cos(Mm - 2*D)
                r -= 0.46 * cos(2*D)

                self.elements[self.planet]['distance'] = r
                self.elements[self.planet]['longitude'] = reduce360(lon)
                self.elements[self.planet]['latitude'] = lat

                xeclip = r * cos(lat) * cos(lon)
                yeclip = r * cos(lat) * sin(lon)
                zeclip = r * sin(lat)
                xequat = xeclip
                yequat = yeclip * cos(obl_ecl) - zeclip * sin(obl_ecl)
                zequat = yeclip * sin(obl_ecl) + zeclip * cos(obl_ecl)

                RA = atan2 (yequat, xequat)
                Decl = atan2 (zequat, math.sqrt(xequat*xequat+yequat*yequat))
                self.elements[self.planet]['right ascension'] = reduce360(RA)
                self.elements[self.planet]['declination'] = Decl
                
                return  (self.elements[self.planet]['distance'],
                         self.elements[self.planet]['longitude'],
                         self.elements[self.planet]['latitude'],
                         self.elements[self.planet]['right ascension'],
                         self.elements[self.planet]['declination'])

            elif self.planet == 'Jupiter':
                lon -= 0.332 * sin(2*Mj - 5*Ms - 67.6)
                lon -= 0.056 * sin(2*Mj - 2*Ms + 21)
                lon += 0.042 * sin(3*Mj - 5*Ms + 21)
                lon -= 0.036 * sin(Mj - 2*Ms)
                lon += 0.022 * cos(Mj - Ms)
                lon += 0.023 * sin(2*Mj - 3*Ms + 52)
                lon -= 0.016 * sin(Mj - 5*Ms - 69)

            elif self.planet == 'Saturn':
                lon += 0.812 * sin(2*Mj - 5*Ms - 67.6)
                lon -= 0.229 * cos(2*Mj - 4*Ms - 2)
                lon += 0.119 * sin(Mj - 2*Ms - 3)
                lon += 0.046 * sin(2*Mj - 6*Ms - 69)
                lon += 0.014 * sin(Mj - 3*Ms + 32)

                lat -= 0.020 * cos(2*Mj - 4*Ms - 2)
                lat += 0.018 * sin(2*Mj - 6*Ms - 49)

            elif self.planet == 'Uranus':
                lon += 0.040 * sin(Ms - 2*Mu + 6)
                lon += 0.035 * sin(Ms - 3*Mu + 33)
                lon -= 0.015 * sin(Mj - Mu + 20)

        else:
            S  =   50.03  +  0.033459652 * self.d
            P  =  238.95  +  0.003968789 * self.d
            lon = 238.9508  +  0.00400703 * self.d
            lon = lon - 19.799 * sin(P) + 19.848 * cos(P)
            lon = lon + 0.897 * sin(2*P) - 4.956 * cos(2*P)
            lon = lon + 0.610 * sin(3*P) + 1.211 * cos(3*P)
            lon = lon - 0.341 * sin(4*P) - 0.190 * cos(4*P)
            lon = lon + 0.128 * sin(5*P) - 0.034 * cos(5*P)
            lon = lon - 0.038 * sin(6*P) + 0.031 * cos(6*P)
            lon = lon + 0.020 * sin(S-P) - 0.010 * cos(S-P)
            lat =  -3.9082
            lat = lat - 5.453 * sin(P)   - 14.975 * cos(P)
            lat = lat + 3.527 * sin(2*P) + 1.673 * cos(2*P)
            lat = lat - 1.051 * sin(3*P) + 0.328 * cos(3*P)
            lat = lat + 0.179 * sin(4*P) - 0.292 * cos(4*P)
            lat = lat + 0.019 * sin(5*P) + 0.100 * cos(5*P)
            lat = lat - 0.031 * sin(6*P) - 0.026 * cos(6*P)
            lat = lat + 0.011 * cos(S-P)

            r     =  40.72
            r = r + 6.68 * sin(P)   + 6.90 * cos(P)
            r = r - 1.18 * sin(2*P) - 0.03 * cos(2*P)
            r = r + 0.15 * sin(3*P) - 0.14 * cos(3*P)
        
        x_geo_eclip = r * cos(lat) * cos(lon) + self.elements['Sun']['x_eclip']
        y_geo_eclip = r * cos(lat) * sin(lon) + self.elements['Sun']['y_eclip']
        z_geo_eclip = r * sin(lat)            + self.elements['Sun']['z_eclip']
        
        lon_geo = reduce360(atan2(y_geo_eclip, x_geo_eclip))
        lat_geo = atan2( z_geo_eclip, math.sqrt (x_geo_eclip*x_geo_eclip + y_geo_eclip*y_geo_eclip))
        r_geo = math.sqrt(x_geo_eclip*x_geo_eclip+y_geo_eclip*y_geo_eclip+z_geo_eclip*z_geo_eclip) 

        x_geo_equat = x_geo_eclip
        y_geo_equat = y_geo_eclip * cos(obl_ecl) - z_geo_eclip * sin(obl_ecl)
        z_geo_equat = y_geo_eclip * sin(obl_ecl) + z_geo_eclip * cos(obl_ecl)

        RA_geo      = reduce360(atan2(y_geo_equat, x_geo_equat))
        Decl_geo    = atan2(z_geo_equat, math.sqrt(x_geo_equat*x_geo_equat + y_geo_equat*y_geo_equat))
        r_geo = math.sqrt(x_geo_equat*x_geo_equat+y_geo_equat*y_geo_equat+z_geo_equat*z_geo_equat) 

        self.elements[self.planet]['distance'] = r_geo
        self.elements[self.planet]['longitude'] = reduce360(lon_geo)
        self.elements[self.planet]['latitude'] = lat_geo
        self.elements[self.planet]['right ascension'] = reduce360(RA_geo)
        self.elements[self.planet]['declination'] = Decl_geo
        
        return  (self.elements[self.planet]['distance'],
                 self.elements[self.planet]['longitude'],
                 self.elements[self.planet]['latitude'],
                 self.elements[self.planet]['right ascension'],
                 self.elements[self.planet]['declination'])
        
