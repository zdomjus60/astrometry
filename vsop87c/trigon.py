import math

def sin(x):
        return math.sin(math.radians(x))

def cos(x):
	return math.cos(math.radians(x))

def tan(x):
        return math.tan(math.radians(x))

def atan2(y , x):
	return math.degrees(math.atan2(y, x))

def reduce360(x):
	return x % 360.0

