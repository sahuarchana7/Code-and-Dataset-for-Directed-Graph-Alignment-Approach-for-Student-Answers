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

st = POS_Tag(model_filename='/home/archana/ve/stanford-postagger-2018-10-16/models/english-bidirectional-distsim.tagger', path_to_jar='/home/archana/ve/stanford-postagger-2018-10-16/stanford-postagger.jar')



def remove():
    os.remove('/location-to-store-output-files/ss.tagged')
    os.remove('/location-to-store-output-files/mm.tagged')
    os.remove('/location-to-store-output-files/s1.tagged')
    os.remove('/location-to-store-output-files/s1.osent')
    os.remove('/location-to-store-output-files/s1.sst')
    os.remove('/location-to-store-output-files/s1.parse')
    os.remove('/location-to-store-output-files/m.tagged')
    os.remove('/location-to-store-output-files/m.osent')
    os.remove('/location-to-store-output-files/m.parse')
    os.remove('/location-to-store-output-files/m.sst')
    os.remove('/location-to-store-output-files/pro_opm.txt')
    os.remove('/location-to-store-output-files/pro_ops.txt')
    os.remove('/location-to-store-output-files/outm.txt')
    os.remove('/location-to-store-output-files/outm_1.txt')
    os.remove('/location-to-store-output-files/outm_23.txt')
    os.remove('/location-to-store-output-files/outm_24.txt')
            
          
    os.remove('./delete_iteration/outs.txt')
    os.remove('./delete_iteration/outs_1.txt')
    os.remove('./delete_iteration/outs_23.txt')
    os.remove('./delete_iteration/outs_24.txt')
            

    os.remove('/location-to-store-output-files/m.txt')
    os.remove('/location-to-store-output-files/s1.txt')
    os.remove('/location-to-store-output-files/1_inp1.txt')
    os.remove('/location-to-store-output-files/2_inp1.txt')
    os.remove('/location-to-store-output-files/wouts_2.txt')
    os.remove('/location-to-store-output-files/woutm_2.txt')     
           

        

