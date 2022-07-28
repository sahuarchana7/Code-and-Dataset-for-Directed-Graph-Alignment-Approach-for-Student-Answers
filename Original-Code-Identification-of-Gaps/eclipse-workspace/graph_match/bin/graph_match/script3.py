import os
from stat import *
 
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
from nltk import pos_tag
import sys
from gensim.models.keyedvectors import KeyedVectors
import ast
from nltk.tag.stanford import StanfordPOSTagger as POS_Tag

from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

d = enchant.Dict("en_US")
d1 = enchant.Dict("en_UK")

wordnet_lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stopset = list(stopwords.words('english')) + ['across'] + ['underneath'] + ['within'] + ['halfway'] + ['slipperiness'] + ['neither'] + ['besides'] + ['sleet'] + ['nowhere'] + ['beyond'] + ['could'] + ['without'] + ['Dear'] + ['dear'] + ['someplace'] + ['do'] + ['something'] + ['else']
#print stopset
#stopset.remove('same')
#word_vectors = KeyedVectors.load_word2vec_format('/home/archana/wiki/pretrained_wiki_model/3/enwiki_5_ner.txt', binary=False)

#wc = sys.argv[3]

#a = "Data members and member functions"
#b = "constructors"
#b = "variables"

#a = sys.argv[1]
#b = sys.argv[2]

#inputs = sys.argv[1]


inputs = "[[the switch, A bulb], [the switch, by a switch when the switch occurs in the same path as the bulb], [the switch, the switch], [the switch, in the same path as the bulb when], [the switch, the switch], [the switch, in the same path as the bulb], [in the same path, A bulb], [in the same path, by a switch when the switch occurs in the same path as the bulb], [in the same path, the switch], [in the same path, in the same path as the bulb when], [in the same path, the switch], [in the same path, in the same path as the bulb], [A switch, A bulb], [A switch, by a switch when the switch occurs in the same path as the bulb], [A switch, the switch], [A switch, in the same path as the bulb when], [A switch, the switch], [A switch, in the same path as the bulb], [a bulb, A bulb], [a bulb, by a switch when the switch occurs in the same path as the bulb], [a bulb, the switch], [a bulb, in the same path as the bulb when], [a bulb, the switch], [a bulb, in the same path as the bulb], [the switch, A bulb], [the switch, by a switch when the switch occurs in the same path as the bulb], [the switch, the switch], [the switch, in the same path as the bulb when], [the switch, the switch], [the switch, in the same path as the bulb], [in the same path when, A bulb], [in the same path when, by a switch when the switch occurs in the same path as the bulb], [in the same path when, the switch], [in the same path when, in the same path as the bulb when], [in the same path when, the switch], [in the same path when, in the same path as the bulb], [the bulb, A bulb], [the bulb, by a switch when the switch occurs in the same path as the bulb], [the bulb, the switch], [the bulb, in the same path as the bulb when], [the bulb, the switch], [the bulb, in the same path as the bulb], [in the same path, A bulb], [in the same path, by a switch when the switch occurs in the same path as the bulb], [in the same path, the switch], [in the same path, in the same path as the bulb when], [in the same path, the switch], [in the same path, in the same path as the bulb], [the bulb, A bulb], [the bulb, by a switch when the switch occurs in the same path as the bulb], [the bulb, the switch], [the bulb, in the same path as the bulb when], [the bulb, the switch], [the bulb, in the same path as the bulb], [in the same path when, A bulb], [in the same path when, by a switch when the switch occurs in the same path as the bulb], [in the same path when, the switch], [in the same path when, in the same path as the bulb when], [in the same path when, the switch], [in the same path when, in the same path as the bulb], [A switch, A bulb], [A switch, by a switch when the switch occurs in the same path as the bulb], [A switch, the switch], [A switch, in the same path as the bulb when], [A switch, the switch], [A switch, in the same path as the bulb], [the bulb appear in the same path, A bulb], [the bulb appear in the same path, by a switch when the switch occurs in the same path as the bulb], [the bulb appear in the same path, the switch], [the bulb appear in the same path, in the same path as the bulb when], [the bulb appear in the same path, the switch], [the bulb appear in the same path, in the same path as the bulb], [A switch, A bulb], [A switch, by a switch when the switch occurs in the same path as the bulb], [A switch, the switch], [A switch, in the same path as the bulb when], [A switch, the switch], [A switch, in the same path as the bulb], [a bulb when the switch, A bulb], [a bulb when the switch, by a switch when the switch occurs in the same path as the bulb], [a bulb when the switch, the switch], [a bulb when the switch, in the same path as the bulb when], [a bulb when the switch, the switch], [a bulb when the switch, in the same path as the bulb]]"




#inputs = "[[A part of the plant, The part of the plant], [A part of the plant, a seed], [seeds, The part of the plant], [seeds, a seed], [A part of the plant, The part of the plant], [A part of the plant, a seed], [the fruit, The part of the plant], [the fruit, a seed]]"

