import gmpy2 as gmp

import struct

gmp.get_context().precision=200

def cal2jul(year, month, day, hour=0, minute =0, second=0):
    month2 = month
    year2 = year
    if month2 <= 2:
        year2 -= 1
        month2 += 12
    if (year*10000 + month*100 + day) > 15821015:
        a = int(year2/100)
        b = 2 - a + int(a/4)
    else:
        a = 0
        b = 0
    if year < 0:
        c = int((365.25 * year2)-0.75)
    else:
        c = int(365.25 * year2)
    d = int(30.6001 *(month2 + 1))
    return b + c + d + day + hour / 24.0 + minute / 1440.0 + second / 86400.0 + 1720994.5        




class VSOP2013():
    
    def __init__(self, t, planet, precision=1e-7):
        # calculate millennia from J2000
        self.JD = t
        self.t = gmp.div((t - cal2jul(2000,1,1,12)), 365250.0)
        # predefine powers of self.t
        self.power = []; self.power.append(gmp.mpfr(1.0)); self.power.append(self.t)
        for i in xrange(2,21):
            t = self.power[-1]
            self.power.append(gmp.mul(self.t,t))
        # choose planet file in a dict
        self.planet = planet
        self.planets = {'Mercury':'VSOP2013p1.dat',
                        'Venus'  :'VSOP2013p2.dat',
                        'EMB'    :'VSOP2013p3.dat',
                        'Mars'   :'VSOP2013p4.dat',
                        'Jupiter':'VSOP2013p5.dat',
                        'Saturn' :'VSOP2013p6.dat',
                        'Uranus' :'VSOP2013p7.dat',
                        'Neptune':'VSOP2013p8.dat',
                        'Pluto'  :'VSOP2013p9.dat'}
        # VSOP2013 routines precision
        self.precision = precision
        
        # lambda coefficients
        # l(1,13) : linear part of the mean longitudes of the planets (radian).
        # l(14): argument derived from TOP2013 and used for Pluto (radian).
        # l(15,17) : linear part of Delaunay lunar arguments D, F, l (radian).

        self.l = (
            (gmp.mpfr(4.402608631669), gmp.mpfr(26087.90314068555)),
            (gmp.mpfr(3.176134461576), gmp.mpfr(10213.28554743445)),
            (gmp.mpfr(1.753470369433), gmp.mpfr( 6283.075850353215)),
            (gmp.mpfr(6.203500014141), gmp.mpfr( 3340.612434145457)),
            (gmp.mpfr(4.091360003050), gmp.mpfr( 1731.170452721855)),
            (gmp.mpfr(1.713740719173), gmp.mpfr( 1704.450855027201)), 
            (gmp.mpfr(5.598641292287), gmp.mpfr( 1428.948917844273)),
            (gmp.mpfr(2.805136360408), gmp.mpfr( 1364.756513629990)),
            (gmp.mpfr(2.326989734620), gmp.mpfr( 1361.923207632842)),
            (gmp.mpfr(0.599546107035), gmp.mpfr(  529.6909615623250)),
            (gmp.mpfr(0.874018510107), gmp.mpfr(  213.2990861084880)),
            (gmp.mpfr(5.481225395663), gmp.mpfr(   74.78165903077800)),
            (gmp.mpfr(5.311897933164), gmp.mpfr(   38.13297222612500)),
            (gmp.mpfr(0.000000000000), gmp.mpfr(    0.3595362285049309)),
            (gmp.mpfr(5.198466400630), gmp.mpfr(77713.7714481804)),
            (gmp.mpfr(1.627905136020), gmp.mpfr(84334.6615717837)),
            (gmp.mpfr(2.355555638750), gmp.mpfr(83286.9142477147))
            )

        # planetary frequencies in longitude
        self.freqpla = {'Mercury'   :   gmp.mpfr(0.2608790314068555e5),  
                        'Venus'     :   gmp.mpfr(0.1021328554743445e5),
                        'EMB'       :   gmp.mpfr(0.6283075850353215e4),
                        'Mars'      :   gmp.mpfr(0.3340612434145457e4), 
                        'Jupiter'   :   gmp.mpfr(0.5296909615623250e3),  
                        'Saturn'    :   gmp.mpfr(0.2132990861084880e3),
                        'Uranus'    :   gmp.mpfr(0.7478165903077800e2),  
                        'Neptune'   :   gmp.mpfr(0.3813297222612500e2), 
                        'Pluto'     :   gmp.mpfr(0.2533566020437000e2)}  

        
            
        # target variables
        self.ax = gmp.mpfr(0.0)            # major semiaxis
        self.ml = gmp.mpfr(0.0)            # mean longitude
        self.kp = gmp.mpfr(0.0)            # e*cos(perielium longitude)
        self.hp = gmp.mpfr(0.0)            # e*sin(perielium longitude)
        self.qa = gmp.mpfr(0.0)            # sin(inclination/2)*cos(ascending node longitude)
        self.pa = gmp.mpfr(0.0)            # sin(inclination/2)*cos(ascending node longitude)
        
        self.tg_var = {'A':self.ax, 'L':self.ml, 'K':self.kp,
                       'H':self.hp, 'Q':self.qa, 'P':self.pa } 

        # eps  = (23.d0+26.d0/60.d0+21.41136d0/3600.d0)*dgrad
        self.eps = gmp.mpfr((23.0+26.0/60.0+21.411360/3600.0)*gmp.const_pi()/180.0)
        self.phi  = gmp.mpfr(-0.051880 * gmp.const_pi() / 180.0 / 3600.0)
        self.ceps = gmp.cos(self.eps)
        self.seps = gmp.sin(self.eps)
        self.cphi = gmp.cos(self.phi)
        self.sphi = gmp.sin(self.phi)
        
        # rotation of ecliptic -> equatorial rect coords
        self.rot = [[self.cphi, -self.sphi*self.ceps,  self.sphi*self.seps],
                    [self.sphi,  self.cphi*self.ceps, -self.cphi*self.seps],
                    [0.0,        self.seps,            self.ceps          ]]
        
        self.fmt = struct.Struct("""6s 3s 3s 3s 3s x 3s 3s 3s 3s 3s x 4s 4s 4s 4s x
                       6s x 3s 3s 3s 20s x 3s 20s x 3s x""")

        self.gmp_ = {
       'Mercury' : gmp.mpfr(4.9125474514508118699e-11),
       'Venus'   : gmp.mpfr(7.2434524861627027000e-10),
       'EMB'     : gmp.mpfr(8.9970116036316091182e-10),
       'Mars'    : gmp.mpfr(9.5495351057792580598e-11),
       'Jupiter' : gmp.mpfr(2.8253458420837780000e-07),
       'Saturn'  : gmp.mpfr(8.4597151856806587398e-08),
       'Uranus'  : gmp.mpfr(1.2920249167819693900e-08),
       'Neptune' : gmp.mpfr(1.5243589007842762800e-08),
       'Pluto'   : gmp.mpfr(2.1886997654259696800e-12)
       }

        self.gmsol = gmp.mpfr(2.9591220836841438269e-04)
        self.rgm = gmp.sqrt(self.gmp_[self.planet]+self.gmsol)
        # run calculus routine
        self.calc()
        

    def __str__(self):
        
        vsop_out = "{:3.13} {:3.13} {:3.13} {:3.13} {:3.13} {:3.13}\n".format(
                                          self.tg_var['A'],
                                          self.tg_var['L'],
                                          self.tg_var['K'],
                                          self.tg_var['H'],
                                          self.tg_var['Q'],
                                          self.tg_var['P'])
        vsop_out += "{:3.13} {:3.13} {:3.13} {:3.13} {:3.13} {:3.13}\n".format(
                                          self.ecl[0],
                                          self.ecl[1],
                                          self.ecl[2],
                                          self.ecl[3],
                                          self.ecl[4],
                                          self.ecl[5])
        vsop_out += "{:3.13} {:3.13} {:3.13} {:3.13} {:3.13} {:3.13}\n".format(
                                          self.equat[0],
                                          self.equat[1],
                                          self.equat[2],
                                          self.equat[3],
                                          self.equat[4],
                                          self.equat[5])
                        

        return vsop_out



    def calc(self):
        with open(self.planets[self.planet]) as file_in:
            terms = []
            b = '*'
            while b != '':
                b = file_in.readline()
                if b != '':
                    if b[:5] == ' VSOP':
                        header = b.split()
                        #print header[3], header[7], header[8], self.t**int(header[3])
                        no_terms = int(header[4])
                        for i in xrange(no_terms):
                            #6x,4i3,1x,5i3,1x,4i4,1x,i6,1x,3i3,2a24
                            terms = file_in.readline()
                            a = self.fmt.unpack(terms)
                            S = gmp.mul(gmp.mpfr(a[18]),gmp.exp10(int(a[19])))
                            C = gmp.mul(gmp.mpfr(a[20]),gmp.exp10(int(a[21])))
                            if gmp.sqrt(S*S+C*C) < self.precision:
                                break
                            aa = 0.0; bb = 0.0;
                            for j in xrange(1,18):
                                aa += gmp.mul(gmp.mpfr(a[j]), self.l[j-1][0])
                                bb += gmp.mul(gmp.mpfr(a[j]), self.l[j-1][1])
                            arg = aa + bb * self.t
                            power = int(header[3])
                            comp = self.power[power] * (S * gmp.sin(arg) + C * gmp.cos(arg))
                            if header[7] == 'L' and power == 1 and int(a[0]) == 1:
                                pass
                            else:
                                self.tg_var[header[7]] += comp
        self.tg_var['L'] = self.tg_var['L'] + self.t * self.freqpla[self.planet]
        self.tg_var['L'] = self.tg_var['L'] % (2 * gmp.const_pi())
        if self.tg_var['L'] < 0:
            self.tg_var['L'] += 2*gmp.const_pi()
        print "Julian date {}".format(self.JD)
        file_in.close()
        ##print self.tg_var
    
        ####    def ELLXYZ(self):

        xa = self.tg_var['A']
        xl = self.tg_var['L']
        xk = self.tg_var['K']
        xh = self.tg_var['H']
        xq = self.tg_var['Q']
        xp = self.tg_var['P']
        
        # Computation
  
        xfi = gmp.sqrt(1.0 -xk * xk - xh * xh)
        xki = gmp.sqrt(1.0 -xq * xq - xp * xp)
        u = 1.0/(1.0 + xfi)
        z = complex(xk, xh)
        ex = abs(z)
        ex2 = ex  * ex
        ex3 = ex2 * ex
        z1 = z.conjugate()
        #
        gl = xl % (2*gmp.const_pi())
        gm = gl - gmp.atan2(xh, xk)
        e  = gl + (ex - 0.1250 * ex3) * gmp.sin(gm)
        e += 0.50 * ex2 * gmp.sin(2.0 * gm)
        e += 0.3750 * ex3 * gmp.sin(3.0 * gm)
        #
        while True:
            z2 = complex(0.0, e)
            zteta = gmp.exp(z2)
            z3 = z1 * zteta
            dl = gl - e + z3.imag
            rsa = 1.0 - z3.real
            e = e + dl / rsa
            if abs(dl) < 1e-15:
                break
        #
        z1  =  u * z * z3.imag
        z2  =  gmp.mpc(z1.imag, -z1.real)
        zto = (-z+zteta+z2)/rsa
        xcw = zto.real
        xsw = zto.imag
        xm  = xp * xcw - xq * xsw
        xr  = xa * rsa
        #
        self.ecl = []; self.equ = {}
        self.ecl.append(xr * (xcw -2.0 *xp * xm))
        self.ecl.append(xr * (xsw +2.0 *xq * xm))
        self.ecl.append(-2.0 * xr * xki * xm)
        #
        xms = xa *(xh + xsw) / xfi
        xmc = xa *(xk + xcw) / xfi
        xn  = self.rgm / xa ** (1.50)
        #
        self.ecl.append( xn *((2.0 * xp * xp - 1.0) * xms + 2.0 * xp * xq * xmc))
        self.ecl.append( xn *((1.0 -2.0 * xq * xq) * xmc -2.0 * xp * xq * xms))
        self.ecl.append( 2.0 * xn * xki * (xp * xms + xq * xmc))
        
        # Equatorial rectangular coordinates and velocity

        #         
        #
        # --- Computation ------------------------------------------------------
        #
        self.equat = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]    
        for i in xrange(3):
           for j in xrange(3):
               self.equat[i]   = self.equat[i]   + self.rot[i][j] * self.ecl[j]
               self.equat[i+3] = self.equat[i+3] + self.rot[i][j] * self.ecl[j+3]



if __name__ == '__main__':
    for planet in ('Mercury', 'Venus', 'EMB', 'Mars', 'Jupiter',
          'Saturn', 'Uranus', 'Neptune', 'Pluto'):
        print "PLANETARY EPHEMERIS VSOP2013  "+ planet + "(TDB)\n"+""" 
  1/ Elliptic   Elements:    a (au), lambda (radian), k, h, q, p        - Dynamical Frame J2000
  2/ Ecliptic   Heliocentric Coordinates:  X,Y,Z (au)  X',Y',Z' (au/d)  - Dynamical Frame J2000
  3/ Equatorial Heliocentric Coordinates:  X,Y,Z (au)  X',Y',Z' (au/d)  - ICRS Frame J2000
"""
        init_date = cal2jul(1890,6,26,12)
        set_date = init_date

        while set_date < init_date + 41000:
            v = VSOP2013(set_date, planet)
            print v
            set_date += 4000
          
        
