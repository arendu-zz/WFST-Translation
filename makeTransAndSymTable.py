__author__ = 'arenduchintala'

import fst


def make_translation_chunks(phrases, sym_f, sym_e):
    # assumes syms have chunked phrases already
    # make phrase map many to 1.
    functional_phrases = {}
    for fp, ep, lp in phrases:
        functional_phrases[fp] = functional_phrases.get(fp, [])
        functional_phrases[fp].append((ep, -lp))  # convert the negative weights to positive, large weight = less prob

    full = fst.Transducer(sym_f, sym_e)
    full[0].final = True
    ist = 1
    for fp, e_list in functional_phrases.iteritems():
        fp = '_'.join(fp)
        full.add_arc(0, ist, fp, fst.EPSILON, 0.0)
        for ep, lp in e_list:
            ep = '_'.join(ep)
            print '\t', ep, sym_f[fp], lp
            full.add_arc(ist, 0, fst.EPSILON, ep, lp)
        #full.add_arc(ist, 0, fst.EPSILON, ep, 0.0)
        ist += 1
    return full


def ends(txt, sym_f, sym_e):
    txt = txt.split()
    lc = fst.Transducer(sym_f, sym_e)
    for idx, t in enumerate(txt):
        lc.add_arc(idx, idx + 1, t, t, 0.0)
    lc[idx + 1].final = True
    return lc


if __name__ == '__main__':

    sym_f = fst.SymbolTable()
    sym_e = fst.SymbolTable()
    for l in open('data/syme.sym', 'r').readlines():
        sym_e[l.split()[0]]
    for l in open('data/symf.sym', 'r').readlines():
        sym_f[l.split()[0]]
        for lw in l.split()[0].split('_'):
            sym_f[lw]

    phrases = [(tuple(l.split('|||')[0].split()), tuple(l.split('|||')[1].split()), float(l.split('|||')[2])) for l in
               open('data/tm', 'r').readlines()]
    [phr_f, phr_e, wt] = zip(*phrases)
    phr_f = set(phr_f)
    potentially_unk = [(tuple([t]), tuple(['<unk>']), 0.0) for t in open('data/input', 'r').read().split() if (t,) not in phr_f]
    phrases = phrases + potentially_unk
    out = make_translation_chunks(phrases, sym_f, sym_e)
    out.write('data/trans.fst', sym_f, sym_e)
    print 'writing binary symbol table..'
    sym_e.write('data/syme.bin')
    sym_f.write('data/symf.bin')
    print 'writing concat fsts...'
    s = ends('<s>', sym_f, sym_e)
    s.write('data/s.fst', sym_f, sym_e)
    s = ends('</s>', sym_f, sym_e)
    s.write('data/ss.fst', sym_f, sym_e)

