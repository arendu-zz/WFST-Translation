__author__ = 'arenduchintala'

import fst
import phraseSegmentation


if __name__ == '__main__':
    phrases = [(tuple(l.split('|||')[0].split()), tuple(l.split('|||')[1].split()), float(l.split('|||')[2])) for l in
               open('data/tm', 'r').readlines()]