#inputs = "[[The arrays, each element of that array], [The arrays, to zero by the compiler when the array is created], [The arrays, the array], [The arrays, created], [The arrays, each element of that array], [The arrays, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [The arrays, A program], [The arrays, at all in c + +], [The arrays, a static array], [The arrays, explicitly by the programmer], [The arrays, their declarations], [The arrays, when], [The arrays, each element of that array], [The arrays, to zero by the compiler If a static array is not initialized explicitly by the programmer], [The arrays, the array], [The arrays, when], [The arrays, their declarations], [The arrays, encountered], [The arrays, Non static array members], [The arrays, at all], [The arrays, each element of that array], [The arrays, to zero by the compiler], [The arrays, their declarations], [The arrays, first], [The arrays, Non static array members], [The arrays, at all in c + +], [The arrays, their], [The arrays, declarations], [The arrays, a static array], [The arrays, explicitly], [The arrays, static local arrays when their declarations are first encountered], [The arrays, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [The arrays, A program], [The arrays, at all], [only once, each element of that array], [only once, to zero by the compiler when the array is created], [only once, the array], [only once, created], [only once, each element of that array], [only once, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [only once, A program], [only once, at all in c + +], [only once, a static array], [only once, explicitly by the programmer], [only once, their declarations], [only once, when], [only once, each element of that array], [only once, to zero by the compiler If a static array is not initialized explicitly by the programmer], [only once, the array], [only once, when], [only once, their declarations], [only once, encountered], [only once, Non static array members], [only once, at all], [only once, each element of that array], [only once, to zero by the compiler], [only once, their declarations], [only once, first], [only once, Non static array members], [only once, at all in c + +], [only once, their], [only once, declarations], [only once, a static array], [only once, explicitly], [only once, static local arrays when their declarations are first encountered], [only once, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [only once, A program], [only once, at all], [The arrays, each element of that array], [The arrays, to zero by the compiler when the array is created], [The arrays, the array], [The arrays, created], [The arrays, each element of that array], [The arrays, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [The arrays, A program], [The arrays, at all in c + +], [The arrays, a static array], [The arrays, explicitly by the programmer], [The arrays, their declarations], [The arrays, when], [The arrays, each element of that array], [The arrays, to zero by the compiler If a static array is not initialized explicitly by the programmer], [The arrays, the array], [The arrays, when], [The arrays, their declarations], [The arrays, encountered], [The arrays, Non static array members], [The arrays, at all], [The arrays, each element of that array], [The arrays, to zero by the compiler], [The arrays, their declarations], [The arrays, first], [The arrays, Non static array members], [The arrays, at all in c + +], [The arrays, their], [The arrays, declarations], [The arrays, a static array], [The arrays, explicitly], [The arrays, static local arrays when their declarations are first encountered], [The arrays, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [The arrays, A program], [The arrays, at all], [as static live throughout the life of the program, each element of that array], [as static live throughout the life of the program, to zero by the compiler when the array is created], [as static live throughout the life of the program, the array], [as static live throughout the life of the program, created], [as static live throughout the life of the program, each element of that array], [as static live throughout the life of the program, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [as static live throughout the life of the program, A program], [as static live throughout the life of the program, at all in c + +], [as static live throughout the life of the program, a static array], [as static live throughout the life of the program, explicitly by the programmer], [as static live throughout the life of the program, their declarations], [as static live throughout the life of the program, when], [as static live throughout the life of the program, each element of that array], [as static live throughout the life of the program, to zero by the compiler If a static array is not initialized explicitly by the programmer], [as static live throughout the life of the program, the array], [as static live throughout the life of the program, when], [as static live throughout the life of the program, their declarations], [as static live throughout the life of the program, encountered], [as static live throughout the life of the program, Non static array members], [as static live throughout the life of the program, at all], [as static live throughout the life of the program, each element of that array], [as static live throughout the life of the program, to zero by the compiler], [as static live throughout the life of the program, their declarations], [as static live throughout the life of the program, first], [as static live throughout the life of the program, Non static array members], [as static live throughout the life of the program, at all in c + +], [as static live throughout the life of the program, their], [as static live throughout the life of the program, declarations], [as static live throughout the life of the program, a static array], [as static live throughout the life of the program, explicitly], [as static live throughout the life of the program, static local arrays when their declarations are first encountered], [as static live throughout the life of the program, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [as static live throughout the life of the program, A program], [as static live throughout the life of the program, at all], [the function, each element of that array], [the function, to zero by the compiler when the array is created], [the function, the array], [the function, created], [the function, each element of that array], [the function, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [the function, A program], [the function, at all in c + +], [the function, a static array], [the function, explicitly by the programmer], [the function, their declarations], [the function, when], [the function, each element of that array], [the function, to zero by the compiler If a static array is not initialized explicitly by the programmer], [the function, the array], [the function, when], [the function, their declarations], [the function, encountered], [the function, Non static array members], [the function, at all], [the function, each element of that array], [the function, to zero by the compiler], [the function, their declarations], [the function, first], [the function, Non static array members], [the function, at all in c + +], [the function, their], [the function, declarations], [the function, a static array], [the function, explicitly], [the function, static local arrays when their declarations are first encountered], [the function, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [the function, A program], [the function, at all], [first, each element of that array], [first, to zero by the compiler when the array is created], [first, the array], [first, created], [first, each element of that array], [first, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [first, A program], [first, at all in c + +], [first, a static array], [first, explicitly by the programmer], [first, their declarations], [first, when], [first, each element of that array], [first, to zero by the compiler If a static array is not initialized explicitly by the programmer], [first, the array], [first, when], [first, their declarations], [first, encountered], [first, Non static array members], [first, at all], [first, each element of that array], [first, to zero by the compiler], [first, their declarations], [first, first], [first, Non static array members], [first, at all in c + +], [first, their], [first, declarations], [first, a static array], [first, explicitly], [first, static local arrays when their declarations are first encountered], [first, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [first, A program], [first, at all], [The arrays, each element of that array], [The arrays, to zero by the compiler when the array is created], [The arrays, the array], [The arrays, created], [The arrays, each element of that array], [The arrays, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [The arrays, A program], [The arrays, at all in c + +], [The arrays, a static array], [The arrays, explicitly by the programmer], [The arrays, their declarations], [The arrays, when], [The arrays, each element of that array], [The arrays, to zero by the compiler If a static array is not initialized explicitly by the programmer], [The arrays, the array], [The arrays, when], [The arrays, their declarations], [The arrays, encountered], [The arrays, Non static array members], [The arrays, at all], [The arrays, each element of that array], [The arrays, to zero by the compiler], [The arrays, their declarations], [The arrays, first], [The arrays, Non static array members], [The arrays, at all in c + +], [The arrays, their], [The arrays, declarations], [The arrays, a static array], [The arrays, explicitly], [The arrays, static local arrays when their declarations are first encountered], [The arrays, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [The arrays, A program], [The arrays, at all], [only once when the function is first called, each element of that array], [only once when the function is first called, to zero by the compiler when the array is created], [only once when the function is first called, the array], [only once when the function is first called, created], [only once when the function is first called, each element of that array], [only once when the function is first called, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [only once when the function is first called, A program], [only once when the function is first called, at all in c + +], [only once when the function is first called, a static array], [only once when the function is first called, explicitly by the programmer], [only once when the function is first called, their declarations], [only once when the function is first called, when], [only once when the function is first called, each element of that array], [only once when the function is first called, to zero by the compiler If a static array is not initialized explicitly by the programmer], [only once when the function is first called, the array], [only once when the function is first called, when], [only once when the function is first called, their declarations], [only once when the function is first called, encountered], [only once when the function is first called, Non static array members], [only once when the function is first called, at all], [only once when the function is first called, each element of that array], [only once when the function is first called, to zero by the compiler], [only once when the function is first called, their declarations], [only once when the function is first called, first], [only once when the function is first called, Non static array members], [only once when the function is first called, at all in c + +], [only once when the function is first called, their], [only once when the function is first called, declarations], [only once when the function is first called, a static array], [only once when the function is first called, explicitly], [only once when the function is first called, static local arrays when their declarations are first encountered], [only once when the function is first called, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [only once when the function is first called, A program], [only once when the function is first called, at all], [the function, each element of that array], [the function, to zero by the compiler when the array is created], [the function, the array], [the function, created], [the function, each element of that array], [the function, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [the function, A program], [the function, at all in c + +], [the function, a static array], [the function, explicitly by the programmer], [the function, their declarations], [the function, when], [the function, each element of that array], [the function, to zero by the compiler If a static array is not initialized explicitly by the programmer], [the function, the array], [the function, when], [the function, their declarations], [the function, encountered], [the function, Non static array members], [the function, at all], [the function, each element of that array], [the function, to zero by the compiler], [the function, their declarations], [the function, first], [the function, Non static array members], [the function, at all in c + +], [the function, their], [the function, declarations], [the function, a static array], [the function, explicitly], [the function, static local arrays when their declarations are first encountered], [the function, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [the function, A program], [the function, at all], [called, each element of that array], [called, to zero by the compiler when the array is created], [called, the array], [called, created], [called, each element of that array], [called, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [called, A program], [called, at all in c + +], [called, a static array], [called, explicitly by the programmer], [called, their declarations], [called, when], [called, each element of that array], [called, to zero by the compiler If a static array is not initialized explicitly by the programmer], [called, the array], [called, when], [called, their declarations], [called, encountered], [called, Non static array members], [called, at all], [called, each element of that array], [called, to zero by the compiler], [called, their declarations], [called, first], [called, Non static array members], [called, at all in c + +], [called, their], [called, declarations], [called, a static array], [called, explicitly], [called, static local arrays when their declarations are first encountered], [called, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [called, A program], [called, at all], [the function, each element of that array], [the function, to zero by the compiler when the array is created], [the function, the array], [the function, created], [the function, each element of that array], [the function, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [the function, A program], [the function, at all in c + +], [the function, a static array], [the function, explicitly by the programmer], [the function, their declarations], [the function, when], [the function, each element of that array], [the function, to zero by the compiler If a static array is not initialized explicitly by the programmer], [the function, the array], [the function, when], [the function, their declarations], [the function, encountered], [the function, Non static array members], [the function, at all], [the function, each element of that array], [the function, to zero by the compiler], [the function, their declarations], [the function, first], [the function, Non static array members], [the function, at all in c + +], [the function, their], [the function, declarations], [the function, a static array], [the function, explicitly], [the function, static local arrays when their declarations are first encountered], [the function, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [the function, A program], [the function, at all], [when, each element of that array], [when, to zero by the compiler when the array is created], [when, the array], [when, created], [when, each element of that array], [when, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [when, A program], [when, at all in c + +], [when, a static array], [when, explicitly by the programmer], [when, their declarations], [when, when], [when, each element of that array], [when, to zero by the compiler If a static array is not initialized explicitly by the programmer], [when, the array], [when, when], [when, their declarations], [when, encountered], [when, Non static array members], [when, at all], [when, each element of that array], [when, to zero by the compiler], [when, their declarations], [when, first], [when, Non static array members], [when, at all in c + +], [when, their], [when, declarations], [when, a static array], [when, explicitly], [when, static local arrays when their declarations are first encountered], [when, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [when, A program], [when, at all], [static, each element of that array], [static, to zero by the compiler when the array is created], [static, the array], [static, created], [static, each element of that array], [static, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [static, A program], [static, at all in c + +], [static, a static array], [static, explicitly by the programmer], [static, their declarations], [static, when], [static, each element of that array], [static, to zero by the compiler If a static array is not initialized explicitly by the programmer], [static, the array], [static, when], [static, their declarations], [static, encountered], [static, Non static array members], [static, at all], [static, each element of that array], [static, to zero by the compiler], [static, their declarations], [static, first], [static, Non static array members], [static, at all in c + +], [static, their], [static, declarations], [static, a static array], [static, explicitly], [static, static local arrays when their declarations are first encountered], [static, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [static, A program], [static, at all], [throughout the life of the program, each element of that array], [throughout the life of the program, to zero by the compiler when the array is created], [throughout the life of the program, the array], [throughout the life of the program, created], [throughout the life of the program, each element of that array], [throughout the life of the program, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [throughout the life of the program, A program], [throughout the life of the program, at all in c + +], [throughout the life of the program, a static array], [throughout the life of the program, explicitly by the programmer], [throughout the life of the program, their declarations], [throughout the life of the program, when], [throughout the life of the program, each element of that array], [throughout the life of the program, to zero by the compiler If a static array is not initialized explicitly by the programmer], [throughout the life of the program, the array], [throughout the life of the program, when], [throughout the life of the program, their declarations], [throughout the life of the program, encountered], [throughout the life of the program, Non static array members], [throughout the life of the program, at all], [throughout the life of the program, each element of that array], [throughout the life of the program, to zero by the compiler], [throughout the life of the program, their declarations], [throughout the life of the program, first], [throughout the life of the program, Non static array members], [throughout the life of the program, at all in c + +], [throughout the life of the program, their], [throughout the life of the program, declarations], [throughout the life of the program, a static array], [throughout the life of the program, explicitly], [throughout the life of the program, static local arrays when their declarations are first encountered], [throughout the life of the program, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [throughout the life of the program, A program], [throughout the life of the program, at all], [the function, each element of that array], [the function, to zero by the compiler when the array is created], [the function, the array], [the function, created], [the function, each element of that array], [the function, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [the function, A program], [the function, at all in c + +], [the function, a static array], [the function, explicitly by the programmer], [the function, their declarations], [the function, when], [the function, each element of that array], [the function, to zero by the compiler If a static array is not initialized explicitly by the programmer], [the function, the array], [the function, when], [the function, their declarations], [the function, encountered], [the function, Non static array members], [the function, at all], [the function, each element of that array], [the function, to zero by the compiler], [the function, their declarations], [the function, first], [the function, Non static array members], [the function, at all in c + +], [the function, their], [the function, declarations], [the function, a static array], [the function, explicitly], [the function, static local arrays when their declarations are first encountered], [the function, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [the function, A program], [the function, at all], [the array, each element of that array], [the array, to zero by the compiler when the array is created], [the array, the array], [the array, created], [the array, each element of that array], [the array, to zero by the compiler when the array is created If a static array is not initialized explicitly by the programmer], [the array, A program], [the array, at all in c + +], [the array, a static array], [the array, explicitly by the programmer], [the array, their declarations], [the array, when], [the array, each element of that array], [the array, to zero by the compiler If a static array is not initialized explicitly by the programmer], [the array, the array], [the array, when], [the array, their declarations], [the array, encountered], [the array, Non static array members], [the array, at all], [the array, each element of that array], [the array, to zero by the compiler], [the array, their declarations], [the array, first], [the array, Non static array members], [the array, at all in c + +], [the array, their], [the array, declarations], [the array, a static array], [the array, explicitly], [the array, static local arrays when their declarations are first encountered], [the array, If a static array is not initialized explicitly by the programmer each element of that array is initialized to zero by the compiler when the array is created], [the array, A program], [the array, at all]]"



