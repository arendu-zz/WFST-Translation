__author__ = 'arenduchintala'
import fst, itertools, pdb

if __name__ == '__main__':
    tokens = open('data/input', 'r').read().split()
    tokens = set(tokens)
    symf = fst.read_symbols('data/symf.bin')
    reorder_list = []
    reorder = fst.Transducer(symf, symf)
    reorder[0].final = True
    for s, v in symf.items():
        reorder.add_arc(0, 0, s, s, 0.0)
        st = set(s.split('_'))
        if len(st.intersection(tokens)) > 0:
            print 'keep', s
            reorder_list.append(s)
        else:
            print 'reject', s
    print 'filtered down to', len(set(reorder_list))
    pdb.set_trace()
    n = 1
    c = 0
    for a, b in itertools.product(reorder_list, reorder_list):
        c += 1
        if c % 1000 == 0:
            print int(c / 1000), 'of', int((len(reorder_list) ** 2) / 1000)
        if a != b:
            reorder.add_arc(0, n, a, fst.EPSILON, 0.0)
            #print 0, n
            reorder.add_arc(n, n + 1, b, fst.EPSILON, 0.0)
            #print n + 1, n + 2
            reorder.add_arc(n + 1, n + 2, fst.EPSILON, b, 0.0)
            #print n + 2, 0
            reorder.add_arc(n + 2, 0, fst.EPSILON, a, 0.0)
            n += 3
    reorder.write('data/reorder.fst', symf, symf)


