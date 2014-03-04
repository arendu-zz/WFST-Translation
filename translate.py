import os
import sys
import pdb
if __name__ == '__main__':
    n = 1  # int(sys.argv[1])
    reordering = False
    input_file = str(sys.argv[1])
    for s in open(input_file,'r').readlines():
        #print s.strip()
        s = [str('"'+i+'"') for i in s.split()]
        #print ' '.join(s)
        os.system('mkdir t')
        os.system('python linearChain.py -fst t/lc.fst -str ' +' '.join(s) + ' -sym data/symf.bin')
        os.system('fstcompose t/lc.fst data/seg.fst > t/lc.seg.fst')

        if reordering:
            os.system('fstcompose t/lc.seg.fst data/reorder.fst > t/lc.re.fst')
            os.system('fstarcsort --sort_type="olabel" t/lc.re.fst > t/lc.re.sort.fst')
            os.system('fstcompose t/lc.re.sort.fst data/trans.fst > t/lc.trans.fst')
        else:
            os.system('fstcompose t/lc.seg.fst data/trans.fst > t/lc.trans.fst')

        os.system('fstcompose t/lc.trans.fst data/inv_seg.fst > t/lc.out.fst')
        os.system('fstconcat data/__s__.fst t/lc.out.fst > t/lc.s.out.fst')
        os.system('fstconcat t/lc.s.out.fst data/_s_.fst > t/lc.s.s.out.fst')
        os.system('fstcompose t/lc.s.s.out.fst data/lm.fst > t/lc.final.fst')
        os.system('python outputPaths.py t/lc.final.fst ' + str(n))
        os.system('rm -rf t')
