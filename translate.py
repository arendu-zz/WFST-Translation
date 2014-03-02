import os
import sys
if __name__ == '__main__':
    n = int(sys.argv[1])
    s = str(' '.join(sys.argv[2:]))

    os.system('python linearChain.py -fst lc.fst -str ' +
              s.strip() + ' -sym data/symf.bin')
    os.system('fstcompose lc.fst data/seg.fst > lc.seg.fst')
    os.system('fstcompose lc.seg.fst data/trans.fst > lc.trans.fst')
    os.system('fstcompose lc.trans.fst data/inv_seg.fst > lc.out.fst')
    os.system('fstconcat data/__s__.fst lc.out.fst > lcs.out.fst')
    os.system('fstconcat lcs.out.fst data/_s_.fst > lc.final.fst')
    os.system('fstcompose lc.final.fst data/lm.fst > final.fst')
    os.system('rm lc.fst lc.trans.fst lc.seg.fst lcs.out.fst lc.out.fst lc.final.fst')
    os.system('python outputPaths.py final.fst ' + str(n))