#inputs = "[[A constructor, an object], [A constructor, when], [A constructor, Constructor], [A constructor, independent to the rest of the code], [A constructor, an object], [A constructor, created], [A constructor, a function], [A constructor, a portion of code], [A constructor, a larger program], [A constructor, a specific task], [A constructor, Constructor], [A constructor, a special block], [A constructor, a function], [A constructor, a portion However], [A constructor, an object], [A constructor, is], [A constructor, a function], [A constructor, a portion], [A constructor, statements], [A constructor, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [A constructor, statements], [A constructor, independent to the rest of the code], [A constructor, statements], [A constructor, when an object is created], [A constructor, an object], [A constructor, when], [A constructor, Constructor], [A constructor, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, an object], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, when], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, Constructor], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, independent to the rest of the code], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, an object], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, created], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a function], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a portion of code], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a larger program], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a specific task], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, Constructor], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a special block], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a function], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a portion However], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, an object], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, is], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a function], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a portion], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, statements], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, statements], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, independent to the rest of the code], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, statements], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, when an object is created], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, an object], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, when], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, Constructor], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [functions, an object], [functions, when], [functions, Constructor], [functions, independent to the rest of the code], [functions, an object], [functions, created], [functions, a function], [functions, a portion of code], [functions, a larger program], [functions, a specific task], [functions, Constructor], [functions, a special block], [functions, a function], [functions, a portion However], [functions, an object], [functions, is], [functions, a function], [functions, a portion], [functions, statements], [functions, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [functions, statements], [functions, independent to the rest of the code], [functions, statements], [functions, when an object is created], [functions, an object], [functions, when], [functions, Constructor], [functions, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [to indicate a return type, an object], [to indicate a return type, when], [to indicate a return type, Constructor], [to indicate a return type, independent to the rest of the code], [to indicate a return type, an object], [to indicate a return type, created], [to indicate a return type, a function], [to indicate a return type, a portion of code], [to indicate a return type, a larger program], [to indicate a return type, a specific task], [to indicate a return type, Constructor], [to indicate a return type, a special block], [to indicate a return type, a function], [to indicate a return type, a portion However], [to indicate a return type, an object], [to indicate a return type, is], [to indicate a return type, a function], [to indicate a return type, a portion], [to indicate a return type, statements], [to indicate a return type, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [to indicate a return type, statements], [to indicate a return type, independent to the rest of the code], [to indicate a return type, statements], [to indicate a return type, when an object is created], [to indicate a return type, an object], [to indicate a return type, when], [to indicate a return type, Constructor], [to indicate a return type, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [an object, an object], [an object, when], [an object, Constructor], [an object, independent to the rest of the code], [an object, an object], [an object, created], [an object, a function], [an object, a portion of code], [an object, a larger program], [an object, a specific task], [an object, Constructor], [an object, a special block], [an object, a function], [an object, a portion However], [an object, an object], [an object, is], [an object, a function], [an object, a portion], [an object, statements], [an object, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [an object, statements], [an object, independent to the rest of the code], [an object, statements], [an object, when an object is created], [an object, an object], [an object, when], [an object, Constructor], [an object, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [whereas a function needs to be called explicitly Constructors do not have return type, an object], [whereas a function needs to be called explicitly Constructors do not have return type, when], [whereas a function needs to be called explicitly Constructors do not have return type, Constructor], [whereas a function needs to be called explicitly Constructors do not have return type, independent to the rest of the code], [whereas a function needs to be called explicitly Constructors do not have return type, an object], [whereas a function needs to be called explicitly Constructors do not have return type, created], [whereas a function needs to be called explicitly Constructors do not have return type, a function], [whereas a function needs to be called explicitly Constructors do not have return type, a portion of code], [whereas a function needs to be called explicitly Constructors do not have return type, a larger program], [whereas a function needs to be called explicitly Constructors do not have return type, a specific task], [whereas a function needs to be called explicitly Constructors do not have return type, Constructor], [whereas a function needs to be called explicitly Constructors do not have return type, a special block], [whereas a function needs to be called explicitly Constructors do not have return type, a function], [whereas a function needs to be called explicitly Constructors do not have return type, a portion However], [whereas a function needs to be called explicitly Constructors do not have return type, an object], [whereas a function needs to be called explicitly Constructors do not have return type, is], [whereas a function needs to be called explicitly Constructors do not have return type, a function], [whereas a function needs to be called explicitly Constructors do not have return type, a portion], [whereas a function needs to be called explicitly Constructors do not have return type, statements], [whereas a function needs to be called explicitly Constructors do not have return type, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [whereas a function needs to be called explicitly Constructors do not have return type, statements], [whereas a function needs to be called explicitly Constructors do not have return type, independent to the rest of the code], [whereas a function needs to be called explicitly Constructors do not have return type, statements], [whereas a function needs to be called explicitly Constructors do not have return type, when an object is created], [whereas a function needs to be called explicitly Constructors do not have return type, an object], [whereas a function needs to be called explicitly Constructors do not have return type, when], [whereas a function needs to be called explicitly Constructors do not have return type, Constructor], [whereas a function needs to be called explicitly Constructors do not have return type, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [an object, an object], [an object, when], [an object, Constructor], [an object, independent to the rest of the code], [an object, an object], [an object, created], [an object, a function], [an object, a portion of code], [an object, a larger program], [an object, a specific task], [an object, Constructor], [an object, a special block], [an object, a function], [an object, a portion However], [an object, an object], [an object, is], [an object, a function], [an object, a portion], [an object, statements], [an object, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [an object, statements], [an object, independent to the rest of the code], [an object, statements], [an object, when an object is created], [an object, an object], [an object, when], [an object, Constructor], [an object, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [whereas a function needs to be called explicitly Constructors do not have return type whenever, an object], [whereas a function needs to be called explicitly Constructors do not have return type whenever, when], [whereas a function needs to be called explicitly Constructors do not have return type whenever, Constructor], [whereas a function needs to be called explicitly Constructors do not have return type whenever, independent to the rest of the code], [whereas a function needs to be called explicitly Constructors do not have return type whenever, an object], [whereas a function needs to be called explicitly Constructors do not have return type whenever, created], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a function], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a portion of code], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a larger program], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a specific task], [whereas a function needs to be called explicitly Constructors do not have return type whenever, Constructor], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a special block], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a function], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a portion However], [whereas a function needs to be called explicitly Constructors do not have return type whenever, an object], [whereas a function needs to be called explicitly Constructors do not have return type whenever, is], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a function], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a portion], [whereas a function needs to be called explicitly Constructors do not have return type whenever, statements], [whereas a function needs to be called explicitly Constructors do not have return type whenever, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [whereas a function needs to be called explicitly Constructors do not have return type whenever, statements], [whereas a function needs to be called explicitly Constructors do not have return type whenever, independent to the rest of the code], [whereas a function needs to be called explicitly Constructors do not have return type whenever, statements], [whereas a function needs to be called explicitly Constructors do not have return type whenever, when an object is created], [whereas a function needs to be called explicitly Constructors do not have return type whenever, an object], [whereas a function needs to be called explicitly Constructors do not have return type whenever, when], [whereas a function needs to be called explicitly Constructors do not have return type whenever, Constructor], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [a function, an object], [a function, when], [a function, Constructor], [a function, independent to the rest of the code], [a function, an object], [a function, created], [a function, a function], [a function, a portion of code], [a function, a larger program], [a function, a specific task], [a function, Constructor], [a function, a special block], [a function, a function], [a function, a portion However], [a function, an object], [a function, is], [a function, a function], [a function, a portion], [a function, statements], [a function, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [a function, statements], [a function, independent to the rest of the code], [a function, statements], [a function, when an object is created], [a function, an object], [a function, when], [a function, Constructor], [a function, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [to be called explicitly Constructors do not have return type, an object], [to be called explicitly Constructors do not have return type, when], [to be called explicitly Constructors do not have return type, Constructor], [to be called explicitly Constructors do not have return type, independent to the rest of the code], [to be called explicitly Constructors do not have return type, an object], [to be called explicitly Constructors do not have return type, created], [to be called explicitly Constructors do not have return type, a function], [to be called explicitly Constructors do not have return type, a portion of code], [to be called explicitly Constructors do not have return type, a larger program], [to be called explicitly Constructors do not have return type, a specific task], [to be called explicitly Constructors do not have return type, Constructor], [to be called explicitly Constructors do not have return type, a special block], [to be called explicitly Constructors do not have return type, a function], [to be called explicitly Constructors do not have return type, a portion However], [to be called explicitly Constructors do not have return type, an object], [to be called explicitly Constructors do not have return type, is], [to be called explicitly Constructors do not have return type, a function], [to be called explicitly Constructors do not have return type, a portion], [to be called explicitly Constructors do not have return type, statements], [to be called explicitly Constructors do not have return type, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [to be called explicitly Constructors do not have return type, statements], [to be called explicitly Constructors do not have return type, independent to the rest of the code], [to be called explicitly Constructors do not have return type, statements], [to be called explicitly Constructors do not have return type, when an object is created], [to be called explicitly Constructors do not have return type, an object], [to be called explicitly Constructors do not have return type, when], [to be called explicitly Constructors do not have return type, Constructor], [to be called explicitly Constructors do not have return type, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [explicitly Constructors, an object], [explicitly Constructors, when], [explicitly Constructors, Constructor], [explicitly Constructors, independent to the rest of the code], [explicitly Constructors, an object], [explicitly Constructors, created], [explicitly Constructors, a function], [explicitly Constructors, a portion of code], [explicitly Constructors, a larger program], [explicitly Constructors, a specific task], [explicitly Constructors, Constructor], [explicitly Constructors, a special block], [explicitly Constructors, a function], [explicitly Constructors, a portion However], [explicitly Constructors, an object], [explicitly Constructors, is], [explicitly Constructors, a function], [explicitly Constructors, a portion], [explicitly Constructors, statements], [explicitly Constructors, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [explicitly Constructors, statements], [explicitly Constructors, independent to the rest of the code], [explicitly Constructors, statements], [explicitly Constructors, when an object is created], [explicitly Constructors, an object], [explicitly Constructors, when], [explicitly Constructors, Constructor], [explicitly Constructors, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [return type, an object], [return type, when], [return type, Constructor], [return type, independent to the rest of the code], [return type, an object], [return type, created], [return type, a function], [return type, a portion of code], [return type, a larger program], [return type, a specific task], [return type, Constructor], [return type, a special block], [return type, a function], [return type, a portion However], [return type, an object], [return type, is], [return type, a function], [return type, a portion], [return type, statements], [return type, when an object is created when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program], [return type, statements], [return type, independent to the rest of the code], [return type, statements], [return type, when an object is created], [return type, an object], [return type, when], [return type, Constructor], [return type, a special block of statements called when an object is created either when an object is declared statically or constructed on the stack However a function is a portion of code within a larger program]]"


