# -*- coding: utf-8 -*-
# calculate Sun longitude according to Paul Schlyter formulas
from planets import Planet
sun = Planet('Sun', 1990, 4, 19)
print sun.position()
