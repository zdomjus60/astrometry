def cal2jul(year, month, day, hour=0, minute =0, second=0):
    month2 = month
    year2 = year
    if month2 <= 2:
        year2 -= 1
        month2 += 12
    else:
        pass
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

def julian_centuries(year, month, day, hour=0, minute =0, second=0):
    return (cal2jul(year, month, day, hour, minute, second)-cal2jul(2000,1,1,12))/36525.0

def julian_millennia(year, month, day, hour=0, minute =0, second=0):
    return julian_centuries(year, month, day, hour, minute, second) / 10.0

def julian_decamillennia(year, month, day, hour=0, minute =0, second=0):
    return julian_centuries(year, month, day, hour, minute, second) / 100.0

def obl_ecl_JPL(year, month, day, hour=0, minute = 0, second = 0):

    t = julian_centuries(year, month, day, hour, minute, second)
    
    """ from JPL Astronomical Almanac 2010 """
    return (23 * 3600 + 26*60 + 21.406
                - 46.836769 * t
                - 0.0001831 * t *t
                + 0.00200340 * t* t* t
                - 0.576e-6 * t* t* t* t
                - 4.34e-8 * t* t* t* t* t)/3600.0


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

"""


def obl_ecl_Laskar(year, month, day, hour = 0, minute = 0, second = 0):
    """
    // -----------------------------------------------------------
    // Compute the (t) value in Julian decamillennia corresponding
    // to the JD argument and reckoned from J2000.
       $t = ($JD - 2451545.0) / 3652500.0;

    // --------------------------------------
    // Compute mean obliquity in arc seconds.
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

if __name__ == '__main__':
    print obl_ecl_Laskar(2015,2,13)
    
    
    
