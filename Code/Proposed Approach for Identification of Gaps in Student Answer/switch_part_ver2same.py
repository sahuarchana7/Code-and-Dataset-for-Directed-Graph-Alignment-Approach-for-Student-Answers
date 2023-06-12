import nltk
from nltk import word_tokenize
import os
import subprocess
from xml.dom import minidom

from nltk.translate.bleu_score import modified_precision
from nltk.corpus import stopwords
import numpy as np

from gensim.models.keyedvectors import KeyedVectors

import string
import nltk
import numpy
import gensim
from nltk import tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities, utils, matutils
from gensim.models import Word2Vec
import re, collections
import math
import en
from nltk.corpus import wordnet as wn
import inflect
import enchant

import subprocess
from subprocess import Popen, PIPE
from subprocess import*
import string

from nltk.cluster import euclidean_distance
from nltk import cluster
from nltk.tag.stanford import StanfordPOSTagger as POS_Tag

from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


wordnet_lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
d = enchant.Dict("en_US")     
stopset = list(stopwords.words('english')) + ['across'] + ['underneath'] + ['within'] + ['halfway'] + ['slipperiness'] + ['neither'] + ['besides'] + ['sleet'] + ['nowhere'] + ['beyond'] + ['could'] + ['without'] + ['Dear'] + ['dear'] + ['someplace'] + ['must'] + ['can'] + ['would']



import individual_func

import threshold_f1


def remove_filess():
    os.remove('/location-to-store-output-files/FA_err1.txt')
    os.remove('/location-to-store-output-files/best_filter/profit_matrix.txt')    # specific to best filter
    os.remove('/location-to-store-output-files/best_filter/tuple_pairs1_u.txt')   # specific to best filter
    os.remove('/location-to-store-output-files/best_filter/tuple_pairs2_u.txt')   # specific to best filter
    os.remove('/location-to-store-output-files/hungarian_results.txt') # specific to best filter
    




def remove_filess_1():
    os.remove('/location-to-store-output-files/FA_err1.txt')
   

def remove_filess_2():
    
    os.remove('/location-to-store-output-files/graphm-0.52/arch/cost.csv')
    os.remove('/location-to-store-output-files/graphm-0.52/arch/m_adj.csv')
    os.remove('/location-to-store-output-files/graphm-0.52/arch/s_adj.csv')
    os.remove('/location-to-store-output-files/graphm-0.52/arch/new_cost.csv')
    os.remove('/location-to-store-output-files/best_filter/profit_matrix.txt')
    os.remove('/location-to-store-output-files/best_filter/tuple_pairs1_u.txt')
    os.remove('/location-to-store-output-files/best_filter/tuple_pairs2_u.txt')
    os.remove('/location-to-store-output-files/hungarian_results.txt')

def remove_filess_3():
    os.remove('/location-to-store-output-files/tp.txt')


def combi_1(argument):
    individual_func.cluster_algo_output()
    individual_func.fix_point1()
    threshold_f1.best_filter(argument)

def combi_2(argument):
    individual_func.cluster_algo_output()
    individual_func.fix_point1()
    threshold_f1.threshold_filter(argument)

def combi_3(argument):                                                     
    individual_func.cluster_algo_output()
    individual_func.fix_point1()
    threshold_f1.exact_filter(argument)
    


def combi_13(argument):
    os.system("python /location-to-store-output-files/undirected_gapsvar.py")
    threshold_f1.best_filter(argument)

def combi_14(argument):
    os.system("python /location-to-store-output-files/undirected_gapsvar.py")
    threshold_f1.threshold_filter(argument)

def combi_15(argument):
    os.system("python /location-to-store-output-files/undirected_gapsvar.py")
    threshold_f1.exact_filter(argument)


def various_combos(argument):
    switcher={
    1: combi_1,
    2: combi_2,
    3: combi_3,    
}

# Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "Invalid combo")
# Execute the function
    return func(argument)


print various_combos(1)

remove_filess()



print various_combos(2)
remove_filess_1()




print various_combos(3)

remove_filess_1()



print various_combos(13)
remove_filess_2()

print various_combos(14)
remove_filess_2()

print various_combos(15)
remove_filess_2()

























































    
    
    






  


  
















