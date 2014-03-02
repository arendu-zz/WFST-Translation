import os,sys
if __name__ == '__main__':
    n = int(sys.argv[1])
    s = str(' '.join(sys.argv[2:]))

    os.system('python linearChain.py -fst lc.fst -str ' + s.strip() + ' -sym data/symf.bin')
    os.system('fstcompose lc.fst data/seg.fst > lc.seg.fst')
    os.system('fstcompose lc.seg.fst data/trans.fst > lc.trans.fst')
    os.system('python outputPaths.py lc.trans.fst ' + str(n))
    os.system('rm lc.fst lc.trans.fst lc.seg.fst')
