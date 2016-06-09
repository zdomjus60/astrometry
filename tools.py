# -*- coding: utf-8 -*-
""" helper functions for time management
"""
import math

def sin(x):
        return math.sin(math.radians(x))

def cos(x):
	return math.cos(math.radians(x))

def atan2(y , x):
	return math.degrees(math.atan2(y, x))

def reduce360(x):
	return x % 360.0

def dms2ddd(hour, minute, second):
    """ from sexagesimal to decimal """
    return hour+minute/60.0+second/3600.0

def ddd2dms(dec_hour):
    """ from decimal to sexagesimal representation of hours and angles."""
    if dec_hour < 0:
        sign = -1
        dec_hour *= sign
    else:
        sign = 1
    total_seconds = int(dec_hour * 3600.0+.5)
    seconds = total_seconds % 60 
    total_minutes = int((total_seconds - seconds)/60.0)
    minutes = total_minutes % 60 
    hours = int((total_minutes - minutes)/60.0)
    return (hours * sign, minutes * sign, seconds * sign)

def cal2jul(year, month, day, hour=0, minute=0, second=0):
    """ converts calendar date to julian date
        this routine and the following are built following Duffet Smith /Zwart instructions
        as given in Peter Duffett-Smith-Zwart Practical Astronomy with your Calculator or Spreadsheet
        Fourth Edition, Cambridge University Press, Fourth Ed. 2011
        For an easier use of the function, hours minutes and seconds are defaulted to 0, so it's
        not necessary to give them as parameters when the hour is 00:00:00 
    """
    month2 = month
    year2 = year
    if month2 <= 2:
        year2 -= 1
        month2 += 12
    else:
        pass
    if (year*10000 + month*100 + day) >= 15821015:
        a = math.trunc(year2/100.0)
        b = 2 - a + math.trunc(a/4.0)
    else:
        a = 0
        b = 0
    if year < 0:
        c = math.trunc((365.25 * year2)-0.75)
    else:
        c = math.trunc(365.25 * year2)
    d = math.trunc(30.6001 *(month2 + 1))
    return b + c + d + day + hour / 24.0 + minute / 1440.0 + second / 86400.0 + 1720994.5

def jul2cal(jd):
    """ converts julian date to calendar date """
    jd += 0.5
    i = math.modf(jd)[1]
    f = math.modf(jd)[0]
    if i > 2299160:
        a = math.trunc((i-1867216.25)/36524.25)
        b = i + a - math.trunc(a/4)+1
    else:
        b = i
    c = b + 1524
    d = math.trunc((c-122.1)/365.25)
    e = math.trunc(365.25 * d)
    g = math.trunc((c-e)/30.6001)
    day = c-e+f-math.trunc(30.6001*g)
    if g < 13.5:
        month = g - 1
    else:
        month = g - 13
    if month > 2.5:
        year = d - 4716
    else:
        year = d - 4715
    
    hours_frac = math.modf(day)[0]*24
    day = int(day)
    hour, minute, second = ddd2dms(hours_frac) 
    return (year, month, day, hour, minute, second)

def day_of_the_week(year, month, day):
    """ given a calendar date, the routine returns a tuple with the Day Of The Week in number and in plaintext
        0 for Sunday 1 for Monday and so on up to 6 Saturday
    """
    doth = {0:'Sunday', 1:'Monday', 2:'Tuesday',
            3:'Wednesday', 4:'Thursday', 5:'Friday',
            6:'Saturday'}
    jd = cal2jul(year, month, day, 0, 0, 0)
    a = (jd+1.5)/7
    f = math.trunc((a % 1)*7 +.5)
    return (f,doth[f])

def lt2ut(year, month, day, hour=0, minute=0, second=0, timezone=0, DS=0):
    """ Given, for a location on the Earth,a date, a time, a timezone (East + West - in hours) and the Daylight
        Savings (0 normal time 1 Daylight Savings), this routine gives back a calendar date in Universal Time
        representation (year, month, day, hour, minute, second).
        It aims to restore a common date and time for all places in the Earth. Timezone and
        Daylight Savings can be automized knowing the location using the pytz module (Olson
        database)
    """
    ut = dms2ddd(hour,minute,second) - timezone - DS
    greenwich_calendar_date = day + ut/24
    jd = cal2jul(year, month, greenwich_calendar_date)
    greenwich_calendar_date = jul2cal(jd)
    return greenwich_calendar_date

def ut2lt(year, month, day, hour=0, minute=0, second=0, timezone=0, DS=0):
    """ Given a date, a time for Greenwich in UT format this routine gives back a calendar date
        in local time representation (year, month, day, hour, minute, second).
        It's the inverse function of the previous formula 
    """
    lt = dms2ddd(hour,minute,second) + timezone +DS
    local_calendar_date = day + lt/24
    jd = cal2jul(year, month, local_calendar_date)
    local_calendar_date = jul2cal(jd)
    return local_calendar_date

def ut2gst(year, month, day, hour, minute, second):
    """ Sidereal time is a time-keeping system astronomers use to keep track of the direction to point
        their telescopes to view a given star in the night sky.
        Briefly, sidereal time is a "time scale that is based on the Earth's rate of rotation measured
        relative to the fixed stars." (source Wikipedia)
        This routine converts Universal Time to Sidereal Time for Greenwich (Greenwich Sidereal Time)
    """
    jd = cal2jul(year, month, day)
    S = jd - 2451545.0
    T = S/36525.0
    T0 = (6.697374558 + (2400.051336 * T)+ 0.000025862 *T*T) % 24
    UT = dms2ddd(hour, minute, second)*1.002737909
    GST = ddd2dms((UT + T0) % 24)
    return GST
    
