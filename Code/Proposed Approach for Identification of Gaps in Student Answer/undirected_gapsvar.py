import itertools
import nltk
from nltk import word_tokenize
import os

from itertools import groupby
from operator import itemgetter

import csv
import numpy
from apgl.graph import *

from requests import get


#import itertools
from itertools import chain, combinations
from collections import defaultdict
from gensim import corpora, models, similarities
import math



import string
import gensim
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import re, collections

import enchant
from gensim.models.keyedvectors import KeyedVectors
from nltk.corpus import wordnet as wn
import en

import numpy as np



from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

d = enchant.Dict("en_US")
d1 = enchant.Dict("en_UK")

wordnet_lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stopset = list(stopwords.words('english')) + ['across'] + ['underneath'] + ['within'] + ['halfway'] + ['slipperiness'] + ['neither'] + ['besides'] + ['sleet'] + ['nowhere'] + ['beyond'] + ['could'] + ['without'] + ['Dear'] + ['dear'] + ['someplace'] + ['do'] + ['something'] + ['else']

word_vectors = KeyedVectors.load_word2vec_format('/location-to-store-output-files/enwiki_5_ner.txt', binary=False)




def model_sim(a, b): 
   
    pos1 = nltk.pos_tag(word_tokenize(a))
    pos2 = nltk.pos_tag(word_tokenize(b))      

    arr1 = []
    for p in pos1:
    
        pp = p[1][0:2]       
    
        px = p[0].lower()

        if px not in stopset: 
           if pp == "NN":     
                     
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

                   clmw = wordnet_lemmatizer.lemmatize(px)
                   
                   clmw1 = wn.morphy(clmw)
                  

                   if clmw1 == None:
                     clmw1 = clmw
                     
                     if d.check(clmw1) == True:
                        arr1.append(clmw1 + "_" + "NOUN")

                     elif d1.check(clmw1) == True:
                        arr1.append(clmw1 + "_" + "NOUN")
                   else:
                     clmw1 = clmw1
                     
                     if d.check(clmw1) == True:
                        arr1.append(clmw1 + "_" + "NOUN")

                     elif d1.check(clmw1) == True:
                        arr1.append(clmw1 + "_" + "NOUN")

                     else:
                        arr1.append(clmw1)
                        

                   




           if pp == "JJ":
      
              if px == "one" or px == "ones":
                 pos_new = "NUM"
                 arr1.append("one" + "_" + "NUM")

              elif px == "saturated":
                      
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


                                  





       
           if pp == "VB":
       
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
                          

                         clmw3 = wn.morphy(clmw2)                    
                         arr1.append(clmw3 + "_" +"VERB")


                       
                      except KeyError:
                         arr1.append(clmw1 + "_"+"VERB")            


       

           if pp == "RB":
       
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









    arr2 = []
    for p in pos2:  
        

        pp = p[1][0:2]
    
        py = p[0].lower()
        if py not in stopset: 
           if pp == "NN":       
       
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
             
                  
              else:
                  
                  clmw = wordnet_lemmatizer.lemmatize(py)
                  

                  clmw1 = wn.morphy(clmw)
                  
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
       
              if py == "one" or py == "ones":
                 pos_new = "NUM"
                 arr2.append("one" + "_" + "NUM")

              elif py == "saturated":
                       
                   arr2.append("saturate" + "_" + "VERB")              

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

                                     





       
           if pp == "VB":
       
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
                   clmw1 = wn.morphy(clmw)
                   if d.check(clmw1) == True:
                    
                      try:
                          clmw2 = en.verb.present(clmw1)                         

                          clmw3 = wn.morphy(clmw2)                    
                          arr2.append(clmw3 + "_" +"VERB")


                       
                      except KeyError:
                          arr2.append(clmw1 + "_"+"VERB")            


       

           if pp == "RB":
       
              if py == "farthest":
                 pos_new = "ADV"
                 arr2.append("farther" + "_" + "ADV")

              if py == "add":
                 arr2.append("add" + "_" + "VERB")
              else:

                 clmw = wordnet_lemmatizer.lemmatize(py)
                 clmw1 = wn.morphy(clmw)
                 if d.check(clmw1) == True:
                    arr2.append(clmw1 + "_" + "ADV")    



    

    if "" in arr1:
       arr1.remove("")
    else:
       arr1 = arr1


    if "" in arr2:
       arr2.remove("")
    else:
       arr2 = arr2      

    if arr1 == [] or arr2 == [] or (arr1 == [] and arr2 == []):
       sims_opt = similar(a, b)
       return sims_opt

    else:
      
       try:
          sims_opt = word_vectors.n_similarity(arr1, arr2)
          return sims_opt
          
       except KeyError as ex:
          ffs = []
          exx = (ex.args[0])
          exx1 = exx.split(" ")      
       
    




