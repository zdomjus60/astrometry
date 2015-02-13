# -*- coding: utf-8 -*-
""" helper functions for time management
"""
import math

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
    if (year*10000 + month*100 + day) > 15821015:
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

def jul_millennia(year, month, day, hour=0, minute=0, second=0):
    d1 = cal2jul(2000,1,1,12,0,0)
    d2 = cal2jul(year, month, day, hour, minute, second)
    return (d2-d1)/365250

if __name__ == '__main__':
    dash_line = 80 * '-'
    print dash_line
    ddd = dms2ddd(15,24,35)
    print '''from sexagesimal to decimal of 15h 24' 35": ''', ddd
    dms = ddd2dms(ddd)
    print 'and inverse function: ', dms
    print dash_line
    jd = cal2jul(2009,6,19,18,3,21)
    print 'julian date from calendar date 2009/06/19 18:03:21', jd
    cal = jul2cal(jd)
    print 'inverse: calendar date from julian date ', jd, ' :',cal
    print dash_line
    epoch = cal2jul(1999,12,31)
    date_ = cal2jul(1990, 4,19)
    print 'days from 1999/12/31', date_ - epoch
    print dash_line
    doth = day_of_the_week(2009, 6, 19)
    print 'day of the week for 2009/6/19 :',doth
    doth = day_of_the_week(2015, 1, 25)
    print 'day of the week for 2015/1/25 :',doth
    ddd = dms2ddd(19,20,37)
    print dash_line
    print """conversion 19h 20' 37": """, ddd
    print "inverse conversion :", ddd2dms(ddd)
    print dash_line 
    ut = lt2ut(2013,7,1, 3, 37,0, 4, 1)
    print "greenwich calendar date for 2013/7/1 3h37 timezone +4 Daylight Savings)", ut
    lt = ut2lt(ut[0], ut[1], ut[2], ut[3], ut[4], ut[5], 4, 1)
    print "inverse of the previous calculus", lt 
    print dash_line
    print """from Universal Time to Greenwich Sidereal Time for 1980/4/22 14h36'52" """, ut2gst(1980,4,22, 14,36,52)
    print """from Greenwich Sidereal Time to Universal Time for 1980/4/22 4h40'06"  """, gst2ut(1980,4,22, 4,40,06)
    print dash_line
    print """ from GST 4h40'06" to LST for 64°W """, gst2lst(4,40,6,-64,0,0)
    print """ inverse of the previous formula   """, lst2gst(0,24,6,64,0,0)
    
