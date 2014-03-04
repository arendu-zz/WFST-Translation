__author__ = 'arenduchintala'

import fst


def split_l(l):
    try:
        [ps, ng, bk] = l
        return -float(ps), ng, -float(bk)
    except:
        [ps, ng] = l
        return -float(ps), ng.strip(), None


if __name__ == '__main__':
    sym_f = fst.read_symbols('data/symf.bin')
    sym_e = fst.read_symbols('data/syme.bin')
    lm_lines = open('data/lmc', 'r').readlines()
    lm_ps = {}
    lm_ng = {}
    lm_bk = {}

    lm_fst = fst.Transducer(sym_e, sym_e)
    _init_id = 0
    lm_fst.add_state()
    _null_id = 1
    lm_fst.add_state()
    _final_id = 2
    lm_fst[2].final = True
    node_id = 3
    for l in lm_lines:
        l = l.strip()
        ls = l.split('\t')
        if l.strip() != '' and len(ls) > 1:
            ng = ""
            [ps, ng, bk] = split_l(ls)
            print ps, ng, bk
            lm_ng[ng] = node_id
            ngs = ng.split()
            if len(ngs) == 1:
                #unigram
                if ngs[0] == '<s>':
                    lm_fst.add_arc(_init_id, node_id, ngs[0], ngs[0], ps)
                elif ngs[0] == '</s>':
                    node_id -= 1  #lm_fst.add_arc(node_id, _final_id, ngs[0], ngs[0], ps)
                else:
                    lm_fst.add_arc(_null_id, node_id, ngs[0], ngs[0], ps)
            elif len(ngs) == 2:
                #bigram
                [ng1, ng2] = ngs
                lm_fst.add_arc(lm_ng[ng1], node_id, ng2, ng2, ps)
                if ng2 == '</s>':
                    lm_fst.add_arc(node_id, _final_id, fst.EPSILON, fst.EPSILON, 0.0)
            elif len(ngs) == 3:
                [ng1, ng2, ng3] = ngs
                ng12 = ng1 + ' ' + ng2
                lm_fst.add_arc(lm_ng[ng12], node_id, ng3, ng3, ps)
                if ng3 == '</s>':
                    lm_fst.add_arc(node_id, _final_id, fst.EPSILON, fst.EPSILON, 0.0)
            if bk is None:
                lm_fst.add_arc(node_id, _null_id, fst.EPSILON, fst.EPSILON, 0.0)
            else:
                lm_fst.add_arc(node_id, _null_id, fst.EPSILON, fst.EPSILON, bk)
            node_id += 1
    lm_fst.arc_sort_input()
    lm_fst.write('data/lmc.fst', sym_e, sym_e)