def vector_generate(f3, f4, ff1, ff, word_vectors):


           poss_m = []
           poss_s = []

           f3 = open('/location-to-store-output-files/m.txt', 'r')
           f33 = f3.readlines()
           for line in f33:
               
               n1 = st.tag(line.split())
               for i in n1:
                   poss_m.append(i)
           f3.close()



           f4 = open('/location-to-store-output-files/s1.txt', 'r')
           f44 = f4.readlines()
           for line in f44:
               
               n1 = st.tag(line.split())
               for i in n1:
                   poss_s.append(i)
           f4.close()






           f = open('/location-to-store-output-files/outm_24.txt', 'r')                 # all triples obtained from IE tool

           f1 = f.readlines()
           lm = len(f1)
           bb = []
           for line in f1:
               line = line.split("\t")
               l = line[1]
               l1 = l.split(" ") 


    

               w_pos = []
               for xx in l1:
                   pos = [item[1] for item in poss_m if xx in item[0]]
        
                   if pos != []:
                      yy = []
                      yy.append(xx)
                      yy.append(pos[0])
                      w_pos.append(tuple(yy))

              

   
    

               if len(w_pos) > 1:
                  l1 = l.split(" ")
                  new_word_pos = []
                  for j in range(len(l1)):
                      if l1[j] not in stopset:
                         new_word_pos.append(w_pos[j])


       
                 

                  new_word_pos2 = []      

                  for jj in new_word_pos:
          
                      jj1 = jj[1]
                      jj2 = jj1[0:2] 
                      jj3 = []
                      jj3.append(jj[0])
                      jj3.append(jj2)
                      jj4 = tuple(jj3)

                      new_word_pos2.append(jj4)

       
                  
                  for ii in new_word_pos2:

           
           

                      if ii[1] == "NN":
                         if ii[0] == "one" or ii[0] == "ones":
                    
                            j3 = "one" + "_" + "NUM"
                            wv = word_vectors[j3]
                    
                            ff1.write(ii[0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
    
                    
                    

                         elif ii[0] == "uses":
                      
                              j3 = "use" + "_" + "VERB"
                              wv = word_vectors[j3]
                      

                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
                      

                         elif ii[0] == "whacking":
                      
                              j3 = "whack" + "_" + "VERB"
                              wv = word_vectors[j3]
                      
                       
                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
                      

                         elif ii[0] == "warmness":
                      
                              j3 = "warmth" + "_" + "NOUN" 
                              wv = word_vectors[j3]
                     

                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
                                 
                                 

                         else:

                              clmw = wordnet_lemmatizer.lemmatize(ii[0])
                              clmw1 = wn.morphy(clmw)
                              if d.check(clmw1) == True:
                                 j3 = clmw1 + "_" + "NOUN"
                                 wv = word_vectors[j3]
                        

                                 ff1.write(ii[0])
                                 ff1.write('\n')

                                 for item in wv:
                                     ff.write("%f " % item)

                                 ff.write('\n')

                                  
                                 




                      if ii[1] == "VB":   
             
                        if ii[0] == "pass":
                            j3 = "pass" + "_" + "VERB"
                            wv = word_vectors[j3]
                      

                            ff1.write(ii[0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')




                    

                        elif ii[0] == "created":
                         j3 = "create" + "_" + "VERB"
                         
                         wv = word_vectors[j3]
                        

                         ff1.write(ii[0])
                         ff1.write('\n')

                         for item in wv:
                             ff.write("%f " % item)

                         ff.write('\n')



                   
                        else:

                          lmw = wordnet_lemmatizer.lemmatize(ii[0])
                          lmw1 = wn.morphy(lmw)
                          if d.check(lmw1) == True:
                 

                            try:
                             lmw2 = en.verb.present(lmw1) 
                             lmw3 = wn.morphy(lmw2)                    
                             j3 = lmw3 + "_" +"VERB"
                             wv = word_vectors[j3]
                            

                             ff1.write(ii[0])
                             ff1.write('\n')

                             for item in wv:
                                 ff.write("%f " % item)

                             ff.write('\n')




                   
                            except KeyError:
                             j3 = lmw1 + "_"+"VERB"
                             wv = word_vectors[j3] 
                             

                             ff1.write(ii[0])
                             ff1.write('\n')

                             for item in wv:
                                 ff.write("%f " % item)

                             ff.write('\n')




                      if ii[1] == "RB":

                         if ii[0] == "farthest":
                            pos_new = "ADV"
                            j3 = "farther" + "_" + "ADV"
                            wv = word_vectors[j3]
                    

                            ff1.write(ii[0])
                            ff1.write('\n')

                            for item in wv:
                              ff.write("%f " % item)

                            ff.write('\n')
                       
                   
                   
                         else:

                           clmw = wordnet_lemmatizer.lemmatize(ii[0])
                           clmw1 = wn.morphy(clmw)
                           if d.check(clmw1) == True:
                              j3 = clmw1 + "_" + "ADV"  
                              wv = word_vectors[j3]
                       

                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
                       




                
                      if ii[1] == "JJ":
                         if ii[0] == "one" or ii[0] == "ones":
                     
                            j3 = "one" + "_" + "NUM"
                            wv = word_vectors[j3]
                    

                            ff1.write(ii[0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                   

                         elif ii[0] == "saturated":
                       
                            j3 = "saturate" + "_" + "VERB"
                            wv = word_vectors[j3]
                      

                            ff1.write(ii[0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                      

                         else:

                            clmw = wordnet_lemmatizer.lemmatize(ii[0])
                            clmw1 = wn.morphy(clmw)
                            if d.check(clmw1) == True:
                               j3 = clmw1 + "_" + "ADJ" 
                               wv = word_vectors[j3]
                        

                               ff1.write(ii[0])
                               ff1.write('\n')

                               for item in wv:
                                   ff.write("%f " % item)

                               ff.write('\n')
                       

                            else:
                               j3 = ii[0] + "_" + "ADJ"
                               wv = word_vectors[j3]
                        

                               ff1.write(ii[0])
                               ff1.write('\n')

                               for item in wv:
                                   ff.write("%f " % item)

                               ff.write('\n')


    
               elif w_pos != [] and w_pos[0][0] not in stopset:

                    new_word_pos = []
             
                    jj1 = w_pos[0][1]
                    jj2 = jj1[0:2] 
                    jj3 = []
                    jj3.append(w_pos[0][0])
                    jj3.append(jj2)
                    jj4 = tuple(jj3)

                    new_word_pos.append(jj4)

                   

                    if new_word_pos[0][1] == "NN":
                       if new_word_pos[0][0] == "one" or new_word_pos[0][0] == "ones":
                    
                          j3 = "one" + "_" + "NUM"
                          wv = word_vectors[j3]
                   

                          ff1.write(new_word_pos[0][0])
                          ff1.write('\n')

                          for item in wv:
                              ff.write("%f " % item)

                          ff.write('\n')
                    

                       elif new_word_pos[0][0] == "uses":
                     
                            j3 = "use" + "_" + "VERB"
                            wv = word_vectors[j3]
                      

                            ff1.write(new_word_pos[0][0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                      

                       elif new_word_pos[0][0] == "whacking":
                     
                            j3 = "whack" + "_" + "VERB"
                            wv = word_vectors[j3]
                      

                            ff1.write(new_word_pos[0][0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                      

                       elif new_word_pos[0][0] == "warmness":
                      
                            j3 = "warmth" + "_" + "NOUN" 
                            wv = word_vectors[j3]
                      

                            ff1.write(new_word_pos[0][0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                                  
                                 

                       else:

                          clmw = wordnet_lemmatizer.lemmatize(new_word_pos[0][0])
                          clmw1 = wn.morphy(clmw)
                          
                          if d.check(clmw1) == True:
                             j3 = clmw1 + "_" + "NOUN"
                             wv = word_vectors[j3]
                         

                             ff1.write(new_word_pos[0][0])
                             ff1.write('\n')

                             for item in wv:
                                 ff.write("%f " % item)

                             ff.write('\n')


                    if new_word_pos[0][1] == "VB":   
             
                      if new_word_pos[0][0] == "pass":
                        j3 = "pass" + "_" + "VERB"
                        wv = word_vectors[j3]
                       

                        ff1.write(new_word_pos[0][0])
                        ff1.write('\n')

                        for item in wv:
                           ff.write("%f " % item)

                        ff.write('\n')
                    

                      elif new_word_pos[0][0] == "created":
                         j3 = "create" + "_" + "VERB"
                         
                         wv = word_vectors[j3]
                        

                         ff1.write(new_word_pos[0][0])
                         ff1.write('\n')

                         for item in wv:
                             ff.write("%f " % item)

                         ff.write('\n') 

                      elif new_word_pos[0][0] == "uses":
                         j3 = "use" + "_" + "VERB"
                         
                         wv = word_vectors[j3]
                        

                         ff1.write(new_word_pos[0][0])
                         ff1.write('\n')

                         for item in wv:
                             ff.write("%f " % item)

                         ff.write('\n') 

                        

                    
                      else:

                         lmw = wordnet_lemmatizer.lemmatize(new_word_pos[0][0])
                       
                         lmw1 = wn.morphy(lmw)
                       
                         if d.check(lmw1) == True:
                 

                            try:
                               lmw2 = en.verb.present(lmw1) 
                               lmw3 = wn.morphy(lmw2)                    
                               j3 = lmw3 + "_" +"VERB"
                               wv = word_vectors[j3]
                             

                               ff1.write(new_word_pos[0][0])
                               ff1.write('\n')

                               for item in wv:
                                 ff.write("%f " % item)

                               ff.write('\n')



                    
                            except KeyError:
                               j3 = lmw1 + "_"+"VERB"
                               wv = word_vectors[j3] 
                             

                               ff1.write(new_word_pos[0][0])
                               ff1.write('\n')

                               for item in wv:
                                   ff.write("%f " % item)

                               ff.write('\n')




                    if new_word_pos[0][1] == "RB":

                       if new_word_pos[0][0] == "farthest":
                          pos_new = "ADV"
                          j3 = "farther" + "_" + "ADV"
                          wv = word_vectors[j3]
                    
                          ff1.write(new_word_pos[0][0])
                          ff1.write('\n')

                          for item in wv:
                              ff.write("%f " % item)

                          ff.write('\n')
                    
                   
                       else:

                          clmw = wordnet_lemmatizer.lemmatize(new_word_pos[0][0])
                          clmw1 = wn.morphy(clmw)
                          if d.check(clmw1) == True:
                             j3 = clmw1 + "_" + "ADV"  
                             wv = word_vectors[j3]
                       

                             ff1.write(new_word_pos[0][0])
                             ff1.write('\n')

                             for item in wv:
                                 ff.write("%f " % item)

                             ff.write('\n')
                       




                 
                    if new_word_pos[0][1] == "JJ":
                       if new_word_pos[0][0] == "one" or new_word_pos[0][0] == "ones":
                     
                          j3 = "one" + "_" + "NUM"
                          wv = word_vectors[j3]
                    

                          ff1.write(new_word_pos[0][0])
                          ff1.write('\n')

                          for item in wv:
                              ff.write("%f " % item)

                          ff.write('\n')
                    

                       elif new_word_pos[0][0] == "saturated":
                       
                            j3 = "saturate" + "_" + "VERB"
                            wv = word_vectors[j3]
                      

                            ff1.write(new_word_pos[0][0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                      

                       else:

                           clmw = wordnet_lemmatizer.lemmatize(new_word_pos[0][0])
                           clmw1 = wn.morphy(clmw)
                           if d.check(clmw1) == True:
                              j3 = clmw1 + "_" + "ADJ" 
                              wv = word_vectors[j3]
                       

                              ff1.write(new_word_pos[0][0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
                        

                           else:
                              j3 = new_word_pos[0][0] + "_" + "ADJ"
                              wv = word_vectors[j3]
                        

                              ff1.write(new_word_pos[0][0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
   

               else:
          
                    bb.append(l1[0])




           f.close()






           f = open('/location-to-store-output-files/outs_24.txt', 'r')

           f1 = f.readlines()

           ls = len(f1)

           for line in f1:
	
               line = line.split("\t")
               l = line[1]

               l1 = l.split(" ")

    
    

               w_pos = []
               for xx in l1:
                   pos = [item[1] for item in poss_s if xx in item[0]]
        
                   if pos != []:
                      yy = []
                      yy.append(xx)
                      yy.append(pos[0])
                      w_pos.append(tuple(yy))




   
               

               if len(w_pos) > 1:
                  l1 = l.split(" ")
                  new_word_pos = []
                  for j in range(len(l1)):
           
                      if l1[j].lower() not in stopset:
                         new_word_pos.append(w_pos[j])
       



                  
                  new_word_pos2 = []      

                  for jj in new_word_pos:
          
                      jj1 = jj[1]
                      jj2 = jj1[0:2] 
                      jj3 = []
                      jj3.append(jj[0])
                      jj3.append(jj2)
                      jj4 = tuple(jj3)

                      new_word_pos2.append(jj4)

      
                  
                  for ii in new_word_pos2:
                     
          

                      if ii[1] == "NN":
                         if ii[0] == "one" or ii[0] == "ones":
                   
                            j3 = "one" + "_" + "NUM"
                            wv = word_vectors[j3]
                   

                            ff1.write(ii[0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')


                   
                         elif ii[0] == "uses" or ii[0] == "using":
                      
                              j3 = "use" + "_" + "VERB"
                              wv = word_vectors[j3]
                      

                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
                     

                         elif ii[0] == "whacking":
                      
                              j3 = "whack" + "_" + "VERB"
                              wv = word_vectors[j3]
                      

                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
                      

                         elif ii[0] == "warmness":
                      
                              j3 = "warmth" + "_" + "NOUN" 
                              wv = word_vectors[j3]
                      

                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
                        

                         elif ii[0] == "contains":
                       
                              j3 = "contain" + "_" + "VERB" 
                              wv = word_vectors[j3]
                     

                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')


                         elif ii[0] == "connected":
                       
                              j3 = "connect" + "_" + "VERB" 
                              wv = word_vectors[j3]
                     

                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
                         
                                          
                                 

                         else:

                             clmw = wordnet_lemmatizer.lemmatize(ii[0])
                             
                             clmw1 = wn.morphy(clmw)
                             
                             if d.check(clmw1) == True:
                                try:
                                   j3 = clmw1 + "_" + "NOUN"
                                   wv = word_vectors[j3]
                         

                                   ff1.write(ii[0])
                                   ff1.write('\n')

                                   for item in wv:
                                       ff.write("%f " % item)

                                   ff.write('\n')
                    
                                except TypeError:
                                    if clmw1 not in stopset:
                                       try:
                                          j3 = clmw1 + "_"+"VERB"
                                          wv = word_vectors[j3] 
                                       except:
                                   
                                   

                                          ww = wn.synsets(ii[0])
                                   
                                          ww1 = ww[0]
                                          ww2 = ww1.name()
                                          ww3 = ww2.split(".")[0]
                                          pos_w = ww1.pos()
                                          if pos_w == 'n':
                                             pp = 'NOUN'
                                          if pos_w == 'v':
                                             pp = 'VERB'
                                          if pos_w == 'a' or pos_w == 's':
                                             pp = 'ADJ'
                                          if pos_w == 'r':
                                             pp = 'ADV'

                          
                                          ww4 = ww3 + "_" +  pp
                                          wv = word_vectors[ww4]


                             

                                       ff1.write(ii[0])
                                       ff1.write('\n')

                                       for item in wv:
                                           ff.write("%f " % item)

                                       ff.write('\n')

                               
                  









                      if ii[1] == "VB":   
             
                         if ii[0] == "pass":
                            j3 = "pass" + "_" + "VERB"
                            wv = word_vectors[j3]
                       

                            ff1.write(ii[0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                    

                         elif ii[0] == "created":
                              j3 = "create" + "_" + "VERB"
                        
                              wv = word_vectors[j3]
                         

                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')


                         elif ii[0] == "using" or ii[0] == "uses":
                              j3 = "use" + "_" + "VERB"
                        
                              wv = word_vectors[j3]
                         

                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')


                    
                         else:

                            lmw = wordnet_lemmatizer.lemmatize(ii[0])
                            
                            lmw1 = wn.morphy(lmw)
                            
                            if d.check(lmw1) == True:
                  

                               try:
                                 lmw2 = en.verb.present(lmw1) 
                                 lmw3 = wn.morphy(lmw2)                    
                                 j3 = lmw3 + "_" +"VERB"
                                 wv = word_vectors[j3]
                            

                                 ff1.write(ii[0])
                                 ff1.write('\n')

                                 for item in wv:
                                     ff.write("%f " % item)

                                 ff.write('\n')

                    
                               except KeyError:
                                  if lmw1 not in stopset:
                                     try:
                                       j3 = lmw1 + "_"+"VERB"
                                       wv = word_vectors[j3] 
                                     except:
                                   
                                   

                                       ww = wn.synsets(ii[0])
                                   
                                       ww1 = ww[0]
                                       ww2 = ww1.name()
                                       ww3 = ww2.split(".")[0]
                                       pos_w = ww1.pos()
                                       if pos_w == 'n':
                                          pp = 'NOUN'
                                       if pos_w == 'v':
                                          pp = 'VERB'
                                       if pos_w == 'a' or pos_w == 's':
                                          pp = 'ADJ'
                                       if pos_w == 'r':
                                          pp = 'ADV'

                          
                                       ww4 = ww3 + "_" +  pp
                                       wv = word_vectors[ww4]


                             

                                     ff1.write(ii[0])
                                     ff1.write('\n')

                                     for item in wv:
                                         ff.write("%f " % item)

                                     ff.write('\n')

                               
                                   




                      if ii[1] == "RB":

                         if ii[0] == "farthest":
                            pos_new = "ADV"
                            j3 = "farther" + "_" + "ADV"
                            wv = word_vectors[j3]
                    

                            ff1.write(ii[0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                    
                   
                         else:

                            clmw = wordnet_lemmatizer.lemmatize(ii[0])
                            clmw1 = wn.morphy(clmw)
                            if d.check(clmw1) == True:
                               j3 = clmw1 + "_" + "ADV"  
                               wv = word_vectors[j3]
                       

                               ff1.write(ii[0])
                               ff1.write('\n')

                               for item in wv:
                                   ff.write("%f " % item)

                               ff.write('\n')
                       




                 
                      if ii[1] == "JJ":
                         if ii[0] == "one" or ii[0] == "ones":
                     
                            j3 = "one" + "_" + "NUM"
                            wv = word_vectors[j3]
                    

                            ff1.write(ii[0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                    

                         elif ii[0] == "saturated":
                      
                              j3 = "saturate" + "_" + "VERB"
                              wv = word_vectors[j3]
                      
                              ff1.write(ii[0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')


                      

                         else:
                     
                     
                             clmw = wordnet_lemmatizer.lemmatize(ii[0])
                     
                             clmw1 = wn.morphy(clmw)
                     
                             if d.check(clmw1) == True:
                                try:
                                   j3 = clmw1 + "_" + "ADJ" 
                                   wv = word_vectors[j3]
                       

                                   ff1.write(ii[0])
                                   ff1.write('\n')

                                   for item in wv:
                                       ff.write("%f " % item)

                                   ff.write('\n')
                                except:
                                   ww = wn.synsets(ii[0])
                                   ww1 = ww[0]
                                   ww2 = ww1.name()
                                   ww3 = ww2.split(".")[0]
                                   pos_w = ww1.pos()
                                   if pos_w == 'n':
                                      pp = 'NOUN'
                                   if pos_w == 'v':
                                      pp = 'VERB'
                                   if pos_w == 'a' or pos_w == 's':
                                      pp = 'ADJ'
                                   if pos_w == 'r':
                                      pp = 'ADV'

                          
                                   if ww3 not in stopset:
                                      ww4 = ww3 + "_" +  pp
                          
                                      wv = word_vectors[ww4]
                       

                                      ff1.write(ii[0])
                                      ff1.write('\n')

                                      for item in wv:
                                          ff.write("%f " % item)

                                      ff.write('\n')

                        

                             else:
                                j3 = ii[0] + "_" + "ADJ"
                                wv = word_vectors[j3]
                        

                                ff1.write(ii[0])
                                ff1.write('\n')

                                for item in wv:
                                    ff.write("%f " % item)

                                ff.write('\n')

   
       
               elif w_pos != [] and w_pos[0][0] not in stopset:
                    new_word_pos = []
              
                    jj1 = w_pos[0][1]
                    jj2 = jj1[0:2] 
                    jj3 = []
                    jj3.append(w_pos[0][0].lower())
                    jj3.append(jj2)
                    jj4 = tuple(jj3)

                    new_word_pos.append(jj4)

          

       
                    if new_word_pos[0][1] == "NN":
                       if new_word_pos[0][0] == "one" or new_word_pos[0][0] == "ones":
                    
                          j3 = "one" + "_" + "NUM"
                          wv = word_vectors[j3]
                    

                          ff1.write(new_word_pos[0][0])
                          ff1.write('\n')

                          for item in wv:
                              ff.write("%f " % item)

                          ff.write('\n')
                    

                       elif new_word_pos[0][0] == "uses":
                     
                            j3 = "use" + "_" + "VERB"
                            wv = word_vectors[j3]
                      

                            ff1.write(new_word_pos[0][0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                      

                       elif new_word_pos[0][0] == "whacking":
                      
                            j3 = "whack" + "_" + "VERB"
                            wv = word_vectors[j3]
                      
                            ff1.write(new_word_pos[0][0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                      

                       elif new_word_pos[0][0] == "warmness":
                       
                            j3 = "warmth" + "_" + "NOUN" 
                            wv = word_vectors[j3]
                     

                            ff1.write(new_word_pos[0][0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                        


                       elif new_word_pos[0][0] == "contains":
                       
                            j3 = "contain" + "_" + "VERB" 
                            wv = word_vectors[j3]
                      

                            ff1.write(new_word_pos[0][0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                                    
                                 

                       else:
                      

                           clmw = wordnet_lemmatizer.lemmatize(new_word_pos[0][0])
                      
                           clmw1 = wn.morphy(clmw)
                      
                           if d.check(clmw1) == True:
                              j3 = clmw1 + "_" + "NOUN"
                              wv = word_vectors[j3]
                         

                              ff1.write(new_word_pos[0][0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')


                    if new_word_pos[0][1] == "VB":   
             
                       if new_word_pos[0][0] == "pass":
                          j3 = "pass" + "_" + "VERB"
                          wv = word_vectors[j3]
                       

                          ff1.write(new_word_pos[0][0])
                          ff1.write('\n')

                          for item in wv:
                              ff.write("%f " % item)

                          ff.write('\n')
                   

                       elif new_word_pos[0][0] == "created":
                            j3 = "create" + "_" + "VERB"
                         
                            wv = word_vectors[j3]
                         

                            ff1.write(new_word_pos[0][0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')



                       elif new_word_pos[0][0] == "using" or new_word_pos[0][0] == "uses":
                            j3 = "use" + "_" + "VERB"
                         
                            wv = word_vectors[j3]
                        

                            ff1.write(new_word_pos[0][0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')



                    
                       else:

                           lmw = wordnet_lemmatizer.lemmatize(new_word_pos[0][0])
                       
                           lmw1 = wn.morphy(lmw)
                       
                           if d.check(lmw1) == True:
                 

                              try:
                                 lmw2 = en.verb.present(lmw1) 
                                 lmw3 = wn.morphy(lmw2)                    
                                 j3 = lmw3 + "_" +"VERB"
                                 wv = word_vectors[j3]
                             

                                 ff1.write(new_word_pos[0][0])
                                 ff1.write('\n')

                                 for item in wv:
                                     ff.write("%f " % item)

                                 ff.write('\n')

                    
                              except KeyError:
                                 j3 = lmw1 + "_"+"VERB"
                                 wv = word_vectors[j3] 
                            

                                 ff1.write(new_word_pos[0][0])
                                 ff1.write('\n')

                                 for item in wv:
                                     ff.write("%f " % item)

                                 ff.write('\n')




                    if new_word_pos[0][1] == "RB":

                       if new_word_pos[0][0] == "farthest":
                          pos_new = "ADV"
                          j3 = "farther" + "_" + "ADV"
                          wv = word_vectors[j3]
                   

                          ff1.write(new_word_pos[0][0])
                          ff1.write('\n')

                          for item in wv:
                              ff.write("%f " % item)

                          ff.write('\n')
                    
                   
                       else:

                           clmw = wordnet_lemmatizer.lemmatize(new_word_pos[0][0])
                           clmw1 = wn.morphy(clmw)
                           if d.check(clmw1) == True:
                              j3 = clmw1 + "_" + "ADV"  
                              wv = word_vectors[j3]
                       

                              ff1.write(new_word_pos[0][0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
                       




                 
                    if new_word_pos[0][1] == "JJ":
                       if new_word_pos[0][0] == "one" or new_word_pos[0][0] == "ones":
                     
                          j3 = "one" + "_" + "NUM"
                          wv = word_vectors[j3]
                    

                          ff1.write(new_word_pos[0][0])
                          ff1.write('\n')

                          for item in wv:
                              ff.write("%f " % item)

                          ff.write('\n')
                    

                       elif new_word_pos[0][0] == "saturated":
                       
                            j3 = "saturate" + "_" + "VERB"
                            wv = word_vectors[j3]
                      

                            ff1.write(new_word_pos[0][0])
                            ff1.write('\n')

                            for item in wv:
                                ff.write("%f " % item)

                            ff.write('\n')
                     

                       else:

                           clmw = wordnet_lemmatizer.lemmatize(new_word_pos[0][0])
                           clmw1 = wn.morphy(clmw)
                           if d.check(clmw1) == True:
                              j3 = clmw1 + "_" + "ADJ" 
                              wv = word_vectors[j3]
                       

                              ff1.write(new_word_pos[0][0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
                        

                           else:
                              j3 = new_word_pos[0][0] + "_" + "ADJ"
                              wv = word_vectors[j3]
                        
                              ff1.write(new_word_pos[0][0])
                              ff1.write('\n')

                              for item in wv:
                                  ff.write("%f " % item)

                              ff.write('\n')
   

               else:
           
                   bb.append(l1[0])





           f.close()







i = 0
wordnet_lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
d = enchant.Dict("en_US")     
stopset = list(stopwords.words('english')) + ['across'] + ['underneath'] + ['within'] + ['halfway'] + ['slipperiness'] + ['neither'] + ['besides'] + ['sleet'] + ['nowhere'] + ['beyond'] + ['could'] + ['without'] + ['Dear'] + ['dear'] + ['someplace'] + ['must'] + ['can'] + ['would']


word_vectors = KeyedVectors.load_word2vec_format('/home/archana/wiki/pretrained_wiki_model/3/enwiki_5_ner.txt', binary=False)

ff1 = open('/location-to-store-output-files/cluster_words.txt', 'a')
ff = open('/location-to-store-output-files/model_vector.txt', 'a')




f = open('./student_model/sc_student.csv', 'r')


f1 = f.readlines()

g = open('./student_model/sc_model.csv', 'r')

g1 = g.readlines()

for line in f1:
    linee = line.split("\t")
    line1 = linee[0]
    line2 = line1.split(".") 
       
    for lines in g1:
        liness = lines.split("\t")
        lines1 = liness[0]
        
        
        if line1 == lines1:
           f3 = open('/location-to-store-output-files/m.txt', 'w')
           
           f3.write(liness[1])
           f4 = open('/location-to-store-output-files/s1.txt', 'w')
           
           f4.write(linee[1]) 
           f3.close()
           f4.close()

           os.system("sh /location-to-store-output-files/only_pred.sh")
      
           vector_generate(f3, f4, ff1, ff, word_vectors)
           remove()
           break



        elif len(line2) == 3:                       ## UNT
             line3 = ".".join(line2[0:2])
             if line3 == lines1:
                f3 = open('/location-to-store-output-files/m.txt', 'w')
                
                f3.write(liness[1])
                f4 = open('/location-to-store-output-files/s1.txt', 'w')
                
                f4.write(linee[1]) 
                f3.close()
                f4.close()

                os.system("sh /location-to-store-output-files/only_pred.sh")
      
                vector_generate(f3, f4, ff1, ff, word_vectors)
                remove()
                break


        elif len(line2) == 4:                  ## SB
             line3 = ".".join(line2[0:2])

             lines2 = lines1.split("-")
             ll3 = lines2[0].split("_")
             ll4 = ".".join(ll3[:])
             
             if line3 == ll4:
                f3 = open('/location-to-store-output-files/m.txt', 'w')
                
                f3.write(liness[1])
                f4 = open('/location-to-store-output-files/s1.txt', 'w')
                
                f4.write(linee[1]) 
                f3.close()
                f4.close()

                os.system("sh /location-to-store-output-files/only_pred.sh")
      
                vector_generate(f3, f4, ff1, ff, word_vectors)
                remove()
                break


    i = i + 1
    print i

ff1.close()
ff.close()