#inputs = "[[A constructor, Functions], [A constructor, A constructor is typically used to intialize data members], [A constructor, A constructor is typically used to intialize data members], [A constructor, maybe], [A constructor, Functions], [A constructor, allocate resources for instance memory operations], [A constructor, A constructor], [A constructor, to allocate resources typically], [A constructor, A constructor], [A constructor, to allocate resources], [A constructor, instance memory], [A constructor, files], [A constructor, allocate resources for instance memory operations], [A constructor, globally], [A constructor, A constructor], [A constructor, to intialize data members typically], [A constructor, A constructor], [A constructor, to allocate resources for instance memory], [A constructor, files], [A constructor, etc Also a constructor can not return values], [A constructor, allocate resources for instance memory operations], [A constructor, maybe], [A constructor, allocate resources for instance memory operations], [A constructor, defined], [A constructor, A constructor], [A constructor, to intialize data members for instance memory], [A constructor, A constructor is typically used to intialize data members], [A constructor, defined], [A constructor, A constructor is typically used to intialize data members], [A constructor, globally], [A constructor, A constructor], [A constructor, to intialize data members], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, Functions], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, maybe], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, Functions], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, to allocate resources typically], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, to allocate resources], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, instance memory], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, files], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, globally], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, to intialize data members typically], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, to allocate resources for instance memory], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, files], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, etc Also a constructor can not return values], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, maybe], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, defined], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, to intialize data members for instance memory], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, defined], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, globally], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, to intialize data members], [functions, Functions], [functions, A constructor is typically used to intialize data members], [functions, A constructor is typically used to intialize data members], [functions, maybe], [functions, Functions], [functions, allocate resources for instance memory operations], [functions, A constructor], [functions, to allocate resources typically], [functions, A constructor], [functions, to allocate resources], [functions, instance memory], [functions, files], [functions, allocate resources for instance memory operations], [functions, globally], [functions, A constructor], [functions, to intialize data members typically], [functions, A constructor], [functions, to allocate resources for instance memory], [functions, files], [functions, etc Also a constructor can not return values], [functions, allocate resources for instance memory operations], [functions, maybe], [functions, allocate resources for instance memory operations], [functions, defined], [functions, A constructor], [functions, to intialize data members for instance memory], [functions, A constructor is typically used to intialize data members], [functions, defined], [functions, A constructor is typically used to intialize data members], [functions, globally], [functions, A constructor], [functions, to intialize data members], [to indicate a return type, Functions], [to indicate a return type, A constructor is typically used to intialize data members], [to indicate a return type, A constructor is typically used to intialize data members], [to indicate a return type, maybe], [to indicate a return type, Functions], [to indicate a return type, allocate resources for instance memory operations], [to indicate a return type, A constructor], [to indicate a return type, to allocate resources typically], [to indicate a return type, A constructor], [to indicate a return type, to allocate resources], [to indicate a return type, instance memory], [to indicate a return type, files], [to indicate a return type, allocate resources for instance memory operations], [to indicate a return type, globally], [to indicate a return type, A constructor], [to indicate a return type, to intialize data members typically], [to indicate a return type, A constructor], [to indicate a return type, to allocate resources for instance memory], [to indicate a return type, files], [to indicate a return type, etc Also a constructor can not return values], [to indicate a return type, allocate resources for instance memory operations], [to indicate a return type, maybe], [to indicate a return type, allocate resources for instance memory operations], [to indicate a return type, defined], [to indicate a return type, A constructor], [to indicate a return type, to intialize data members for instance memory], [to indicate a return type, A constructor is typically used to intialize data members], [to indicate a return type, defined], [to indicate a return type, A constructor is typically used to intialize data members], [to indicate a return type, globally], [to indicate a return type, A constructor], [to indicate a return type, to intialize data members], [an object, Functions], [an object, A constructor is typically used to intialize data members], [an object, A constructor is typically used to intialize data members], [an object, maybe], [an object, Functions], [an object, allocate resources for instance memory operations], [an object, A constructor], [an object, to allocate resources typically], [an object, A constructor], [an object, to allocate resources], [an object, instance memory], [an object, files], [an object, allocate resources for instance memory operations], [an object, globally], [an object, A constructor], [an object, to intialize data members typically], [an object, A constructor], [an object, to allocate resources for instance memory], [an object, files], [an object, etc Also a constructor can not return values], [an object, allocate resources for instance memory operations], [an object, maybe], [an object, allocate resources for instance memory operations], [an object, defined], [an object, A constructor], [an object, to intialize data members for instance memory], [an object, A constructor is typically used to intialize data members], [an object, defined], [an object, A constructor is typically used to intialize data members], [an object, globally], [an object, A constructor], [an object, to intialize data members], [whereas a function needs to be called explicitly Constructors do not have return type, Functions], [whereas a function needs to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [whereas a function needs to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [whereas a function needs to be called explicitly Constructors do not have return type, maybe], [whereas a function needs to be called explicitly Constructors do not have return type, Functions], [whereas a function needs to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type, to allocate resources typically], [whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type, to allocate resources], [whereas a function needs to be called explicitly Constructors do not have return type, instance memory], [whereas a function needs to be called explicitly Constructors do not have return type, files], [whereas a function needs to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [whereas a function needs to be called explicitly Constructors do not have return type, globally], [whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type, to intialize data members typically], [whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type, to allocate resources for instance memory], [whereas a function needs to be called explicitly Constructors do not have return type, files], [whereas a function needs to be called explicitly Constructors do not have return type, etc Also a constructor can not return values], [whereas a function needs to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [whereas a function needs to be called explicitly Constructors do not have return type, maybe], [whereas a function needs to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [whereas a function needs to be called explicitly Constructors do not have return type, defined], [whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type, to intialize data members for instance memory], [whereas a function needs to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [whereas a function needs to be called explicitly Constructors do not have return type, defined], [whereas a function needs to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [whereas a function needs to be called explicitly Constructors do not have return type, globally], [whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type, to intialize data members], [an object, Functions], [an object, A constructor is typically used to intialize data members], [an object, A constructor is typically used to intialize data members], [an object, maybe], [an object, Functions], [an object, allocate resources for instance memory operations], [an object, A constructor], [an object, to allocate resources typically], [an object, A constructor], [an object, to allocate resources], [an object, instance memory], [an object, files], [an object, allocate resources for instance memory operations], [an object, globally], [an object, A constructor], [an object, to intialize data members typically], [an object, A constructor], [an object, to allocate resources for instance memory], [an object, files], [an object, etc Also a constructor can not return values], [an object, allocate resources for instance memory operations], [an object, maybe], [an object, allocate resources for instance memory operations], [an object, defined], [an object, A constructor], [an object, to intialize data members for instance memory], [an object, A constructor is typically used to intialize data members], [an object, defined], [an object, A constructor is typically used to intialize data members], [an object, globally], [an object, A constructor], [an object, to intialize data members], [whereas a function needs to be called explicitly Constructors do not have return type whenever, Functions], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A constructor is typically used to intialize data members], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A constructor is typically used to intialize data members], [whereas a function needs to be called explicitly Constructors do not have return type whenever, maybe], [whereas a function needs to be called explicitly Constructors do not have return type whenever, Functions], [whereas a function needs to be called explicitly Constructors do not have return type whenever, allocate resources for instance memory operations], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type whenever, to allocate resources typically], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type whenever, to allocate resources], [whereas a function needs to be called explicitly Constructors do not have return type whenever, instance memory], [whereas a function needs to be called explicitly Constructors do not have return type whenever, files], [whereas a function needs to be called explicitly Constructors do not have return type whenever, allocate resources for instance memory operations], [whereas a function needs to be called explicitly Constructors do not have return type whenever, globally], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type whenever, to intialize data members typically], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type whenever, to allocate resources for instance memory], [whereas a function needs to be called explicitly Constructors do not have return type whenever, files], [whereas a function needs to be called explicitly Constructors do not have return type whenever, etc Also a constructor can not return values], [whereas a function needs to be called explicitly Constructors do not have return type whenever, allocate resources for instance memory operations], [whereas a function needs to be called explicitly Constructors do not have return type whenever, maybe], [whereas a function needs to be called explicitly Constructors do not have return type whenever, allocate resources for instance memory operations], [whereas a function needs to be called explicitly Constructors do not have return type whenever, defined], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type whenever, to intialize data members for instance memory], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A constructor is typically used to intialize data members], [whereas a function needs to be called explicitly Constructors do not have return type whenever, defined], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A constructor is typically used to intialize data members], [whereas a function needs to be called explicitly Constructors do not have return type whenever, globally], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type whenever, to intialize data members], [a function, Functions], [a function, A constructor is typically used to intialize data members], [a function, A constructor is typically used to intialize data members], [a function, maybe], [a function, Functions], [a function, allocate resources for instance memory operations], [a function, A constructor], [a function, to allocate resources typically], [a function, A constructor], [a function, to allocate resources], [a function, instance memory], [a function, files], [a function, allocate resources for instance memory operations], [a function, globally], [a function, A constructor], [a function, to intialize data members typically], [a function, A constructor], [a function, to allocate resources for instance memory], [a function, files], [a function, etc Also a constructor can not return values], [a function, allocate resources for instance memory operations], [a function, maybe], [a function, allocate resources for instance memory operations], [a function, defined], [a function, A constructor], [a function, to intialize data members for instance memory], [a function, A constructor is typically used to intialize data members], [a function, defined], [a function, A constructor is typically used to intialize data members], [a function, globally], [a function, A constructor], [a function, to intialize data members], [to be called explicitly Constructors do not have return type, Functions], [to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [to be called explicitly Constructors do not have return type, maybe], [to be called explicitly Constructors do not have return type, Functions], [to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [to be called explicitly Constructors do not have return type, A constructor], [to be called explicitly Constructors do not have return type, to allocate resources typically], [to be called explicitly Constructors do not have return type, A constructor], [to be called explicitly Constructors do not have return type, to allocate resources], [to be called explicitly Constructors do not have return type, instance memory], [to be called explicitly Constructors do not have return type, files], [to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [to be called explicitly Constructors do not have return type, globally], [to be called explicitly Constructors do not have return type, A constructor], [to be called explicitly Constructors do not have return type, to intialize data members typically], [to be called explicitly Constructors do not have return type, A constructor], [to be called explicitly Constructors do not have return type, to allocate resources for instance memory], [to be called explicitly Constructors do not have return type, files], [to be called explicitly Constructors do not have return type, etc Also a constructor can not return values], [to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [to be called explicitly Constructors do not have return type, maybe], [to be called explicitly Constructors do not have return type, allocate resources for instance memory operations], [to be called explicitly Constructors do not have return type, defined], [to be called explicitly Constructors do not have return type, A constructor], [to be called explicitly Constructors do not have return type, to intialize data members for instance memory], [to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [to be called explicitly Constructors do not have return type, defined], [to be called explicitly Constructors do not have return type, A constructor is typically used to intialize data members], [to be called explicitly Constructors do not have return type, globally], [to be called explicitly Constructors do not have return type, A constructor], [to be called explicitly Constructors do not have return type, to intialize data members], [explicitly Constructors, Functions], [explicitly Constructors, A constructor is typically used to intialize data members], [explicitly Constructors, A constructor is typically used to intialize data members], [explicitly Constructors, maybe], [explicitly Constructors, Functions], [explicitly Constructors, allocate resources for instance memory operations], [explicitly Constructors, A constructor], [explicitly Constructors, to allocate resources typically], [explicitly Constructors, A constructor], [explicitly Constructors, to allocate resources], [explicitly Constructors, instance memory], [explicitly Constructors, files], [explicitly Constructors, allocate resources for instance memory operations], [explicitly Constructors, globally], [explicitly Constructors, A constructor], [explicitly Constructors, to intialize data members typically], [explicitly Constructors, A constructor], [explicitly Constructors, to allocate resources for instance memory], [explicitly Constructors, files], [explicitly Constructors, etc Also a constructor can not return values], [explicitly Constructors, allocate resources for instance memory operations], [explicitly Constructors, maybe], [explicitly Constructors, allocate resources for instance memory operations], [explicitly Constructors, defined], [explicitly Constructors, A constructor], [explicitly Constructors, to intialize data members for instance memory], [explicitly Constructors, A constructor is typically used to intialize data members], [explicitly Constructors, defined], [explicitly Constructors, A constructor is typically used to intialize data members], [explicitly Constructors, globally], [explicitly Constructors, A constructor], [explicitly Constructors, to intialize data members], [return type, Functions], [return type, A constructor is typically used to intialize data members], [return type, A constructor is typically used to intialize data members], [return type, maybe], [return type, Functions], [return type, allocate resources for instance memory operations], [return type, A constructor], [return type, to allocate resources typically], [return type, A constructor], [return type, to allocate resources], [return type, instance memory], [return type, files], [return type, allocate resources for instance memory operations], [return type, globally], [return type, A constructor], [return type, to intialize data members typically], [return type, A constructor], [return type, to allocate resources for instance memory], [return type, files], [return type, etc Also a constructor can not return values], [return type, allocate resources for instance memory operations], [return type, maybe], [return type, allocate resources for instance memory operations], [return type, defined], [return type, A constructor], [return type, to intialize data members for instance memory], [return type, A constructor is typically used to intialize data members], [return type, defined], [return type, A constructor is typically used to intialize data members], [return type, globally], [return type, A constructor], [return type, to intialize data members]]"