def spell_check(word, NWORDS):                                                  # function for spell-checker

    
    def edits1(word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
        inserts    = [a + c + b     for a, b in splits for c in alphabet]
        return set(deletes + transposes + replaces + inserts)

    def known_edits2(word):
        return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

    def known(words): return set(w for w in words if w in NWORDS)

    def correct(word):
        candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
        return max(candidates, key=NWORDS.get)
    
    aa = correct(word)


   
    return(aa)

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model



def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text



NWORDS = train(words(file('wikiArticles.txt').read()))


alphabet = 'abcdefghijklmnopqrstuvwxyz'


def remove_punc(string):
    
    punctuations = '''"'''

    no_punct = ""
    for char in string:
        if char not in punctuations:
           no_punct = no_punct + char

# display the unpunctuated string

    
    return(no_punct)



m1m = []
fp = open('/location-to-store-output-files/outm_24.txt', 'r')
for line in fp:
    m1m.append(line)
fp.close()


arrm_p = [[] for i in range(0, len(m1m))]

arrm = [[] for i in range(0, len(m1m))]
for i in range(0,len(m1m)):
    
    sel = m1m[i].split("\t")
    
    a = sel[0]
    b = sel[2].rstrip()
    arrm[i].append(a)                                # arrm contains the nodes of model answer graph...arrm_p contains corresponding edges
    arrm[i].append(b)                                                   
    arrm_p[i].append(sel[1])



graph1 = DictGraph()

edges1 = numpy.array(arrm, numpy. str)


graph1.addEdges(edges1)


vv = graph1.getAllVertexIds()



vtx1 = []
for i in range(0, len(vv)):
    vtx1.append(i)


com1 = zip(vv, vtx1)                            # for model ans


edgeIndices1 = graph1.getAllEdgeIndices()


graph3 = SparseGraph(GeneralVertexList(graph1.getNumVertices()))
graph3.addEdges(edgeIndices1)

graph3.adjacencyMatrix()

with open('/location-to-store-output-files/graphm-0.52/arch/m_adj.csv', 'wb') as csvfile:
     writer = csv.writer(csvfile, delimiter = ' ')
     for line in graph3.adjacencyMatrix():
         writer.writerow(line)

         

m1 = []
fp = open("/location-to-store-output-files/outs_24.txt", "r")
for line in fp:
    m1.append(line)
fp.close()

            



arr_p = [[] for i in range(0, len(m1))]

arr = [[] for i in range(0, len(m1))]
for i in range(0,len(m1)):
    
    sel = m1[i].split("\t")
            
    a = sel[0]
    b = sel[2].rstrip()
    arr[i].append(a)
    arr[i].append(b)
    arr_p[i].append(sel[1])



graph = DictGraph()

edges = numpy.array(arr, numpy. str)



graph.addEdges(edges)



vv1 = graph.getAllVertexIds()


vtx2 = []
for i in range(0, len(vv1)):
    vtx2.append(i)


com2 = zip(vv1, vtx2)                      # for student ans



edgeIndices = graph.getAllEdgeIndices()



graph2 = SparseGraph(GeneralVertexList(graph.getNumVertices()))
graph2.addEdges(edgeIndices)

graph2.adjacencyMatrix()

with open('/location-to-store-output-files/graphm-0.52/arch/s_adj.csv', 'wb') as csvfile:
     writer = csv.writer(csvfile, delimiter = ' ')
     for line in graph2.adjacencyMatrix():
         writer.writerow(line)











nodes_s = []

for i in arr:
    nodes_s.append(i[0])
    nodes_s.append(i[1])

nodes_s = set(nodes_s)


nodes_m = []

for i in arrm:
    nodes_m.append(i[0])
    nodes_m.append(i[1])

nodes_m = set(nodes_m)




IT = itertools.product(nodes_m, nodes_s)



tuple_ma = []

tuple_sa = []

lol_sim = []

lol_ind = []

lol = [[0 for i in range(0, len(com2))] for j in range(0, len(com1))]     # com1: MA nodes, com2: SA nodes


for xx in IT:
       
    ss1 = xx[0].split(" ")
    ss2 = xx[1].split(" ")
    
    phr_1 = []
    for x in ss1:
        pp1 = spell_check(x, NWORDS)
        qq1 = unicode(str(pp1), "utf-8")
        phr_1.append(qq1)

    phr_2 = []
    for y in ss2:
        pp2 = spell_check(y, NWORDS)
        qq2 = unicode(str(pp2), "utf-8")
        phr_2.append(qq2)


    
    
    phr_11 = " ".join(phr_1[:])
    phr_22 = " ".join(phr_2[:])
    ps = model_sim(phr_11, phr_22)

        
    for jj in com1:
        if jj[0] == xx[0]:
           in1 = jj[1]
           break
    
    for jj in com2:
        if jj[0] == xx[1]:
           in2 = jj[1]
           break

    lol[in1][in2] = ps

    
    cc1 = com1[in1]
    cc2 = com2[in2]

    tuple_ma.append(cc1)
    tuple_sa.append(cc2)

    lol_sim.append(ps)
    aa = []
    aa.append(in1)
    aa.append(in2)

    lol_ind.append(aa)

    

#print tuple_ma                            # these are the nodes of model answer 
#print len(tuple_ma)

#print tuple_sa                            # these are the nodes of student answer
#print len(tuple_sa)

#print lol_ind

#MyList = ['a','b','c','d','e','f']
# Calculate desired row/col
row = len(com1)
col = len(com2)
lolind_lol = [lol_ind[col*i : col*(i+1)] for i in range(row)]
#>>>NewList
#[['a', 'b', 'c'], ['d', 'e', 'f']]




lolind_trans = zip(*lolind_lol)



tuples_trans = [item for sublist in lolind_trans for item in sublist]

#print tuples_trans   # MA node is first, SA node is second



for i in range(0, len(lol)):
    for j in range(0, len(lol[i])):
        
        if lol[i][j] == None:
           
           lol[i][j] = 0.0




numrows = len(lol)
numcols = len(lol[0])


lol_trans = zip(*lol)
numrows1 = len(lol_trans)
numcols1 = len(lol_trans[0])



def Reverse(tuples): 
    new_tup = tuples[::-1] 
    return new_tup 
      




tuple_pairs1 = []
tuple_pairs2 = []
tuple_sim = []
tuple_init = []  
   


if len(vv1) > len(vv) or len(vv1) == len(vv):        # MA < SA or MA == SA

   with open("/location-to-store-output-files/graphm-0.52/arch/cost.csv", "wb") as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerows(lol)

   #os.system("cd graphm-0.52/arch/; ./test_script")                        # smaller graph (graph_1) is always at the left...here it is MA graph exp_out file is generated accordingly

   os.system("sh isorank.sh")

     

   import csv
   with open("/location-to-store-output-files/graphm-0.52/arch/new_cost.csv") as f:
        reader = csv.reader(f, delimiter=' ')
    
        data = []
        for row in reader:
            data.append(row)

        
        tuple_sim = [float(item) for sublist in data for item in sublist]       


   
        tuple_init = [item for sublist in lol for item in sublist]

        

        tuple_saa = []

        tuple_maa = []

        for ii in lol_ind:
                        
            iim = [item for item in tuple_ma if item[1] == ii[0]]

            unique_ma = [tuple(x) for x in set(map(frozenset, iim))]           
            
            iis = [item for item in tuple_sa if item[1] == ii[1]]
            unique_sa = [tuple(x) for x in set(map(frozenset, iis))]

            
            tuple_maa.append(unique_ma[0])
            tuple_saa.append(Reverse(unique_sa[0]))


        
        tp_1 = []
        tp_2 = []
     
        for jj in range(len(tuple_maa)):
            tp_1.append(tuple_maa[jj][0])
            
        for jj in range(len(tuple_saa)):
            tp_2.append(tuple_saa[jj][0])

        
        tp = zip(tp_1, tp_2, tuple_sim, tuple_init) 

        print tp   

        f = open('/location-to-store-output-files/tp.txt', 'w')
        f.write(str(tp))
        f.close()  

            

if len(vv1) < len(vv):                                             # MA > SA 

   with open("/location-to-store-output-files/graphm-0.52/arch/cost.csv", "wb") as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerows(lol_trans)
   #os.system("cd graphm-0.52/arch/; ./test_script1")           # here it is SA graph at the left

   os.system("sh isorank_2.sh")

   
      

   import csv
   with open("/location-to-store-output-files/graphm-0.52/arch/new_cost.csv") as f:
        reader = csv.reader(f, delimiter=' ')
    
        data = []
        for row in reader:
            data.append(row)

        

        tuple_sim = [float(item) for sublist in data for item in sublist]    


  

        tuple_init = [item for sublist in lol_trans for item in sublist]

        


        tuple_saa = []

        tuple_maa = []

        for ii in tuples_trans:        

                        
            iim = [item for item in tuple_ma if item[1] == ii[0]]            

            unique_ma = [tuple(x) for x in set(map(frozenset, iim))]          

                        
             
            iis = [item for item in tuple_sa if item[1] == ii[1]]
            
            unique_sa = [tuple(x) for x in set(map(frozenset, iis))]
             

            tuple_maa.append(unique_ma[0])
            tuple_saa.append(Reverse(unique_sa[0]))

        
        tp_1 = []
        tp_2 = []
     
        for jj in range(len(tuple_maa)):
            tp_1.append(tuple_maa[jj][0])
            
        for jj in range(len(tuple_saa)):
            tp_2.append(tuple_saa[jj][0])

        
        tp = zip(tp_1, tp_2, tuple_sim, tuple_init)          

        f = open('/location-to-store-output-files/tp.txt', 'w')
        f.write(str(tp))
        f.close()   

        



 
              


          



          
          

       

       

 

       

       
        
     
       
 

    


    
 

 


           
    
        

    
    




    





  













 
    

    












    







