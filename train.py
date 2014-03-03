__author__ = 'arenduchintala'
import os

os.system('python extractSym.py')
os.system('python makeTransAndSymTable.py')
os.system('python phraseSegmentation.py')
os.system('python makeLM.py')