#inputs = "[[a function, A function of a class], [a function, a task], [a function, A function of a class], [a function, a task such as display a line of text or do some kind of mathematical operations], [a function, A constructor], [a function, an object or objects of a class], [to be called explicitly Constructors do not have return type, A function of a class], [to be called explicitly Constructors do not have return type, a task], [to be called explicitly Constructors do not have return type, A function of a class], [to be called explicitly Constructors do not have return type, a task such as display a line of text or do some kind of mathematical operations], [to be called explicitly Constructors do not have return type, A constructor], [to be called explicitly Constructors do not have return type, an object or objects of a class], [A constructor, A function of a class], [A constructor, a task], [A constructor, A function of a class], [A constructor, a task such as display a line of text or do some kind of mathematical operations], [A constructor, A constructor], [A constructor, an object or objects of a class], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A function of a class], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a task], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A function of a class], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, a task such as display a line of text or do some kind of mathematical operations], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whenever an object is created whereas a function needs to be called explicitly Constructors do not have return type, an object or objects of a class], [functions, A function of a class], [functions, a task], [functions, A function of a class], [functions, a task such as display a line of text or do some kind of mathematical operations], [functions, A constructor], [functions, an object or objects of a class], [to indicate a return type, A function of a class], [to indicate a return type, a task], [to indicate a return type, A function of a class], [to indicate a return type, a task such as display a line of text or do some kind of mathematical operations], [to indicate a return type, A constructor], [to indicate a return type, an object or objects of a class], [explicitly Constructors, A function of a class], [explicitly Constructors, a task], [explicitly Constructors, A function of a class], [explicitly Constructors, a task such as display a line of text or do some kind of mathematical operations], [explicitly Constructors, A constructor], [explicitly Constructors, an object or objects of a class], [return type, A function of a class], [return type, a task], [return type, A function of a class], [return type, a task such as display a line of text or do some kind of mathematical operations], [return type, A constructor], [return type, an object or objects of a class], [an object, A function of a class], [an object, a task], [an object, A function of a class], [an object, a task such as display a line of text or do some kind of mathematical operations], [an object, A constructor], [an object, an object or objects of a class], [whereas a function needs to be called explicitly Constructors do not have return type, A function of a class], [whereas a function needs to be called explicitly Constructors do not have return type, a task], [whereas a function needs to be called explicitly Constructors do not have return type, A function of a class], [whereas a function needs to be called explicitly Constructors do not have return type, a task such as display a line of text or do some kind of mathematical operations], [whereas a function needs to be called explicitly Constructors do not have return type, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type, an object or objects of a class], [an object, A function of a class], [an object, a task], [an object, A function of a class], [an object, a task such as display a line of text or do some kind of mathematical operations], [an object, A constructor], [an object, an object or objects of a class], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A function of a class], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a task], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A function of a class], [whereas a function needs to be called explicitly Constructors do not have return type whenever, a task such as display a line of text or do some kind of mathematical operations], [whereas a function needs to be called explicitly Constructors do not have return type whenever, A constructor], [whereas a function needs to be called explicitly Constructors do not have return type whenever, an object or objects of a class]]"



#inputs = "[[The groups, their], [The groups, balances], [The groups, The groups], [The groups, their balances], [a standard unit of mass, their], [a standard unit of mass, balances], [a standard unit of mass, The groups], [a standard unit of mass, their balances], [The groups, their], [The groups, balances], [The groups, The groups], [The groups, their balances], [a standard unit of mass like grams, their], [a standard unit of mass like grams, balances], [a standard unit of mass like grams, The groups], [a standard unit of mass like grams, their balances]]"


#inputs = "[[A person, one], [A person, lower which], [the size of the grease spots, one], [the size of the grease spots, lower which], [The sample with the larger grease spot, one], [The sample with the larger grease spot, lower which], [more, one], [more, lower which]]"


#inputs = "[[Anna, one], [Anna, lower which], [the size of the grease spots, one], [the size of the grease spots, lower which], [The sample with the larger grease spot, one], [The sample with the larger grease spot, lower which], [more, one], [more, lower which]]"


