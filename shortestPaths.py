__author__ = 'arenduchintala'
import sys, fst


def parseargs(args):
    try:
        in_fst_path = args[args.index('-in') + 1]
        out_fst_path = args[args.index('-out') + 1]
        n = int(args[args.index('-n') + 1])
        return [in_fst_path, out_fst_path, n]
    except (ValueError, IndexError):
        sys.stderr.write('Usage: -in [name of fst(final)] -out [name of shortest path fst] -n [number of paths]')
        exit()


if __name__ == '__main__':
    [in_fst, out_fst, n] = parseargs(sys.argv)
    sym_f = fst.read_symbols('data/symf.bin')
    sym_e = fst.read_symbols('data/syme.bin')
    f = fst.read(in_fst)
    sp = f.shortest_path(n)
    sp.remove_epsilon()
    sp.write(out_fst, sym_f, sym_e)