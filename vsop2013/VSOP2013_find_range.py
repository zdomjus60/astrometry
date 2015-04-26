import gmpy2 as gmp
gmp.get_context().precision=200
from itertools import islice
import cPickle

def find_limits():
    # create an empty dictionary
    limits={}
    for planet in xrange(1,10):
        # read date files, one per planet
        file_in = open('VSOP2013p'+str(planet)+'.dat')
        # create a list with the header position and values for variables planet, var, power
        elenco = [(s[0], s[1].split()) for s in enumerate(file_in) if "VSOP" in s[1]]
        file_in.close()
        # extend the dictionary with a subdictionary for each planet 
        limits[planet]={}
        for var in xrange(1,7):
            # extend the dictionary with a subdictionary for each variable
            limits[planet][var] = {}
            for power in xrange(0,21):
                # extend the dictionary with a subdictionary for each power
                limits[planet][var][power] = {}
                for threshold in xrange(0,21):
                    # extend the dictionary with a two values tuple (min and max)
                    # for each sensibility threshold
                    # and for each item in list assign (0,0) to the tuple
                    limits[planet][var][power][threshold]=(0,0)
        # create a tuple with range limits for each planet, variable, power
        for i in xrange(len(elenco)):
            start = int(elenco[i][0])+1
            planet = int(elenco[i][1][1])
            var = int(elenco[i][1][2])
            power = int(elenco[i][1][3])
            end = int(elenco[i][1][4])+start
            # load a file chunk for each voice in list and find extreme value for each threshold
            file_in = open('VSOP2013p'+str(planet)+'.dat')
            segmento = islice(file_in, start, end)
            for j, k in enumerate(segmento):
                cursor = j
                line = k.split()
                Sb = float(line[-4])
                Se = int(line[-3])
                S = Sb * 10 ** Se
                Cb =float(line[-2])
                Ce = int(line[-1])
                C = Cb * 10 ** Ce
                ro = gmp.sqrt(S*S+C*C)
                threshold = -int(gmp.floor(gmp.log10(ro)))
                limits[planet][var][power][threshold]=(start, start+cursor)
            file_in.close()
    for planet in xrange(1,10):
        for var in xrange(1,7):
            for power in xrange(0,21):
                for threshold in xrange(1,21):
                    prec_ = limits[planet][var][power][threshold-1]
                    subs_ = limits[planet][var][power][threshold]
                    if subs_ == (0,0) and prec_ !=0:
                        limits[planet][var][power][threshold] = limits[planet][var][power][threshold-1]
    return limits


if __name__ == '__main__':
    limits = find_limits()
    cPickle.dump(limits, open('VSOP2013_ranges.pickle','wb'))
    # reload limits from disk
    load_limits = cPickle.load(open('VSOP2013_ranges.pickle','rb'))