def gst2ut( year, month, day, hour, minute, second):
    """ Inverse of the previous function
    """
    jd = cal2jul(year, month, day, 0,0,0)
    S = jd - 2451545.0
    T = S/36525.0
    T0 = (6.697374558 + 2400.051336 * T + 0.000025862 *T*T) % 24
    GST = (dms2ddd(hour, minute, second) - T0) % 24
    while GST <0:
        GST += 24
    UT = GST * .9972695663
    return ddd2dms(UT)

def gst2lst( hour, minute, second, long_degree, long_minute, long_second=0):
    """ Corrects GST for a different location on the Earth
    """
    GST = dms2ddd(hour,minute,second)
    lg = dms2ddd(long_degree, long_minute, long_second)/15
    lst = ddd2dms((GST + lg) % 24)
    return lst

def lst2gst( hour, minute, second, long_degree, long_minute, long_second=0):
    """ Inverse of the previous method
    """
    lst = dms2ddd(hour,minute,second)
    lg = dms2ddd(long_degree, long_minute, long_second)/15
    GST = ddd2dms((lst + lg) % 24)
    return GST
    
def julian_centuries(year, month, day, hour=0, minute =0, second=0):
    
    d1 = cal2jul(year, month, day, hour, minute, second)
    d2 = cal2jul(2000,1,1,12)
    return (d1-d2) / 36525.0

def julian_millennia(year, month, day, hour=0, minute =0, second=0):
    return julian_centuries(year, month, day, hour, minute, second) / 10.0

def julian_decamillennia(year, month, day, hour=0, minute =0, second=0):
    return julian_centuries(year, month, day, hour, minute, second) / 100.0

def obl_ecl_JPL(year, month, day, hour=0, minute = 0, second = 0):

    t = julian_centuries(year, month, day, hour, minute, second)
    
    """ from JPL Astronomical Almanac 2010 """
    return (23 * 3600 + 26*60 + 21.406
                        - 46.836769  * t
                        - 0.0001831  * t * t
                        + 0.00200340 * t * t * t
                        - 0.576e-6   * t * t * t * t
                        - 4.34e-8    * t * t * t * t * t) / 3600.0



def obl_ecl_Laskar(year, month, day, hour = 0, minute = 0, second = 0):

    """
    Original work from Jay Tanner
    - converted to Python code by Domenico Mustara 2015 
    This PHP function computes the mean obliquity of the ecliptic
    given a JD argument corresponding to any given date and time.

    Author: Jay Tanner - 2010

    The algorithm used here is based on work published by J. Laskar
    Astronomy and Astrophysics, Vol 157, p68 (1986),
    New Formulas for the Precession, Valid Over 10000 years,
    Table 8.

    Source code provided under the provisions of the
    GNU Affero General Public License (AGPL), version 3.
    http://www.gnu.org/licenses/agpl.html

    // -----------------------------------------------------------
    // Compute the (t) value in Julian decamillennia corresponding
    // to the JD argument and reckoned from J2000.
       $t = ($JD - 2451545.0) / 3652500.0;

    // --------------------------------------
    """
    t = julian_decamillennia(year, month, day, hour, minute, second)
    w  = 84381.448
    w -=  4680.93 * t  
    w -=     1.55 * t * t
    w +=  1999.25 * t * t * t 
    w -=    51.38 * t * t * t * t
    w -=   249.67 * t * t * t * t * t
    w -=    39.05 * t * t * t * t * t * t
    w +=     7.12 * t * t * t * t * t * t * t
    w +=    27.87 * t * t * t * t * t * t * t * t
    w +=     5.79 * t * t * t * t * t * t * t * t * t
    w +=     2.45 * t * t * t * t * t * t * t * t * t * t

    return w / 3600.0



""" Some conversion utilities between various coordinate systems """

def sph_ecl2rect_ecl(r, longitude, latitude):
    x = r * cos(latitude) * cos(longitude)
    y = r * cos(latitude) * sin(longitude)
    z = r * sin(latitude)
    return (x,y,z)

def rect_ecl2sph_ecl(x,y,z):
    r = math.sqrt(x*x + y*y + z*z)
    longitude = atan2(y,x)
    latitude = atan2(z, math.sqrt(x*x + y*y))
    return (r, longitude, latitude)

def sph_equat2rect_equat(r, RA, Declination):
    x = r * cos(RA) * cos(Declination)
    y = r * sin(RA) * cos(Declination)
    z = r * sin(Declination)
    return (x,y,x)

def rect_equat2sph_equat(x,y,z):
    r = math.sqrt(x*x + y*y +z*z)
    RA = atan2(y, x)
    Decl = atan2(z, math.sqrt(x*x + y*y))
    return (r, RA, Decl)
    
def rect_ecl2rect_equat(xeclip, yeclip, zeclip, year, month, day, hour = 0, minute = 0, second = 0):
    oblecl = obl_ecl_JPL(year, month, day, hour, minute, second)
    xequat = xeclip
    yequat = yeclip * cos(oblecl) - zeclip * sin(oblecl)
    zequat = yeclip * sin(oblecl) + zeclip * cos(oblecl)
    return (xequat, yequat, zequat)

def rect_equat2rect_ecl(xequat, yequat, zequat, year, month, day, hour = 0, minute = 0, second = 0):
    oblecl = obl_ecl_JPL(year, month, day, hour, minute, second)
    xeclip = xequat
    yeclip = yequat * cos(- oblecl) - zequat * sin(- oblecl)
    zeclip = yequat * sin(- oblecl) + zequat * cos(- oblecl)
    return (xeclip, yeclip, zeclip)

