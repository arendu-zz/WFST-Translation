__author__ = 'arenduchintala'
"""
This code takes a string as input linear chain fst
then returns a fst which contains all possible segmentations of that string
"""
import fst

def log_linear_chain(txt, sym_f):
    txt = txt.split()
    lc = fst.LogTransducer(sym_f, sym_f)
    for idx, t in enumerate(txt):
        lc.add_arc(idx, idx + 1, t, t, 0.0)
    lc[idx + 1].final = True
    return lc


def make_segmenter(phrases, sym_f):
    individual_tokens = set([])
    segmenter = fst.LogTransducer(sym_f, sym_f)
    segmenter[0].final = True
    s = 0
    e = 1
    for fp in phrases:
        if len(fp) > 1:
            fc = '_'.join(fp)
            for idx, fw in enumerate(fp):
                individual_tokens.add(fw)
                if idx == 0:
                    segmenter.add_arc(0, e, fw, fst.EPSILON, 0.0)
                else:
                    segmenter.add_arc(s, e, fw, fst.EPSILON, 0.0)
                s = e
                e += 1
            segmenter.add_arc(s, 0, fst.EPSILON, fc, -1.0)
        else:
            fw = fp[0]
            individual_tokens.add(fw)
    # adding individual tokens
    for idt in individual_tokens:
        # make self loops with single tokens
        segmenter.add_arc(0, 0, idt, idt, -1.0)
    return segmenter

sym_f = fst.read_symbols('data/symf.bin')
sym_e = fst.read_symbols('data/syme.bin')
'''
for l in open('data/syme.sym', 'r').readlines():
    sym_e[l.split()[0]]

for l in open('data/symf.sym', 'r').readlines():
    lp = l.split()[0]
    sym_f[lp]
    lws = lp.split('_')
    for lw in lws:
        sym_f[lw]
'''
phrases_f = [tuple(l.split('|||')[0].split()) for l in
             open('data/tm', 'r').readlines()]
phrases_f = set(phrases_f)
seg = make_segmenter(phrases_f, sym_f)
seg.write('data/seg.fst', sym_f, sym_f)
'''
#Enable this chuck to test the output when a linear chain is composed with the phrase segmenter
lc = log_linear_chain("que et je me", sym_f)
lc.write('data/lc.fst', sym_f, sym_f)
out = lc.compose(seg)
out.write('out.fst', sym_f, sym_f)
'''