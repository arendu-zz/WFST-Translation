__author__ = 'arenduchintala'
import operator, fst, sys, pdb


def bestpathstr(f):
    fbest = f.shortest_path(1)
    for i, path in enumerate(fbest.paths()):
        path_istring = ' '.join(f.isyms.find(arc.ilabel) for arc in path if f.isyms.find(arc.ilabel) != fst.EPSILON)
        path_ostring = ' '.join(f.osyms.find(arc.olabel) for arc in path if f.osyms.find(arc.olabel) != fst.EPSILON)
        path_weight = reduce(operator.mul, (arc.weight for arc in path))
        path_istring = path_istring.encode(encoding='UTF-8', errors='strict')
        path_ostring = path_ostring.encode(encoding='UTF-8', errors='strict')
        path_ostring = path_ostring.replace('<s>', '')
        path_ostring = path_ostring.replace('</s>', '')
        path_ostring = path_ostring.strip()
        return path_ostring
        #paths[float(path_weight)] = paths.get(float(path_weight), []) + [path_ostring + ' <cost=' + str(float(path_weight)) + '>']
        #return paths
        #print('{} | {} / {}'.format(path_istring, path_ostring, path_weight))


if __name__ == '__main__':
    folder = sys.argv[1]
    if folder[-1] != '/':
        folder += '/'
    for idx, s, in enumerate(open('data/input', 'r').readlines()):
        fname = 'lc' + str(idx) + '.final.fst'
        f = fst.read(folder + fname)
        print bestpathstr(f)