#inputs = "[[the string, the Longer], [the string, the string The shorter is the string], [the string, The shorter], [the string, the string], [the string, the higher], [the string, the pitch the string], [the string, the lower], [the string, the pitch The shorter is the string the string], [longer, the Longer], [longer, the string The shorter is the string], [longer, The shorter], [longer, the string], [longer, the higher], [longer, the pitch the string], [longer, the lower], [longer, the pitch The shorter is the string the string], [the string, the Longer], [the string, the string The shorter is the string], [the string, The shorter], [the string, the string], [the string, the higher], [the string, the pitch the string], [the string, the lower], [the string, the pitch The shorter is the string the string], [shorter, the Longer], [shorter, the string The shorter is the string], [shorter, The shorter], [shorter, the string], [shorter, the higher], [shorter, the pitch the string], [shorter, the lower], [shorter, the pitch The shorter is the string the string], [the pitch, the Longer], [the pitch, the string The shorter is the string], [the pitch, The shorter], [the pitch, the string], [the pitch, the higher], [the pitch, the pitch the string], [the pitch, the lower], [the pitch, the pitch The shorter is the string the string], [lower, the Longer], [lower, the string The shorter is the string], [lower, The shorter], [lower, the string], [lower, the higher], [lower, the pitch the string], [lower, the lower], [lower, the pitch The shorter is the string the string], [the pitch, the Longer], [the pitch, the string The shorter is the string], [the pitch, The shorter], [the pitch, the string], [the pitch, the higher], [the pitch, the pitch the string], [the pitch, the lower], [the pitch, the pitch The shorter is the string the string], [lower If the string is longer, the Longer], [lower If the string is longer, the string The shorter is the string], [lower If the string is longer, The shorter], [lower If the string is longer, the string], [lower If the string is longer, the higher], [lower If the string is longer, the pitch the string], [lower If the string is longer, the lower], [lower If the string is longer, the pitch The shorter is the string the string], [the pitch, the Longer], [the pitch, the string The shorter is the string], [the pitch, The shorter], [the pitch, the string], [the pitch, the higher], [the pitch, the pitch the string], [the pitch, the lower], [the pitch, the pitch The shorter is the string the string], [higher, the Longer], [higher, the string The shorter is the string], [higher, The shorter], [higher, the string], [higher, the higher], [higher, the pitch the string], [higher, the lower], [higher, the pitch The shorter is the string the string], [the pitch, the Longer], [the pitch, the string The shorter is the string], [the pitch, The shorter], [the pitch, the string], [the pitch, the higher], [the pitch, the pitch the string], [the pitch, the lower], [the pitch, the pitch The shorter is the string the string], [lower If the string is shorter, the Longer], [lower If the string is shorter, the string The shorter is the string], [lower If the string is shorter, The shorter], [lower If the string is shorter, the string], [lower If the string is shorter, the higher], [lower If the string is shorter, the pitch the string], [lower If the string is shorter, the lower], [lower If the string is shorter, the pitch The shorter is the string the string]]"


#inputs = "[[Georgia, Georgia], [Georgia, the minerals for hardness], [Georgia, Georgia], [Georgia, the minerals for hardness by rubbing the minerals together], [the minerals for hardness, Georgia], [the minerals for hardness, the minerals for hardness], [the minerals for hardness, Georgia], [the minerals for hardness, the minerals for hardness by rubbing the minerals together], [Georgia, Georgia], [Georgia, the minerals for hardness], [Georgia, Georgia], [Georgia, the minerals for hardness by rubbing the minerals together], [the minerals for hardness by rubbing the minerals together, Georgia], [the minerals for hardness by rubbing the minerals together, the minerals for hardness], [the minerals for hardness by rubbing the minerals together, Georgia], [the minerals for hardness by rubbing the minerals together, the minerals for hardness by rubbing the minerals together], [Georgia, Georgia], [Georgia, the minerals for hardness], [Georgia, Georgia], [Georgia, the minerals for hardness by rubbing the minerals together], [which one scratches the other, Georgia], [which one scratches the other, the minerals for hardness], [which one scratches the other, Georgia], [which one scratches the other, the minerals for hardness by rubbing the minerals together], [one, Georgia], [one, the minerals for hardness], [one, Georgia], [one, the minerals for hardness by rubbing the minerals together], [which the other, Georgia], [which the other, the minerals for hardness], [which the other, Georgia], [which the other, the minerals for hardness by rubbing the minerals together]]"

#inputs = "[[A person, A person], [A person, the minerals for hardness by rubbing the minerals together], [A person, A person], [A person, the minerals for hardness], [the minerals for hardness by rubbing the minerals together, A person], [the minerals for hardness by rubbing the minerals together, the minerals for hardness by rubbing the minerals together], [the minerals for hardness by rubbing the minerals together, A person], [the minerals for hardness by rubbing the minerals together, the minerals for hardness], [A person, A person], [A person, the minerals for hardness by rubbing the minerals together], [A person, A person], [A person, the minerals for hardness], [which one scratches the other, A person], [which one scratches the other, the minerals for hardness by rubbing the minerals together], [which one scratches the other, A person], [which one scratches the other, the minerals for hardness], [one, A person], [one, the minerals for hardness by rubbing the minerals together], [one, A person], [one, the minerals for hardness], [which the other, A person], [which the other, the minerals for hardness by rubbing the minerals together], [which the other, A person], [which the other, the minerals for hardness], [A person, A person], [A person, the minerals for hardness by rubbing the minerals together], [A person, A person], [A person, the minerals for hardness], [the minerals for hardness, A person], [the minerals for hardness, the minerals for hardness by rubbing the minerals together], [the minerals for hardness, A person], [the minerals for hardness, the minerals for hardness]]"


#inputs = "[[member functions, the data], [member functions, in a class definition], [member functions, methods], [member functions, in a class definition], [attributes, the data], [attributes, in a class definition], [attributes, methods], [attributes, in a class definition], [Data members, the data], [Data members, in a class definition], [Data members, methods], [Data members, in a class definition], [in a class definition, the data], [in a class definition, in a class definition], [in a class definition, methods], [in a class definition, in a class definition], [member functions, the data], [member functions, in a class definition], [member functions, methods], [member functions, in a class definition], [in a class definition typically, the data], [in a class definition typically, in a class definition], [in a class definition typically, methods], [in a class definition typically, in a class definition], [Data members, the data], [Data members, in a class definition], [Data members, methods], [Data members, in a class definition], [attributes, the data], [attributes, in a class definition], [attributes, methods], [attributes, in a class definition], [member functions, the data], [member functions, in a class definition], [member functions, methods], [member functions, in a class definition], [in a class definition, the data], [in a class definition, in a class definition], [in a class definition, methods], [in a class definition, in a class definition], [Data members, the data], [Data members, in a class definition], [Data members, methods], [Data members, in a class definition], [in a class definition typically, the data], [in a class definition typically, in a class definition], [in a class definition typically, methods], [in a class definition typically, in a class definition]]"




#inputs = "[[the queue, in dequeue item], [the queue, from the front of the queue], [the queue, Enqueue inserts item at the back of the queue], [the queue, from the front of the queue], [item from the queue, in dequeue item], [item from the queue, from the front of the queue], [item from the queue, Enqueue inserts item at the back of the queue], [item from the queue, from the front of the queue], [The two main functions defined by a queue, in dequeue item], [The two main functions defined by a queue, from the front of the queue], [The two main functions defined by a queue, Enqueue inserts item at the back of the queue], [The two main functions defined by a queue, from the front of the queue], [enqueue that adds item to the queue, in dequeue item], [enqueue that adds item to the queue, from the front of the queue], [enqueue that adds item to the queue, Enqueue inserts item at the back of the queue], [enqueue that adds item to the queue, from the front of the queue], [that, in dequeue item], [that, from the front of the queue], [that, Enqueue inserts item at the back of the queue], [that, from the front of the queue], [item, in dequeue item], [item, from the front of the queue], [item, Enqueue inserts item at the back of the queue], [item, from the front of the queue], [The two main functions defined by a queue, in dequeue item], [The two main functions defined by a queue, from the front of the queue], [The two main functions defined by a queue, Enqueue inserts item at the back of the queue], [The two main functions defined by a queue, from the front of the queue], [dequeue, in dequeue item], [dequeue, from the front of the queue], [dequeue, Enqueue inserts item at the back of the queue], [dequeue, from the front of the queue], [dequeue, in dequeue item], [dequeue, from the front of the queue], [dequeue, Enqueue inserts item at the back of the queue], [dequeue, from the front of the queue], [item from the queue, in dequeue item], [item from the queue, from the front of the queue], [item from the queue, Enqueue inserts item at the back of the queue], [item from the queue, from the front of the queue], [the queue, in dequeue item], [the queue, from the front of the queue], [the queue, Enqueue inserts item at the back of the queue], [the queue, from the front of the queue], [item, in dequeue item], [item, from the front of the queue], [item, Enqueue inserts item at the back of the queue], [item, from the front of the queue], [that, in dequeue item], [that, from the front of the queue], [that, Enqueue inserts item at the back of the queue], [that, from the front of the queue], [dequeue, in dequeue item], [dequeue, from the front of the queue], [dequeue, Enqueue inserts item at the back of the queue], [dequeue, from the front of the queue], [The two main functions, in dequeue item], [The two main functions, from the front of the queue], [The two main functions, Enqueue inserts item at the back of the queue], [The two main functions, from the front of the queue], [by a queue, in dequeue item], [by a queue, from the front of the queue], [by a queue, Enqueue inserts item at the back of the queue], [by a queue, from the front of the queue], [dequeue, in dequeue item], [dequeue, from the front of the queue], [dequeue, Enqueue inserts item at the back of the queue], [dequeue, from the front of the queue], [item, in dequeue item], [item, from the front of the queue], [item, Enqueue inserts item at the back of the queue], [item, from the front of the queue], [that, in dequeue item], [that, from the front of the queue], [that, Enqueue inserts item at the back of the queue], [that, from the front of the queue], [item to the queue, in dequeue item], [item to the queue, from the front of the queue], [item to the queue, Enqueue inserts item at the back of the queue], [item to the queue, from the front of the queue]]"


