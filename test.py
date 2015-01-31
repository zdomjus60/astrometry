# -*- coding: utf-8 -*-
# calculate Sun longitude according to Paul Schlyter formulas
from trigon import *
from planets import Planet
year, month, day = (1990, 4, 19)
for body in ('Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
               'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto'):
    
    planet = Planet(body, year, month, day).position()
    print body, planet
