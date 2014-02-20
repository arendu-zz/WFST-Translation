__author__ = 'arenduchintala'

if __name__ == '__main__':
    lm = open('data/lm', 'r').readlines()
    tm = open('data/tm', 'r').readlines()
    sym_e = set([])
    sym_f = set([])
    for l in lm:
        ls = l.split('\t')
        if len(ls) == 2 or len(ls) == 3:
            sym_e.update(ls[1].split())

    for t in tm:
        try:
            [f, e, n] = t.split('|||')
            sym_f.update(tuple(f.split()))
            sym_e.update(tuple(e.split()))
        except:
            print 'error in line', t

    sym_w = open('data/syme.sym', 'w')
    sym_o = [str(sym.strip() + ' ' + str(id + 1)).strip() for id, sym in enumerate(sym_e)]
    sym_o.insert(0, '<eps> 0')
    sym_w.write('\n'.join(sym_o))
    sym_w.flush()
    sym_w.close()

    sym_w = open('data/symf.sym', 'w')
    sym_o = [str(sym.strip() + ' ' + str(id + 1)).strip() for id, sym in enumerate(sym_f)]
    sym_o.insert(0, '<eps> 0')
    sym_w.write('\n'.join(sym_o))
    sym_w.flush()
    sym_w.close()

