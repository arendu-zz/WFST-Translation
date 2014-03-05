import os
import sys
import pdb

if __name__ == '__main__':

    reordering = True
    prn = int(sys.argv[2])
    input_file = str(sys.argv[1])
    os.system('mkdir lcs-out-' + str(prn))
    dir = "t-" + str(prn)
    for idx, s in enumerate(open(input_file, 'r').readlines()):
        print idx, s
        if idx in [20, 22, 27]:  # the 3 files that had mem issues
            pass
        else:
            continue
        os.system('mkdir %s' % dir)
        os.system('cp lcs/lc' + str(idx) + ('.fst %s' % dir) + '/lc.fst ')
        os.system('fstcompose %s' % dir + '/lc.fst data/seg.fst > %s' % dir + '/lc.seg.fst')

        if reordering:
            os.system('fstcompose %s' % dir + '/lc.seg.fst data/reorder.fst > %s' % dir + '/lc.re.fst')
            os.system('fstarcsort --sort_type="olabel" %s' % dir + '/lc.re.fst > %s' % dir + '/lc.re.sort.fst')
            os.system('fstcompose %s' % dir + '/lc.re.sort.fst data/trans.fst > %s' % dir + '/lc.trans.fst')
        else:
            os.system('fstcompose %s' % dir + '/lc.seg.fst data/trans.fst > %s' % dir + '/lc.trans.fst')
        #os.system('fstshortestpath -nshortest=' + str(prn) + ' %s' % dir + '/lc.trans.fst > %s' % dir + '/lc.short.trans.fst')
        os.system('fstcompose %s' % dir + '/lc.trans.fst data/inv_seg.fst > %s' % dir + '/lc.out.fst')
        os.system('fstconcat data/__s__.fst %s' % dir + '/lc.out.fst > %s' % dir + '/lc.s.out.fst')
        os.system('fstconcat %s' % dir + '/lc.s.out.fst data/_s_.fst > %s' % dir + '/lc.s.s.out.fst')
        os.system('fstarcsort --sort_type="olabel" %s/lc.s.s.out.fst > %s/lc.s.s.out.sorted.fst' % (dir, dir))
        os.system('fstcompose %s' % dir + '/lc.s.s.out.sorted.fst data/unk.fst > %s' % dir + '/lc.unk.unsorted.fst')
        os.system('fstarcsort --sort_type="olabel" %s' % dir + '/lc.unk.unsorted.fst > %s' % dir + '/lc.unk.fst')
        if prn > 0:
            os.system('fstshortestpath -nshortest=' + str(prn) + ' %s' % dir + '/lc.unk.fst > %s' % dir + '/lc.s.s.short.out.fst')
            os.system('fstcompose %s' % dir + '/lc.s.s.short.out.fst data/explm-new.fst > %s' % dir + '/lc.final.fst')
        else:
            os.system('fstcompose %s' % dir + '/lc.unk.fst data/explm-new.fst > %s' % dir + '/lc.final.fst')
        #os.system('python outputPaths.py t-'+str(prn)+'/lc.final.fst ' + str(n))
        os.system('fstshortestpath -nshortest=1 %s' % dir + '/lc.final.fst > %s' % dir + '/lc-ep-' + str(idx) + '.final.fst')
        os.system('fstrmepsilon %s' % dir + '/lc-ep-' + str(idx) + '.final.fst > %s' % dir + '/lc' + str(idx) + '.final.fst')
        os.system('cp %s' % dir + '/lc' + str(idx) + '.final.fst lcs-out-' + str(prn) + '/lc' + str(idx) + '.final.fst')
        os.system('rm -rf %s' % dir)

