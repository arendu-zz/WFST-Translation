import os
import sys
import pdb

if __name__ == '__main__':
    n = 1  # int(sys.argv[1])
    reordering = True
    prn = 10000
    input_file = str(sys.argv[1])
    os.system('mkdir lcs-out-'+str(prn))
    for idx, s in enumerate(open(input_file, 'r').readlines()):
        print idx, s
        os.system('mkdir t')
        os.system('cp lcs/lc' + str(idx) + '.fst t/lc.fst ')
        os.system('fstcompose t/lc.fst data/seg.fst > t/lc.seg.fst')

        if reordering:
            os.system('fstcompose t/lc.seg.fst data/reorder.fst > t/lc.re.fst')
            os.system('fstarcsort --sort_type="olabel" t/lc.re.fst > t/lc.re.sort.fst')
            os.system('fstcompose t/lc.re.sort.fst data/trans.fst > t/lc.trans.fst')
        else:
            os.system('fstcompose t/lc.seg.fst data/trans.fst > t/lc.trans.fst')
        os.system('fstshortestpath -nshortest='+str(prn)+' t/lc.trans.fst > t/lc.short.trans.fst')
        os.system('fstcompose t/lc.short.trans.fst data/inv_seg.fst > t/lc.out.fst')
        os.system('fstconcat data/__s__.fst t/lc.out.fst > t/lc.s.out.fst')
        os.system('fstconcat t/lc.s.out.fst data/_s_.fst > t/lc.s.s.out.fst')
        os.system('fstshortestpath -nshortest='+str(prn)+' t/lc.s.s.out.fst > t/lc.s.s.short.out.fst')
        os.system('fstcompose t/lc.s.s.short.out.fst data/lm.fst > t/lc.final.fst')
        #os.system('python outputPaths.py t/lc.final.fst ' + str(n))
        os.system('fstshortestpath -nshortest=1 t/lc.final.fst > t/lc' + str(idx) + '.final.fst')
        os.system('cp t/lc' + str(idx) + '.final.fst lcs-out-'+str(prn)+'/lc' + str(idx) + '.final.fst')
        os.system('rm -rf t')

