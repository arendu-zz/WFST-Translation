__author__ = 'arenduchintala'
import operator, fst, sys, pdb


def uni(s):
    return s.encode(encoding='UTF-8', errors='strict')


def getpaths(f, unk, n=1):
    paths = {}
    fbest = f.shortest_path(n)
    for i, path in enumerate(fbest.paths()):  # refactor out the loop
        path_istring = [uni(f.isyms.find(arc.ilabel)) for arc in path if f.isyms.find(arc.ilabel) != fst.EPSILON]
        path_ostring = [uni(f.osyms.find(arc.olabel)) for arc in path if f.osyms.find(arc.olabel) != fst.EPSILON]

        strings = []

        arcs = zip(path_istring, path_ostring)
        for (ia, oa) in arcs:
            if oa == "<s>" or oa == "</s>":
                pass
            elif not oa == "<unk>":
                strings.append(oa)
            else:
                #there is a unk in thr output
                #hack look for one of the 7 unks possible from the input and insert them
                t = list(set(path_istring).intersection(unk))
                strings.append(t[0])
        return ' '.join(strings)


if __name__ == '__main__':
    #symi = fst.read_symbols(sys.argv[2].strip())
    #symo = fst.read_symbols(sys.argv[3].strip())
    try:
        f = fst.read_std(sys.argv[1].strip())
        unk = set(open('data/unk').read().split())
    except:
        print 'useage: python outputPaths.py [in.fst]\n'  # takes 1-best
        exit()
    f.remove_epsilon()
    paths = getpaths(f, unk)
    print paths
