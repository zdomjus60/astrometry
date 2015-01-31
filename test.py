# -*- coding: utf-8 -*-
# calculate Sun longitude according to Paul Schlyter formulas
from trigon import *
from planets import Planet
year, month, day = (1990, 4, 19)
for planets in ('Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
               'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto'):
    
    planet = Planet(planets, year, month, day).position()
    print planets, planet
