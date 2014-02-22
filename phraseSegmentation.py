__author__ = 'arenduchintala'
"""
This code takes a string as input linear chain fst
then returns a fst which contains all possible segmentations of that string
"""
import fst


def make_linear_chain(txt, phrases, sym):
    lc = fst.LogTransducer(sym, sym)
    pass


def make_segmenter(phrases, sym_f):
    segmenter = fst.LogTransducer(sym_f, sym_f)
    segmenter[0].final = True
    s = 0
    e = 1
    for fp, ep, lp in phrases:
        fc = '_'.join(fp)
        for idx, fw in enumerate(fp):
            if idx == 0:
                segmenter.add_arc(0, e, fw, fst.EPSILON, 0.0)
            else:
                segmenter.add_arc(s, e, fw, fst.EPSILON, 0.0)
            s = e
            e += 1
        segmenter.add_arc(s, 0, fst.EPSILON, fc, 0.0)

    return segmenter


sym_f = fst.SymbolTable()
sym_e = fst.SymbolTable()
for l in open('data/syme.sym', 'r').readlines():
    sym_e[l.split()[0]]
for l in open('data/symf.sym', 'r').readlines():
    sym_f[l.split()[0]]

phrases = [(tuple(l.split('|||')[0].split()), tuple(l.split('|||')[1].split()), float(l.split('|||')[2])) for l in
           open('data/tm-tiny', 'r').readlines()]

seg = make_segmenter(phrases, sym_f)
seg.write('seg.fst', sym_f, sym_f)
