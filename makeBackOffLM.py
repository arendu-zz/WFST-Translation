__author__ = 'arenduchintala'
import fst, re, pprint

INITIAL = '_initial_'
NULL = '_null_'


def trysplit(gramline):
    try:
        [p, ng, b] = gramline.split('\t')
        return -float(p), ng, -float(b)
    except:
        [p, ng] = gramline.split('\t')
        return -float(p), ng, None


def add_arc_pr(lmfst, fid, tid, isy, osy, wt):
    lmfst.add_arc(fid, tid, isy, osy, wt)
    print 'added arc', fid, tid


if __name__ == '__main__':
    sym_e = fst.read_symbols('data/syme.bin')
    lm_txt = open('data/lm', 'r').read()
    [bs, unigrams, bigrams, trigrams] = re.split('1-grams:|2-grams:|3-grams:', lm_txt)
    unigrams = re.split('\n+', unigrams)
    bigrams = re.split('\n+', bigrams)
    trigrams = re.split('\n+', trigrams)

    lm_id = {}
    lm_id[INITIAL] = len(lm_id)
    lm_fst = fst.Transducer(sym_e, sym_e)
    lm_fst.add_state()
    lm_id[NULL] = len(lm_id)
    u = 2
    for uni_line in unigrams:
        if uni_line.strip() != '' and len(uni_line.split('\t')) > 1:
            [p, ng, bk] = trysplit(uni_line)
            lm_id[ng] = lm_id.get(ng, len(lm_id))
            add_arc_pr(lm_fst,lm_id[NULL], u, ng, ng, p)

            if bk is not None:
                add_arc_pr(lm_fst,u, lm_id[NULL], fst.EPSILON, fst.EPSILON, bk)
            if ng == '</s>':
                lm_fst[lm_id[ng]].final = True
            u += 1

    b = u
    for bi_line in bigrams:
        if bi_line.strip() != '' and len(bi_line.split('\t')) > 1:
            [p, ng, bk] = trysplit(bi_line)
            [ng1, ng2] = ng.split()
            lm_id[ng1, ng2] = lm_id.get((ng1, ng2), len(lm_id))
            from_id = lm_id[ng1]
            to_id = lm_id[ng1, ng2]
            add_arc_pr(lm_fst,from_id, to_id, ng2, ng2, p)
            if bk is not None:
                add_arc_pr(lm_fst,to_id, lm_id[ng2], fst.EPSILON, fst.EPSILON, bk)
            if ng2 == '</s>':
                lm_fst[lm_id[ng1, ng2]].final = True
            b += 1
    t = b
    for tri_line in trigrams:
        if tri_line.strip() != '' and len(tri_line.split('\t')) > 1:
            [p, ng, bk] = trysplit(tri_line)
            [ng1, ng2, ng3] = ng.split()
            lm_id[ng2, ng3] = lm_id.get((ng2, ng3), len(lm_id))
            from_id = lm_id[ng1, ng2]
            to_id = lm_id[ng2, ng3]
            add_arc_pr(lm_fst,from_id, to_id, ng3, ng3, p)
            if ng3 == '</s>':
                lm_fst[lm_id[ng2, ng3]].final = True

    pprint.pprint(lm_id)
    #connect init to start

    add_arc_pr(lm_fst,lm_id[INITIAL], lm_id[NULL], fst.EPSILON, fst.EPSILON, 0.0)
    lm_fst.write('data/explm.fst', sym_e, sym_e)
    """
    99 <s> -1.640621
     9 -2.411867   </s>

    for l in lm_lines:
        if l.strip() != '':
    """
