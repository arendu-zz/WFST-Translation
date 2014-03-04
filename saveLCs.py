__author__ = 'arenduchintala'
import os
import sys

if __name__ == '__main__':
    n = 1  # int(sys.argv[1])
    reordering = True
    input_file = str(sys.argv[1])
    os.system('mkdir lcs')
    for idx, s in enumerate(open(input_file, 'r').readlines()):
        #print s.strip()
        s = [str('"' + i + '"') for i in s.split()]
        #print ' '.join(s)
        os.system('python linearChain.py -fst lcs/lc' + str(idx) + '.fst -str ' + ' '.join(s) + ' -sym data/symf.bin')