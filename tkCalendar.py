#/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *


class tkCalendar:
    import datetime

    def __init__(self, master):
        "this section initializes the graphic objects"
        # main window
        self.Calendar = master
        # top frame (date)
        self.date_labels = Frame(self.Calendar)
        self.date_labels.pack(fill = BOTH, expand = 1)
        for i in ('Year', 'Month', 'Hour', 'Minute'):
            label = Label(self.date_labels, text=i, bg = 'tomato')
            label.pack(side = LEFT, fill = X, expand = 1) 
        
        self.dtime = self.datetime.datetime.now()
        self.date = Frame(self.Calendar)
        self.date.pack(side = 'top', fill = X, expand = 1)
        
        # spinbox for year
        self.spin_year = Spinbox(self.date, from_ = -3000, to = 3000, width = 3)
        self.spin_year.pack(side = 'left', fill = X, expand = 1)
        self.spin_year.config(state = 'readonly')
        # spinbox for month
        self.spin_month = Spinbox(self.date,
                                  from_ = 1, to = 12, 
                                  width = 3)
        self.spin_month.pack(side = 'left', fill = X, expand = 1)
        self.spin_month.config(state = 'readonly')# spinbox for hour
        self.spin_hour = Spinbox(self.date,
                                 from_ = 0, to = 23,
                                 width = 3)
        self.spin_hour.pack(side = LEFT, fill = X, expand = 1)
        self.spin_hour.config(state = 'readonly')
        # spinbox for minute
        self.spin_minute = Spinbox(self.date,
                                 from_ = 0, to = 59,
                                 width = 3)
        self.spin_minute.pack(side = LEFT, fill = X, expand = 1)
        self.spin_minute.config(state = 'readonly')
        # frame for days of the week labels
        self.dotw_labels= Frame(self.Calendar)
        self.dotw_labels.pack(fill = BOTH, expand = 1)
        for i in ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'):
            label = Label(self.dotw_labels, text=i, bg = 'light green',
                          relief = GROOVE)
            label.pack(side = LEFT, fill = BOTH, expand = 1) 
        # table (list of buttons) for days
        self.table = []
        for row in range(0,6):
            # here 6 horizontal frames are created
            # each one receives a block of 7 buttons
            self.row = Frame(self.Calendar)
            self.row.pack(side = TOP, fill = BOTH, expand = 1)
            for col in range(0,7):
                button = Button(self.row,
                                width = 2,
                                bg = 'grey',
                                text = ''
                                )
                # just a little trick: because of lambda usage the callback function
                # receives an updated parameter, referred to the specific button
                # widget, not the one available during
                # initialization
                button.config(command = lambda button = button: self.change_day(button))
                button.pack(side = LEFT, fill = BOTH, expand = 1)
                self.table.append(button)
        self.time_lbl = Label(self.Calendar, text='')
        self.time_lbl.pack()

        # some Variable Classes, when updated a callback function is activated
        self.year = IntVar(self.Calendar)
        self.year.set(self.dtime.year)
        self.year.trace('w', self.check_and_reconfigure)
        self.month = IntVar(self.Calendar)
        self.month.set(self.dtime.month)
        self.month.trace('w', self.check_and_reconfigure)
        self.day = IntVar(self.Calendar)
        self.day.set(self.dtime.day)
        self.day.trace('w', self.check_and_reconfigure)
        self.hour = IntVar(self.Calendar)
        self.hour.set(self.dtime.hour)
        self.hour.trace('w', self.check_and_reconfigure)
        self.minute = IntVar(self.Calendar)
        self.minute.set(self.dtime.minute)
        self.minute.trace('w', self.check_and_reconfigure)
        # bottom Frame and call to functions
        self.month_length = 0
        self.spin_year.config(textvariable = self.year)
        self.spin_month.config(textvariable = self.month)
        self.spin_hour.config(textvariable = self.hour, justify = RIGHT)
        self.spin_minute.config(textvariable = self.minute, justify = RIGHT)
        self.jd = self.cal2jul(self.year.get(),
                                                 self.month.get(),
                                                 self.day.get(),
                                                 self.hour.get(),
                                                 self.minute.get())
        self.time_lbl.config(text = "{0}:{1}     JD {2}".format(
                                    str(self.hour.get()).zfill(2),
                                    str(self.minute.get()).zfill(2),
                                    self.jd))                   
        self.check_and_reconfigure()

    def check_and_reconfigure(self, *args):
        year = self.year.get()
        month = self.month.get()
        day = self.day.get()
        hour = self.hour.get()
        minute = self.minute.get()
        self.act_time=""
        # recalculate month's length in days
        if month in (1,3,5,7,8,10,12):
            self.max_days = 31
        elif month in (4,6,9,11):
            self.max_days = 30
        elif month == 2:
            if year < 1582:
                if year%4 == 0:
                    self.max_days = 29
                else:
                    max_day = 28
            else:
                if (year%4 == 0) and (year%400 == 0):
                    self.max_days = 29
                else:
                    self.max_days = 28
        self.month_length = self.max_days
        # fill days' buttons
        for i in self.table:
            i.config(text = '')
            i.config(bg   = 'grey')
            i.config(state = DISABLED)
        for day in range (1, self.month_length+1):
            dotw = self.day_of_the_week(self.year.get(), self.month.get(), day)
            posx = dotw
            if day == 1:
                lag = posx
            posy = int((day+lag-1)/7)
            self.table[posx + posy * 7].config(text = str(day))
            self.table[posx + posy * 7].config(state = NORMAL)
            if day == self.day.get():
                self.table[posx + posy * 7].config(bg='white')
                self.act_time = "{0}:{1}     JD {2}".format(
                        str(self.hour.get()).zfill(2), str(self.minute.get()).zfill(2),
                        self.cal2jul(self.year.get(), self.month.get(), self.day.get(),
                        self.hour.get(), self.minute.get()))
        self.time_lbl['text']=self.act_time
        
    def change_day(self, button):
        self.day.set(button.cget('text'))
        
        
    def cal2jul(self, year, month, day,
                hour=0, minute =0):
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
        return b + c + d + day + hour / 24.0 + minute / 1440.0 + 1720994.5

   
    def day_of_the_week(self, year, month, day):
                
        jd = self.cal2jul(year, month, day)
        a = (jd+1.5)/7
        f = int((a % 1)*7 +.5)
        return f        


       
if __name__ == '__main__':

    root = Tk()
    cal  = tkCalendar(root)

    root.mainloop()
