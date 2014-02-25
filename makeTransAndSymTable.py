__author__ = 'arenduchintala'

import fst

'''
def make_functional_translation(phrases, sym_f, sym_e):
    full = fst.LogTransducer(sym_f, sym_e)
    full[0].final = True
    cumilative = 1
    functional_phrases = {}
    for fp, ep, lp in phrases:
        functional_phrases[ep] = functional_phrases.get(ep, [])
        functional_phrases[ep].append((fp, lp))

    for ep, fp_list in functional_phrases.iteritems():

        ep = list(ep)
        """
        The section below should provide a functional fst
        """
        f_end = None
        for fp_idx, (fp, lp) in enumerate(fp_list):
            #print ep, fp
            for idx, fw in enumerate(fp):
                if len(fp) == 1:
                    if f_end is None:
                        full.add_arc(0, cumilative, fw, fst.EPSILON, lp)
                        #print 'case 4f', 0, 'to', cumilative, 'saving', cumilative
                        f_end = cumilative  #  keep track of end state to merge all fp's into
                    else:
                        full.add_arc(0, f_end, fw, fst.EPSILON, lp)
                        #print 'case 4f', 0, 'to', f_end
                    if fp_idx < len(fp_list) - 1:
                        cumilative += 1  # get ready for the next fp form 0
                elif idx == 0:
                    full.add_arc(0, cumilative, fw, fst.EPSILON, 0.0)
                    #print 'case 1f', 0, 'to', cumilative
                elif idx == len(fp) - 1:
                    if f_end is None:
                        full.add_arc(cumilative, cumilative + 1, fw, fst.EPSILON, lp)
                        #print 'case 3f', cumilative, 'to', cumilative + 1, 'saving', cumilative + 1
                        cumilative += 1
                        f_end = cumilative  #  keep track of end state to merge all fp's into
                    else:
                        full.add_arc(cumilative, f_end, fw, fst.EPSILON, lp)
                        #print 'case 3f', cumilative, 'to', f_end
                    if fp_idx < len(fp_list) - 1:
                        cumilative += 1  # get ready for the next fp form 0
                else:
                    full.add_arc(cumilative, cumilative + 1, fw, fst.EPSILON, 0.0)
                    #print 'case 2f', cumilative, 'to', cumilative + 1
                    cumilative += 1
        cumilative += 1
        for idx, ew in enumerate(ep):
            if len(ep) == 1:
                #print ew, sym_e[ew]
                full.add_arc(f_end, 0, fst.EPSILON, ew, 0.0)
                #print 'case 4e', f_end, 'to', 0
                cumilative -= 1
            elif idx == 0:
                full.add_arc(f_end, cumilative, fst.EPSILON, ew, 0.0)
                #print 'case 1e', f_end, 'to', cumilative
            elif idx == len(ep) - 1:
                full.add_arc(cumilative, 0, fst.EPSILON, ew, 0.0)
                #print 'case 3e', cumilative, 'to', 0
            else:
                full.add_arc(cumilative, cumilative + 1, fst.EPSILON, fst.EPSILON, 0.0)
                #print 'case 2e', cumilative, 'to', cumilative + 1
                cumilative += 1
        cumilative += 1  # getting ready for next sentence pair

    return full


def make_translation(phrases, sym_f, sym_e):
    #The code below makes a non-functional FST (look up def:Functional)
    #http://openfst.cs.nyu.edu/twiki/bin/view/FST/FstGlossary#FunctionalDef
    full = fst.LogTransducer(sym_f, sym_e)
    full[0].final = True
    cumilative = 1

    for fp, ep, lp in phrases:
        fp = list(fp)
        ep = list(ep)
        #print fp, ep
        f_pad = fp + ([fst.EPSILON] * len(ep))
        e_pad = ([fst.EPSILON] * len(fp)) + ep
        for idx, (fw, ew) in enumerate(zip(f_pad, e_pad)):
            #print idx, len(f_pad)
            if idx == 0:
                full.add_arc(0, cumilative, fw, ew, 0.0)
                #print 'case 1 arc from', 0, 'arc to', cumilative, 'cumilative', cumilative

            elif idx == len(f_pad) - 1:
                full.add_arc(cumilative, 0, fw, ew, lp)
                #print 'case 2 arc from', cumilative, 'arc to', 0, 'cumilative', cumilative
            else:
                full.add_arc(cumilative, cumilative + 1, fw, ew, 0.0)
                #print 'case 3 arc from', cumilative, 'arc to', cumilative + 1, 'cumilative', cumilative
                cumilative += 1
        cumilative += 1
    return full
'''


def make_translation_chunks(phrases, sym_f, sym_e):
    # assumes syms have chunked phrases already
    # make phrase map many to 1.
    functional_phrases = {}
    for fp, ep, lp in phrases:
        functional_phrases[ep] = functional_phrases.get(ep, [])
        functional_phrases[ep].append((fp, lp))
    full = fst.LogTransducer(sym_f, sym_e)
    full[0].final = True
    ist = 1
    for ep, f_list in functional_phrases.iteritems():
        ep = '_'.join(ep)
        print sym_e[ep], ep
        for fp, lp in f_list:
            fp = '_'.join(fp)
            print '\t', fp, sym_f[fp], lp
            full.add_arc(0, ist, fp, fst.EPSILON, lp)
        full.add_arc(ist, 0, fst.EPSILON, ep, 0.0)
        ist += 1
    return full


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

out = make_translation_chunks(phrases, sym_f, sym_e)
out.write('data/trans.fst', sym_f, sym_e)
print 'writing binary symbol table..'
sym_e.write('data/syme.bin')
sym_f.write('data/symf.bin')
