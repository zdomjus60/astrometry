from Tkinter import *
import tkFont
import ttk
import sqlite3
import os

class Cities:
    """
    This class is a new widget, aimed to deal with world cities from geoname site
    (see http://download.geonames.org/export/dump/) for details.
    A lot of useful informations are taken from a main archive (allCountries.txt)
    and linked to textual geographical informations from the same site
    (admin1CodesASCII.txt and admin2Codes.txt), then reversed in a sqlite3 db,
    which is read from inside the present program
    """

    def __init__(self, master):
        """
        All the widgets are created in __init__, all significant variables
        are instance variables and can be read from outside
        """
        self.master = master
        root_dir = os.path.dirname(os.getcwd())
        for root, dirs, files in os.walk(root_dir, topdown=True):
            for file in files:
                if file.endswith('localita.db'):
                    self.db = os.path.join(root, file)

        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        self.frame1 = Frame(self.master, background='#006f6f', padx=5, pady=5)
        self.frame1.pack(fill=X, expand=1)
        self.label1 = Label(self.frame1, text='Location')
        self.label1.pack(side=LEFT, anchor='w', fill=X, expand=1)
        self.search = StringVar(self.master)
        self.search.set('')
        self.result = ''
        self.entry1 = Entry(self.frame1, textvariable=self.search)
        self.entry1.pack(side=LEFT, fill=X, expand=1)
        self.button1 = Button(self.frame1, text='<-- Substr. Search', command=self.select)
        self.button1.pack(side=LEFT, fill=X, expand=1)
        self.frame2 = Frame(self.master)
        self.frame2.pack()
        self.combo1 = ttk.Combobox(self.frame2, text=self.result, width=60)
        self.combo1.pack(anchor='w')
        self.combo1.bind('<<ComboboxSelected>>', self.update_label)
        self.label2 = Label(self.frame2, text='\n\n\n\n\n\n\n\n\n', justify=LEFT, anchor='w', width=60, relief=GROOVE, background='orange')
        self.label2.pack(side=LEFT)

    def select(self, *args):
        """
        This is the search engine in the database. As a result, the combobox
        and the bottom label texts are updated
        """
        search = self.search.get()
        p_query = ('%' + search + '%',)
        query = 'select nome_ascii, latitudine, longitudine, admin1, country, ascad1, ascad2, popolazione, elevazione, timezone                 from localita where nome_ascii like ? order by nome_ascii'
        self.c.execute(query, p_query)
        self.cities_list = self.c.fetchall()
        self.combo1.config(values='')
        values = [ [x[0],
         x[4],
         x[5],
         x[6]] for x in self.cities_list ]
        for i in range(len(values)):
            for j in range(4):
                values[i][j] = str(values[i][j])

            values[i] = tuple(values[i])

        self.combo1['values'] = tuple(values)
        self.combo1.set(values[0][0] + ' ' + values[0][1] + ' ' + values[0][2])
        index = self.combo1.index(0)
        self.update_label(index)

    def update_label(self, *args):
        """
        This routine updates the index value to get back the selected row
        in the query results and subsequently updates the top down label
        """
        if args[0] == 0:
            index = 0
        else:
            index = self.combo1.current()
        _list = list(self.cities_list[index])
        s = [ '{}'.format(x) for x in _list ]
        long_list = 'Name: {0}\nLat: {1}\nLong: {2}\nState: {3} ({4})\n'
        long_list += 'Region: {5}\nProvince: {6}\nPopulation: {7}\n'
        long_list += 'Elevation: {8}\nTimezone: {9}'
        self.label2['text'] = long_list.format(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9])
        self.parameters = self.cities_list[index]


if __name__ == '__main__':
    root = Tk()
    app = Cities(root)
    root.mainloop()
