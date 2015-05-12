import cPickle
import numpy as np
from itertools import islice
from fastnumbers import fast_int, fast_float
import struct
import cProfile, pstats 

limits = cPickle.load(open('VSOP2013_ranges.pickle','rb'))

fmt = struct.Struct("""6s 3s 3s 3s 3s x 3s 3s 3s 3s 3s x 4s 4s 4s 4s x
                       6s x 3s 3s 3s 20s x 3s 20s x 3s x""")

def convert(i):
    
    a = fmt.unpack(i)
    return [fast_float(a[j]) for j in xrange(1,22)]

def slice_file(planet, var, power, precision):
    
    file_in = open("VSOP2013p{}.dat".format(planet))
    start, end = limits[planet][var][power][precision]
    data = np.asarray([convert(i) for i in islice(file_in, start, end+1)], np.longdouble)
    file_in.close()
    coeffs = data[:,:17]
    S = 10**data[:,18:19]*data[:,17:18]
    C = 10**data[:,20:21]*data[:,19:20]
    return (coeffs, S, C)
                 

if __name__ == '__main__':
    profile = cProfile.run("slice_file(1,1,0,12)","prof.prof")
    p = pstats.Stats("prof.prof")
    p.sort_stats("cumulative").print_stats(10)


