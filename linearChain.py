__author__ = 'arenduchintala'
"""
accepts a string and file name,  and writes a fst representing the input string.
"""
import sys, re, fst


def parseargs(args):
    try:
        a = re.split('\s(?=-str)|(?<=-str)\s|\s(?=-fst)|(?<=-fst)\s|\s(?=-sym)|(?<=-sym)\s', ' '.join(args))
        #print 'split', a
        fst_path = a[a.index('-fst') + 1]
        #print fst_path
        s = a[a.index('-str') + 1]
        #print s
        s = s.strip()
        sym = a[a.index('-sym') + 1]
        #print sym
        return [s, fst_path, sym]
    except (ValueError, IndexError):
        sys.stderr.write('Usage: -fst [name of fst] -str ' \
                         '[string to encode as fst (no quotes,tokens separated by white space)] ' \
                         '-sym [binary symbol file]\n e.g. -fst sentence.fst -str hello world -sym mysym.bin\n')
        exit()


def log_linear_chain(txt, sym_f):
    txt = txt.split()
    lc = fst.LogTransducer(sym_f, sym_f)
    for idx, t in enumerate(txt):
        lc.add_arc(idx, idx + 1, t, t, 0.0)
    lc[idx + 1].final = True
    return lc


if __name__ == '__main__':
    [s, fst_path, sym_path] = parseargs(sys.argv)
    sym = fst.read_symbols(sym_path)
    lc = log_linear_chain(s, sym)
    lc.write(fst_path, sym, sym)
