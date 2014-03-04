import os
import sys
import pdb
if __name__ == '__main__':
    n = 1  # int(sys.argv[1])
    reordering = True
    input_file = str(sys.argv[1])
    for s in open(input_file,'r').readlines():
        #print s.strip()
        s = [str('"'+i+'"') for i in s.split()]
        #print ' '.join(s)
        os.system('mkdir t2')
        os.system('python linearChain.py -fst t2/lc.fst -str ' +' '.join(s) + ' -sym data/symf.bin')
        os.system('fstcompose t2/lc.fst data/seg.fst > t2/lc.seg.fst')

        if reordering:
            os.system('fstcompose t2/lc.seg.fst data/reorder.fst > t2/lc.re.fst')
            os.system('fstarcsort --sort_type="olabel" t2/lc.re.fst > t2/lc.re.sort.fst')
            os.system('fstcompose t2/lc.re.sort.fst data/trans.fst > t2/lc.trans.fst')
        else:
            os.system('fstcompose t2/lc.seg.fst data/trans.fst > t2/lc.trans.fst')

        os.system('fstcompose t2/lc.trans.fst data/inv_seg.fst > t2/lc.out.fst')
        os.system('fstconcat data/__s__.fst t2/lc.out.fst > t2/lc.s.out.fst')
        os.system('fstconcat t2/lc.s.out.fst data/_s_.fst > t2/lc.s.s.out.fst')
        os.system('fstcompose t2/lc.s.s.out.fst data/lm.fst > t2/lc.final.fst')
        os.system('python outputPaths.py t2/lc.final.fst ' + str(n))
        os.system('rm -rf t2')
