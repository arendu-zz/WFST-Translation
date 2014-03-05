__author__ = 'arenduchintala'

import sys, os


if __name__ == '__main__':
    #symi = fst.read_symbols(sys.argv[2].strip())
    #symo = fst.read_symbols(sys.argv[3].strip())
    try:
        folder = str(sys.argv[1].strip())
        if folder[-1] != '/':
            folder += '/'
        inp_path = str(sys.argv[2].strip())
    except:
        print 'useage: python fst2txt.py [folder] [data/input]\n'  # takes 1-best
        exit()
    err = []
    for idx, l in enumerate(open(inp_path, 'r').readlines()):
        sys.stderr.write(str(idx) + '.' + l)
        fpath = (folder + 'lc' + str(idx) + '.final.fst')
        os.system('python printFinal.py ' + fpath)
