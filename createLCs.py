__author__ = 'arenduchintala'
import os
import sys

if __name__ == '__main__':
    n = 1
    reordering = True
    input_file = str('data/input')
    for idx, s in enumerate(open(input_file, 'r').read().lower().splitlines()):
        s = [str('"' + i + '"') for i in s.split()]
        os.system('mkdir lcs')
        os.system('python linearChain.py -fst lcs/lc' + str(idx) + '.fst -str ' + ' '.join(s) + ' -sym data/symf.bin')