#inputs = "[[member functions, several data members and at least one public data member or method], [member functions, in a class definition], [member functions, a constructor], [member functions, in a class definition], [attributes, several data members and at least one public data member or method], [attributes, in a class definition], [attributes, a constructor], [attributes, in a class definition], [Data members, several data members and at least one public data member or method], [Data members, in a class definition], [Data members, a constructor], [Data members, in a class definition], [in a class definition, several data members and at least one public data member or method], [in a class definition, in a class definition], [in a class definition, a constructor], [in a class definition, in a class definition], [member functions, several data members and at least one public data member or method], [member functions, in a class definition], [member functions, a constructor], [member functions, in a class definition], [in a class definition typically, several data members and at least one public data member or method], [in a class definition typically, in a class definition], [in a class definition typically, a constructor], [in a class definition typically, in a class definition], [Data members, several data members and at least one public data member or method], [Data members, in a class definition], [Data members, a constructor], [Data members, in a class definition], [attributes, several data members and at least one public data member or method], [attributes, in a class definition], [attributes, a constructor], [attributes, in a class definition], [member functions, several data members and at least one public data member or method], [member functions, in a class definition], [member functions, a constructor], [member functions, in a class definition], [in a class definition, several data members and at least one public data member or method], [in a class definition, in a class definition], [in a class definition, a constructor], [in a class definition, in a class definition], [Data members, several data members and at least one public data member or method], [Data members, in a class definition], [Data members, a constructor], [Data members, in a class definition], [in a class definition typically, several data members and at least one public data member or method], [in a class definition typically, in a class definition], [in a class definition typically, a constructor], [in a class definition typically, in a class definition]]"










#inputs = "[[The two main functions, The two main functions], [The two main functions, enqueue which inserts an item at the back of the queue], [The two main functions, The two main functions], [The two main functions, dequeue which removes an item from the front of the queue], [by a queue, The two main functions], [by a queue, enqueue which inserts an item at the back of the queue], [by a queue, The two main functions], [by a queue, dequeue which removes an item from the front of the queue], [The two main functions defined by a queue, The two main functions], [The two main functions defined by a queue, enqueue which inserts an item at the back of the queue], [The two main functions defined by a queue, The two main functions], [The two main functions defined by a queue, dequeue which removes an item from the front of the queue], [enqueue and dequeue, The two main functions], [enqueue and dequeue, enqueue which inserts an item at the back of the queue], [enqueue and dequeue, The two main functions], [enqueue and dequeue, dequeue which removes an item from the front of the queue]]"


#inputs = "[['data members', 'member functions'], ['data type', 'variable'], ['Data members and member functions', 'A constructor functions and variables']]"

#print aa


#inputs = "[[Data members, The data], [Data members, in a class definition], [Data members, methods], [Data members, in a class definition], [attributes, The data], [attributes, in a class definition], [attributes, methods], [attributes, in a class definition], [member functions, The data], [member functions, in a class definition], [member functions, methods], [member functions, in a class definition], [in a class definition, The data], [in a class definition, in a class definition], [in a class definition, methods], [in a class definition, in a class definition], [member functions, The data], [member functions, in a class definition], [member functions, methods], [member functions, in a class definition], [attributes, The data], [attributes, in a class definition], [attributes, methods], [attributes, in a class definition], [Data members, The data], [Data members, in a class definition], [Data members, methods], [Data members, in a class definition], [in a class definition, The data], [in a class definition, in a class definition], [in a class definition, methods], [in a class definition, in a class definition]]"


"""
aaa = list(aa)

a = str(aaa)
"""

input1 = inputs.split("], ")

output1 = []
for i in range(len(input1)):
    a = input1[i]
    a = a.replace("[", "")
    a = a.replace("]", "")
    a = a.replace(" '", "")
    a = a.replace("'", "")

    #print a
    b = a.split(",")
    #print b
    output1.append(b)

#print output1   

a = str(output1)

#print a

#a = str([["Data members and member functions", "variables"], ["Data members and member functions", "accessible to by that class and possibly other classes"], ["Data members and member functions", "variables"], ["Data members and member functions", "accessible depending on how by are done"], ["Data members and member functions", "variables"], ["Data members and member functions", "accessible"], ["Data members and member functions", "A constructor functions and variables"], ["Data members and member functions", "in a class definition"], ["attributes", "variables"], ["attributes", "accessible to by that class and possibly other classes"], ["attributes", "variables"], ["attributes", "accessible depending on how by are done"], ["attributes", "variables"], ["attributes", "accessible"], ["attributes", "A constructor functions and variables"], ["attributes", "in a class definition"], ["Data members and member functions", "variables"], ["Data members and member functions", "accessible to by that class and possibly other classes"], ["Data members and member functions", "variables"], ["Data members and member functions", "accessible depending on how by are done"], ["Data members and member functions", "variables"], ["Data members and member functions", "accessible"], ["Data members and member functions", "A constructor functions and variables"], ["Data members and member functions", "in a class definition"], ["in a class definition typically", "variables"], ["in a class definition typically", "accessible to by that class and possibly other classes"], ["in a class definition typically", "variables"], ["in a class definition typically", "accessible depending on how by are done"], ["in a class definition typically", "variables"], ["in a class definition typically", "accessible"], ["in a class definition typically", "A constructor functions and variables"], ["in a class definition typically", "in a class definition"], ["Data members and member functions", "variables"], ["Data members and member functions", "accessible to by that class and possibly other classes"], ["Data members and member functions", "variables"], ["Data members and member functions", "accessible depending on how by are done"], ["Data members and member functions", "variables"], ["Data members and member functions", "accessible"], ["Data members and member functions", "A constructor functions and variables"], ["Data members and member functions", "in a class definition"], ["in a class definition", "variables"], ["in a class definition", "accessible to by that class and possibly other classes"], ["in a class definition", "variables"], ["in a class definition", "accessible depending on how by are done"], ["in a class definition", "variables"], ["in a class definition", "accessible"], ["in a class definition", "A constructor functions and variables"], ["in a class definition", "in a class definition"]])


#print a

#aa = "0.5, 0.2, 0.3"

#print aa


#a = "[['Data members and member functions', 'variables'], ['Data members and member functions', 'accessible to by that class and possibly other classes'], ['Data members and member functions', 'variables']]"

b = ast.literal_eval(a)

"""
b = [['The two main functions', 'The two main functions'], ['The two main functions', 'enqueue which inserts an item at the back of the queue'], ['The two main functions', 'The two main functions'], ['The two main functions', 'dequeue which removes an item from the front of the queue']]

print b

aa = []
for i in b:
    i = ['The two main functions', 'enqueue which inserts an item at the back of the queue']
    bb = []
    for j in i:
        j1 = j.split(" ")
        for x in j1:
            if d.check(x) == False and if d1.check(x) == False:
               bb.append(x)
        else:
            
           

    sim = similar(bb[0], bb[1])
    aa.append(sim)

print aa

"""



#print b

#print b

#print b[0]

#print type(b[0][0])

#input = "[2,3,4,5]"
#>>> map(float, input.strip('[]').split(','))
#[2.0, 3.0, 4.0, 5.0]

#aa = map(str, a.strip('[]').split(','))

#print aa

#wv = sys.argv[3]

#print a
#print b
#print wv

#print b

st = POS_Tag(model_filename='/home/archana/ve/stanford-postagger-2018-10-16/models/english-bidirectional-distsim.tagger', path_to_jar='/home/archana/ve/stanford-postagger-2018-10-16/stanford-postagger.jar')
word_vectors = KeyedVectors.load_word2vec_format('/home/archana/wiki/pretrained_wiki_model/3/enwiki_5_ner.txt', binary=False)

simi_result = []

for iter1 in range(len(b)):
    aa = b[iter1][0] 
    bb = b[iter1][1]

    #print aa
    #print bb

    pos1 = nltk.pos_tag(word_tokenize(aa))
    pos2 = nltk.pos_tag(word_tokenize(bb))

#print pos1
#print pos2

    #print pos1
    #print pos2

   

    """pos1 = st.tag(aa.split())
    pos2 = st.tag(bb.split())"""

    #print pos1
    #print pos2

    #pos1 = [('enqueue', 'NN'), ('and', 'CC'), ('dequeue', 'NN')]
    #pos2 = [('The', 'DT'), ('two', 'CD'), ('main', 'JJ'), ('functions', 'NNS')]

    arr1 = []
    for p in pos1:
    #print p[1]
        #print p
        pp = p[1][0:2]

        #print pp
    #print pp
        px = p[0].lower()

        #print px

        if px not in stopset: 
           if pp == "NN":
       #arr1.append(p[0].lower() + "_" + "NOUN")

              #print px
       
              if px == "one" or px == "ones":
                 pos_new = "NUM"
                 arr1.append("one" + "_" + "NUM")

              elif px == "uses":
                   pos_new = "VERB"
                   arr1.append("use" + "_" + "VERB")

              elif px == "whacking":
                   pos_new = "VERB"
                   arr1.append("whack" + "_" + "VERB")
              elif px == "warmness":
                   pos_new = "NOUN"
                   arr1.append("warmth" + "_" + "NOUN")    
                                   
              else:
                   #print px
                   clmw = wordnet_lemmatizer.lemmatize(px)
                   #print clmw
                   clmw1 = wn.morphy(clmw)
                   #print clmw1

                   if clmw1 == None:
                     clmw1 = clmw
                     #print clmw1
                     #print d.check(clmw1)
                     #print d1.check(clmw1)
                     if d.check(clmw1) == True:
                        arr1.append(clmw1 + "_" + "NOUN")

                     elif d1.check(clmw1) == True:
                        arr1.append(clmw1 + "_" + "NOUN")
                   else:
                     clmw1 = clmw1
                     #print clmw1
                     #print d.check(clmw1)
                     #print d1.check(clmw1) 
                     if d.check(clmw1) == True:
                        arr1.append(clmw1 + "_" + "NOUN")

                     elif d1.check(clmw1) == True:
                        arr1.append(clmw1 + "_" + "NOUN")

                     else:
                        arr1.append(clmw1)
                        

                   #if d.check(clmw1) == True:
                   #   arr1.append(clmw1 + "_" + "NOUN")

                   #print arr1




           if pp == "JJ":
       #arr1.append(p[0] + "_" + "ADJ")
              #print px
              if px == "one" or px == "ones":
                 pos_new = "NUM"
                 arr1.append("one" + "_" + "NUM")

              elif px == "saturated":
                       #pos_new = "NOUN"
                   arr1.append("saturate" + "_" + "VERB")

              else:

                  clmw = wordnet_lemmatizer.lemmatize(px)
                  clmw1 = wn.morphy(clmw)

                  if clmw1 == None:
                     clmw1 = clmw
                     if d.check(clmw1) == True:
                        arr1.append(clmw1 + "_" + "ADJ")
                  else:
                     clmw1 = clmw1
                     if d.check(clmw1) == True:
                        arr1.append(clmw1 + "_" + "ADJ")


                  #if d.check(clmw1) == True:
                  #   arr1.append(clmw1 + "_" + "ADJ") 
                  #else:
                  #   arr1.append(px + "_" + "ADJ")                      





       
           if pp == "VB":
       #arr1.append(p[0] + "_" + "VERB")
              if px == "pass":
                 arr1.append("pass" + "_" + "VERB")

              elif px == "fed":
                   arr1.append("feed" + "_"+"VERB")
              elif px == "colored":
                   arr1.append("color" + "_" + "NOUN")
              elif px == "done":
                   arr1.append("")

              elif px == "data":
                   arr1.append("data" + "_" + "NOUN")
              else:

                   clmw = wordnet_lemmatizer.lemmatize(px)
                   clmw1 = wn.morphy(clmw)
                   if d.check(clmw1) == True:
                    
                      try:

                         clmw2 = en.verb.present(clmw1) 
                          #print clmw2

                         clmw3 = wn.morphy(clmw2)                    
                         arr1.append(clmw3 + "_" +"VERB")


                       #v1 = en.verb.present(clmw1)
                       #str_s1.append(v1 + "_" +"VERB")
                      except KeyError:
                         arr1.append(clmw1 + "_"+"VERB")            


       

           if pp == "RB":
       #arr1.append(p[0] + "_" + "ADV")
              if px == "farthest":
                 pos_new = "ADV"
                 arr1.append("farther" + "_" + "ADV")

              if px == "add":
                 arr1.append("add" + "_" + "VERB")
              else:

                 clmw = wordnet_lemmatizer.lemmatize(px)
                 clmw1 = wn.morphy(clmw)
                 if d.check(clmw1) == True:
                    arr1.append(clmw1 + "_" + "ADV")    




