import os
import sys
import pdb

if __name__ == '__main__':
    n = 1  # int(sys.argv[1])
    reordering = True
    prn = int(sys.argv[2])
    input_file = str(sys.argv[1])
    os.system('mkdir lcs-out-' + str(prn))
    for idx, s in enumerate(open(input_file, 'r').readlines()):
        print idx, s
        os.system('mkdir t-' + str(prn))
        os.system('cp lcs/lc' + str(idx) + '.fst t/lc.fst ')
        os.system('fstcompose t-' + str(prn) + '/lc.fst data/seg.fst > t-' + str(prn) + '/lc.seg.fst')

        if reordering:
            os.system('fstcompose t-' + str(prn) + '/lc.seg.fst data/reorder.fst > t-' + str(prn) + '/lc.re.fst')
            os.system('fstarcsort --sort_type="olabel" t-' + str(prn) + '/lc.re.fst > t-' + str(prn) + '/lc.re.sort.fst')
            os.system('fstcompose t-' + str(prn) + '/lc.re.sort.fst data/trans.fst > t-' + str(prn) + '/lc.trans.fst')
        else:
            os.system('fstcompose t-' + str(prn) + '/lc.seg.fst data/trans.fst > t-' + str(prn) + '/lc.trans.fst')
        os.system('fstshortestpath -nshortest=' + str(prn) + ' t-' + str(prn) + '/lc.trans.fst > t-' + str(prn) + '/lc.short.trans.fst')
        os.system('fstcompose t-' + str(prn) + '/lc.short.trans.fst data/inv_seg.fst > t-' + str(prn) + '/lc.out.fst')
        os.system('fstconcat data/__s__.fst t-' + str(prn) + '/lc.out.fst > t-' + str(prn) + '/lc.s.out.fst')
        os.system('fstconcat t-' + str(prn) + '/lc.s.out.fst data/_s_.fst > t-' + str(prn) + '/lc.s.s.out.fst')
        os.system('fstshortestpath -nshortest=' + str(prn) + ' t-' + str(prn) + '/lc.s.s.out.fst > t-' + str(prn) + '/lc.s.s.short.out.fst')
        os.system('fstcompose t-' + str(prn) + '/lc.s.s.short.out.fst data/lm.fst > t-' + str(prn) + '/lc.final.fst')
        #os.system('python outputPaths.py t-'+str(prn)+'/lc.final.fst ' + str(n))
        os.system('fstshortestpath -nshortest=1 t-' + str(prn) + '/lc.final.fst > t-' + str(prn) + '/lc-ep-' + str(idx) + '.final.fst')
        os.system('fstrmepsilon t-' + str(prn) + '/lc-ep-' + str(idx) + '.final.fst > t-' + str(prn) + '/lc' + str(idx) + '.final.fst')
        os.system('cp t-' + str(prn) + '/lc' + str(idx) + '.final.fst lcs-out-' + str(prn) + '/lc' + str(idx) + '.final.fst')
        os.system('rm -rf t-' + str(prn))

