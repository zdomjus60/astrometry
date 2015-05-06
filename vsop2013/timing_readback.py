import cPickle
from itertools import islice
import cProfile, pstats, timeit

limits = cPickle.load(open('VSOP2013_ranges.pickle','rb'))

def timing01():
    chunk = []
    file_in = open('VSOP2013p1.dat')
    all_lines = file_in.readlines()
    start, end = limits[1][1][0][20]
    chunk = all_lines[start:end+1]
    file_in.close()
    return chunk
    
def timing02():
    chunk=[]
    file_in = open('VSOP2013p1.dat')
    start, end = limits[1][1][0][20]
    chunk = [line for line in islice(file_in, start, end+1)]
    file_in.close()    
    return chunk
    
def timing03():
    chunk = []
    file_in = open('VSOP2013p1.dat')
    start, end = limits[1][1][0][20]
    chunk = list(islice(file_in, start, end+1))
    file_in.close()
    return chunk
        
def main():
    result1 = timing01()
    result2 = timing02()
    result3 = timing03()
    return (result1, result2, result3)

if __name__ == '__main__':
    
    profile = cProfile.run("main()","prof.prof")
    p = pstats.Stats("prof.prof")
    p.sort_stats("cumulative").print_stats(15)

    result = main()
    print "timing 100 repliche timing01():", timeit.timeit("timing01()", setup = "from __main__ import timing01", number=100)
    print "timing 100 repliche timing02():", timeit.timeit("timing02()", setup = "from __main__ import timing02", number=100)
    print "timing 100 repliche timing03():", timeit.timeit("timing03()", setup = "from __main__ import timing03", number=100)
    print "-" * 80
    print "primo elemento della lista 1:", result[0][0]
    print "primo elemento della lista 2:", result[1][0]
    print "primo elemento della lista 3:", result[2][0]
    
    print "ultimo elemento della lista 1:", result[0][-1]
    print "ultimo elemento della lista 2:", result[1][-1]
    print "ultimo elemento della lista 3:", result[2][-1]
    