#print arr1




    arr2 = []
    for p in pos2:
    #print p[1]

        #print p

        pp = p[1][0:2]
    #print pp
        py = p[0].lower()
        #print py
        if py not in stopset: 
           if pp == "NN":
       #arr1.append(p[0].lower() + "_" + "NOUN")
       
              if py == "one" or py == "ones":
                 pos_new = "NUM"
                 arr2.append("one" + "_" + "NUM")

              elif py == "uses":
                   pos_new = "VERB"
                   arr2.append("use" + "_" + "VERB")

              elif py == "whacking":
                   pos_new = "VERB"
                   arr2.append("whack" + "_" + "VERB")
              elif py == "warmness":
                   pos_new = "NOUN"
                   arr2.append("warmth" + "_" + "NOUN")   
              #elif py == "done":
              #     arr2.append("does" + "_" + "VERB")
             
                  
              else:

                  #print py
                  clmw = wordnet_lemmatizer.lemmatize(py)
                  #print clmw

                  clmw1 = wn.morphy(clmw)
                  #print clmw1
                  #clmw1 = "enqueue"
                  if clmw1 == None:
                     clmw1 = clmw
                     if d.check(clmw1) == True:
                        arr2.append(clmw1 + "_" + "NOUN")
                     elif d1.check(clmw1) == True:
                        arr2.append(clmw1 + "_" + "NOUN")
           
                  else:
                     clmw1 = clmw1
                     if d.check(clmw1) == True:
                        arr2.append(clmw1 + "_" + "NOUN")
                     elif d1.check(clmw1) == True:
                        arr2.append(clmw1 + "_" + "NOUN")




           if pp == "JJ":
       #arr1.append(p[0] + "_" + "ADJ")
              #print py
              if py == "one" or py == "ones":
                 pos_new = "NUM"
                 arr2.append("one" + "_" + "NUM")

              elif py == "saturated":
                       #pos_new = "NOUN"
                   arr2.append("saturate" + "_" + "VERB")

              #elif py == "done":
              #     arr2.append("does" + "_" + "VERB")

              else:
             

                   clmw = wordnet_lemmatizer.lemmatize(py)
                   clmw1 = wn.morphy(clmw)

                   if clmw1 == None:
                     clmw1 = clmw
                     if d.check(clmw1) == True:
                        arr2.append(clmw1 + "_" + "ADJ")
                   else:
                     clmw1 = clmw1
                     if d.check(clmw1) == True:
                        arr2.append(clmw1 + "_" + "ADJ")

                   

                   #if d.check(clmw1) == True:
                   #   arr2.append(clmw1 + "_" + "ADJ") 
                   #else:
                   #   arr2.append(py + "_" + "ADJ")                      





       
           if pp == "VB":
       #arr1.append(p[0] + "_" + "VERB")
              if py == "pass":
                 arr2.append("pass" + "_" + "VERB")

              elif py == "fed":
                   arr2.append("feed" + "_"+"VERB")
              elif py == "colored":
                   arr2.append("color" + "_" + "NOUN")
              elif py == "done":
                   arr2.append("")
              elif py == "data":
                   arr2.append("data" + "_" + "NOUN")

              else:

                   clmw = wordnet_lemmatizer.lemmatize(py)
                   #print clmw
                   clmw1 = wn.morphy(clmw)
                   #print clmw1
                   if d.check(clmw1) == True:
                    
                      try:

                          clmw2 = en.verb.present(clmw1) 
                          #print clmw2

                          clmw3 = wn.morphy(clmw2)                    
                          arr2.append(clmw3 + "_" +"VERB")


                       #v1 = en.verb.present(clmw1)
                       #str_s1.append(v1 + "_" +"VERB")
                      except KeyError:
                          arr2.append(clmw1 + "_"+"VERB")            


       

           if pp == "RB":
       #arr1.append(p[0] + "_" + "ADV")
              if py == "farthest":
                 pos_new = "ADV"
                 arr2.append("farther" + "_" + "ADV")

              if py == "add":
                 arr2.append("add" + "_" + "VERB")

              #if py == "statically":
              #   arr2.append("static" + "_" + "ADJ")
              else:

                 clmw = wordnet_lemmatizer.lemmatize(py)
                 #print clmw
                 clmw1 = wn.morphy(clmw)
                 #print clmw1
                 if clmw1 != None:
                    if d.check(clmw1) == True:
                       arr2.append(clmw1 + "_" + "ADV")
                 else:
                    if d.check(clmw) == True:
                       arr2.append(clmw + "_" + "ADV")
                       
      



    #print arr1
    #print arr2

    if "" in arr1:
       arr1.remove("")
    else:
       arr1 = arr1


    if "" in arr2:
       arr2.remove("")
    else:
       arr2 = arr2



       #arr1.remove("")
    #arr2.remove("") 
    #print arr1
    #arr1 = ['enqueue_NOUN', 'dequeue_NOUN']
    #print arr2

    #sims_opt = word_vectors.n_similarity(arr1, arr2)

    #print sims_opt

    #print arr1
    #print arr2

    if arr1 == [] or arr2 == [] or (arr1 == [] and arr2 == []):
       #print aa
       #print bb
       sim = similar(aa, bb)
       #print sim
       simi_result.append(sim)

    else:
      
       try:
          sims_opt = word_vectors.n_similarity(arr1, arr2)
          #print sims_opt
       except KeyError as ex:
          ffs = []
          exx = (ex.args[0])
          #print exx
          exx1 = exx.split(" ")
          #print exx1

          sims_opt = similar(aa, bb)


          """err = exx1[1]
          err1 = err.split("_")
          #print err1
         
           
          err_q = ""
          for i in err1[0]:
              if i != "'":
                 err_q = err_q + i

          #print err_q
          syn = wn.synsets(err_q)
          #print syn
          #print syn[0]
          
          s1 = syn[0].name()
          s2 = s1.split(".")
          w = s2[0]

          #print w
          
          s3 = syn[0].pos()
          if s3 == 'n':
             ps = 'NOUN'
          elif s3 == 'v':
               ps = 'VERB'
          elif s3 == 'a' or s3 == 's':
               ps = 'ADJ'
          elif s3 == 'r':
               ps = 'ADV'

          #print ps
 
          aa = []
          aa.append(w)
          aa.append(ps)

          bb = "_".join(aa[:])

          #print bb

          arr11 = []

          for ii in arr1:
              ii1 = ii.split("_")
              if err_q == ii1[0]:
                 arr11.append(bb)
              else:
                 arr11.append(ii)

          #print arr11

          arr22 = []
          for ii in arr2:
              ii1 = ii.split("_")
              if err_q == ii1[0]:
                 arr22.append(bb)
              else:
                 arr22.append(ii)

          
          #print arr22

          try:

            sims_opt = word_vectors.n_similarity(arr11, arr22)       
          except KeyError as ex:
            
            sims_opt = similar(arr11, arr22)"""
                   
          
       simi_result.append(sims_opt)

#print simi_result

s2 = []
for i in simi_result:
    s2.append(str(i))


s1 = ",".join(s2[:])



print s1

#print type(s1)
"""
output:

['remove_VERB', 'item_NOUN', 'front_NOUN', 'queue_NOUN']
1.0,0.384543717459,1.0,0.449339485565,0.279996482544,0.634113760397,0.279996482544,0.659866360823,0.866563046879,0.549722606271,0.866563046879,0.583834496032,0.285714285714,0.459459459459,0.285714285714,0.207792207792


"""




#if final_st22 == []:
#                 sims_opt = 0.0
#              else:

#                 try:
#                   print final_st22
#                   print final_m22
#sims_opt = word_vectors.n_similarity(arr1, arr2)

#print arr1
#print arr2
       #sims_opt = word_vectors.n_similarity(arr1, arr2)
       #print sims_opt

# check stopwords 'other' and others also
       
