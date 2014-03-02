__author__ = 'arenduchintala'
import operator, fst, sys, pdb


def getpaths(f, n):
    paths = {}
    fbest = f.shortest_path(n)
    for i, path in enumerate(fbest.paths()):
        path_istring = ' '.join(f.isyms.find(arc.ilabel) for arc in path if f.isyms.find(arc.ilabel) != fst.EPSILON)
        path_ostring = ' '.join(f.osyms.find(arc.olabel) for arc in path if f.osyms.find(arc.olabel) != fst.EPSILON)
        path_weight = reduce(operator.mul, (arc.weight for arc in path))
        path_istring = path_istring.encode(encoding='UTF-8', errors='strict')
        path_ostring = path_ostring.encode(encoding='UTF-8', errors='strict')
        paths[float(path_weight)] = paths.get(float(path_weight), []) + [path_ostring + ' <cost=' + str(float(path_weight)) + '>']
    return paths
    #print('{} | {} / {}'.format(path_istring, path_ostring, path_weight))


if __name__ == '__main__':
    #symi = fst.read_symbols(sys.argv[2].strip())
    #symo = fst.read_symbols(sys.argv[3].strip())
    try:
        f = fst.read_std(sys.argv[1].strip())
        n = int(sys.argv[2].strip())
    except:
        print 'useage: python outputPaths.py [in.fst] [n]\n'
        exit()
    f.remove_epsilon()
    paths = getpaths(f, n)
    for p in sorted(paths):
        print '\n'.join(paths[p])
