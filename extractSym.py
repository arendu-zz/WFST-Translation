__author__ = 'arenduchintala'

if __name__ == '__main__':
    lm = open('data/lm', 'r').readlines()
    tm = open('data/tm', 'r').readlines()
    input = open('data/input', 'r').read().split()
    input = set(input)
    sym_e = set(['<s>', '</s>', '<unk>'])
    sym_f = set(['<s>', '</s>', '<unk>'])
    sym_f.update(input)
    for l in lm:
        ls = l.split('\t')
        if len(ls) == 2 or len(ls) == 3:
            sym_e.update(ls[1].split())

    for t in tm:
        try:
            [f, e, n] = t.split('|||')
            fs = f.split()
            fp = '_'.join(fs)
            sym_f.update(tuple(fs))
            sym_f.add(fp)
            es = e.split()
            ep = '_'.join(es)
            sym_e.update(tuple(es))
            sym_e.add(ep)
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
