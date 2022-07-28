import os, shutil

from sys import argv
from rouge import Rouge

rouge = Rouge()




import itertools

import os

from itertools import groupby
from operator import itemgetter

import csv
import numpy

import math




import re, collections










punctuations1 = '''()[],.':'''



punctuations = ["[", "]", "'"]



#ds = 'ScientsBank'
#type_file = 'only-dir'

#type_file = 'only-undir'

#interm_ops

# first give input as "1"/"2"/"3" ; "new"; "threshold"



# ds refers to the dataset either University of North Texas, SciEntsBank or Beetle dataset. 
# type_file refers to either 'dir' dataset or 'nodir' dataset. 'dir' dataset is comprised of student answers in which the directionality information in their respective answer graphs is of utmost importance for better understanding and 'nodir' dataset is comprised of student answers where the directionality information is not vital
# q indicates either 'refresh' or 'new' mode of creating dynamic folders for storing outputs. 
# r1 is the threshold for ROUGE-2 F1-Score. 

def path_decide(ds, q, r1, type_file, *args):
    
    #if ds == '1':
    if q == 'refresh':

          #ds = 'rada'
          #r1 = '0.3'

         


          shutil.rmtree('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/tp')
          shutil.rmtree('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/fp')
          shutil.rmtree('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/fn')
          shutil.rmtree('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_prec')
          shutil.rmtree('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_rec')
          shutil.rmtree('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_f1')







          os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/tp')
          os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/fp')
          os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/fn')
          os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_prec')
          os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_rec')
          os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_f1')

    elif q == 'new':
           #r1 = '0.3'
           #ds = 'rada'
           os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/tp')
           os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/fp')
           os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/fn')
           os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_prec')
           os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_rec')
           os.mkdir('location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_f1')
            
    return ds, r1, type_file

 
# arguments passed are dataset, new or refresh indicating creating a new folder at the location where to store outputs, threshold decided for ROUGE-2 F1 score that indicates similarity between predicted gap phrase and true gap phrase, type_file indicating whether determining the evaluation metrics for dir dataset or nodir dataset. 

# python extract-gaps.py ScientsBank new 0.5 dir 
        
ds, r1, type_file = path_decide(*argv[1:])


fl1 = ['location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file +'/tp/tp'+"_"+str(i)+".txt" for i in range(1,3)] 
tps = [open(fl1[j], "a") for j in range(len(fl1))]

fl2 = ['location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/fp/fp'+"_"+str(i)+".txt" for i in range(1,3)]
fps = [open(fl2[j], "a") for j in range(len(fl2))]


fl3 = ['location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/fn/fn'+"_"+str(i)+".txt" for i in range(1,3)] 
fns = [open(fl3[j], "a") for j in range(len(fl3))]


fl4 = ['location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_prec/m_prec'+"_"+str(i)+".txt" for i in range(1,3)]
m_prec = [open(fl4[j], "a") for j in range(len(fl4))]


fl5 = ['location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_rec/m_rec'+"_"+str(i)+".txt" for i in range(1,3)] 
m_rec = [open(fl5[j], "a") for j in range(len(fl5))] 

fl6 = ['location-where-wish-to-store-files/thres=' + r1 +'/'+ds+'/'+type_file + '/m_f1/f1'+"_"+str(i)+".txt" for i in range(1,3)]
m_f1 = [open(fl6[j], "a") for j in range(len(fl6))]

       





cnt = 0

f = open('location-where-wish-to-store-files/'+ds+'/total-dir.txt', 'r')   #  'dir' dataset file

f1 = f.readlines()
for line in f1:
    line = line.split("  ")
    idd = line[0]
    with open('location-where-wish-to-store-files/'+ds+'/tr_gaps.txt') as kfile:   # tr_gaps is the file that contains true gaps / gold standard gaps for the respective dataset 'ds'. 
         for line_t in kfile:
             if idd in line_t:
                line_t1 = line_t.split("\t")
                #xx1 = " ".join(xx[1:])
                #print line_t1

                if len(line_t1) != 1:
                   xx1 = line_t1[1]              

                   xx2 = xx1.split(" . ")
                

         
                   tr_gap = []
                   for i in xx2:
                      j = i.lower()
                      tr_gap.append(j)

                else:
                   tr_gap = []
                   tr_gap.append("")

                #print tr_gap




                file_names = ['location-where-wish-to-store-files/'+ds+'/all_gaps/final_gapsold1'+"_"+str(i)+".txt" for i in range(1,3)] 

# this is where predicted gaps are stored. 



                for iter1 in range(0, len(file_names)):
                
                    with open(file_names[iter1], 'r') as ffi:                  
                  
                         for linet in ffi:
                             ids = linet.split("\t")
                             ac_id = ids[0]                    
                                                                        

                             if idd == ac_id:
                                liness1 = ids[1]
                                break            
             
                    liness2 = liness1.split(", ")
                                 
                    no_punct_s = []
                    for j in liness2:           
                        no_punct = ""
                    
                        for kiter in j:
                            if kiter not in punctuations:
                               no_punct = no_punct + kiter                  
                        no_punct_s.append(no_punct)
               

                        no_punct_s[-1] = no_punct_s[-1].rstrip()               


                        bb1 = set(no_punct_s)

                
                    sys_gap = []
                    for i in bb1:
                        sys_gap.append(i)




                    print sys_gap

                    if tr_gap == [''] and sys_gap == ['']:    
                       tp = 0
                       fp = 0
                       fn = 0
                
                       prec = float(1.0)
                       tps[iter1].write(str(idd) + "\t"+ str(tp))
                       tps[iter1].write('\n')
                       fps[iter1].write(str(idd) + "\t" + str(fp))
                       fps[iter1].write('\n')
                       m_prec[iter1].write(str(idd) + "\t"+ str(prec))
                       m_prec[iter1].write('\n')

                       rec = float(1.0)
                       fns[iter1].write(str(idd) + "\t" + str(fn))
                       fns[iter1].write('\n')
                       m_rec[iter1].write(str(idd) + "\t" + str(rec))
                       m_rec[iter1].write('\n')

                       f1_sc = (2 * prec * rec)/(prec + rec)
                       f11_sc = float(f1_sc)
                       m_f1[iter1].write(str(idd) + "\t" + str(f11_sc))
                       m_f1[iter1].write('\n')
                   
                       #cnt = cnt + 1
                       #print cnt
                       #break
                    elif tr_gap != [''] and sys_gap == ['']:
                      

                       #cnt = cnt + 1
                       #print cnt
                       #break    


                       tp = 0
                       fp = 0
                       fn = len(tr_gap)
                       prec = float(0.0)
                       rec = float(0.0)
                       f1_sc = float(0.0)


                       tps[iter1].write(str(idd) + "\t" + str(tp))
                       tps[iter1].write('\n')
                       fps[iter1].write(str(idd) + "\t" + str(fp))
                       fps[iter1].write('\n')
                       fns[iter1].write(str(idd) + "\t" + str(fn))
                       fns[iter1].write('\n')
                       m_prec[iter1].write(str(idd) + "\t" + str(prec))
                       m_prec[iter1].write('\n')
                       m_rec[iter1].write(str(idd) + "\t" + str(rec))
                       m_rec[iter1].write('\n')

                 
                       m_f1[iter1].write(str(idd) + "\t" + str(f1_sc))
                       m_f1[iter1].write('\n')

                                                 




                    elif tr_gap == [''] and sys_gap != ['']:  
                       tp = 0
                       fp = len(sys_gap)
                       fn = 0

                       prec = float(0.0)
                       tps[iter1].write(str(idd) + "\t" + str(tp))
                       tps[iter1].write('\n')
                       fps[iter1].write(str(idd) + "\t" + str(fp))
                       fps[iter1].write('\n')
                       m_prec[iter1].write(str(idd) + "\t" + str(prec))
                       m_prec[iter1].write('\n')

                       rec = float(0.0)
                       fns[iter1].write(str(idd) + "\t" + str(fn))
                       fns[iter1].write('\n')
                   
                       m_rec[iter1].write(str(idd) + "\t" + str(rec))
                       m_rec[iter1].write('\n')

                      
                       f11_sc = float(0.0)
                       m_f1[iter1].write(str(idd) + "\t" + str(f11_sc))
                       m_f1[iter1].write('\n')

                       #cnt = cnt + 1
                       #print cnt
                       #break 
                   



                    #if tr_gap != [''] and sys_gap != ['']:
                    else:

                       tp = 0
                       arr_tr = []
                       for a in sys_gap:
                    
                           simi_b = []
                    
                           for bb in tr_gap:
                                              
                              
                               scores = rouge.get_scores(a, bb)
                              
                               simi_b.append(float(scores[0]['rouge-2']['f']))    # ROUGE-2 F1-score is used as the similarity score between true gap and predicted gap.                            
                    
                           if any(x >= float(r1) for x in simi_b):
                              m1 = max(simi_b)
                              ind = simi_b.index(m1)
                              if arr_tr != []:
                                 if tr_gap[ind] not in arr_tr: 
                                    tp = tp + 1
                                    arr_tr.append(tr_gap[ind])

                              else:
                                 tp = tp + 1
                                 arr_tr.append(tr_gap[ind])

                           
                       
                           else:
                              tp = tp

                      
                       fp = 0
                       arr_tr1 = []

                       for a in sys_gap:
                    
                           simi_b = []
                    
                           for bb in tr_gap:
                       
                                                             
                               scores = rouge.get_scores(a, bb)
                               
                               simi_b.append(float(scores[0]['rouge-2']['f']))

                           
                    
                           if all(x < float(r1) for x in simi_b):
                              m1 = max(simi_b)
                              ind = simi_b.index(m1)
                              if arr_tr1 != []:
                                 if tr_gap[ind] not in arr_tr1: 
                                    fp = fp + 1
                                    arr_tr1.append(tr_gap[ind])

                              else:
                                 fp = fp + 1
                                 arr_tr1.append(tr_gap[ind])

                           
                       
                           else:
                              fp = fp                   


   
                                     

                       tps[iter1].write(str(idd) + "\t" + str(tp))
                       tps[iter1].write('\n')
                       fps[iter1].write(str(idd) + "\t" + str(fp))
                       fps[iter1].write('\n')
                     
                       prec = float(tp)/float(tp + fp)
                       m_prec[iter1].write(str(idd) + "\t" + str(prec))
                       m_prec[iter1].write('\n')

                       fn = 0
                       arr_sys = []
                       for ii in tr_gap:
                           simi_c = []
                           for jj in sys_gap:
                             

                               scores = rouge.get_scores(jj, ii)   # a: hypothesis, bb: reference
                            
                               simi_c.append(float(scores[0]['rouge-2']['f']))
                   
                           
                    
                           if all(x < float(r1) for x in simi_c):
                       
                              
                              m1 = max(simi_c)
                              ind = simi_c.index(m1)
                              if arr_sys != []:
                                 if sys_gap[ind] not in arr_sys: 
                                    fn = fn + 1
                                    arr_sys.append(sys_gap[ind])

                              else:
                                 fn = fn + 1
                                 arr_sys.append(sys_gap[ind])
                       
                           else:
                              fn = fn                      

                      
                       fns[iter1].write(str(idd) + "\t" + str(fn))
                       fns[iter1].write('\n')

                       rec = float(tp)/float(tp + fn)
                       m_rec[iter1].write(str(idd) + "\t" + str(rec))
                       m_rec[iter1].write('\n')

                

                       f1_sc = float(2 * tp)/float((2 * tp) + fn + fp)

               
                       m_f1[iter1].write(str(idd) + "\t" + str(f1_sc))
                       m_f1[iter1].write('\n')                    

                  
              

   


               
    cnt = cnt + 1
    print cnt



import numpy as np

# ds is the dataset either University of North Texas dataset or SciEntsBank or Beetle dataset, in which total-dir.txt is comprised of student answers in which the directionality information in their respective answer graphs is of utmost importance for better understanding and nodir.txt is comprised of student answers where the directionality information is not vital


with open('location-where-wish-to-store-files/'+ds+'/total-dir.txt') as kfile1:

     ques = []
     for num, line in enumerate(kfile1, 1):
     #for line in kfile:
         #xx = nltk.word_tokenize(line)
         #xx = line.split("\t")
         xx = line.split("  ")
         #print xx
         idd = xx[0]
      
         if ds == 'rada':
            idd1 = idd.split(".")
            idd2 = ".".join(idd1[0:2])
            #print idd2
            ques.append(idd2)
         
         elif ds == 'ScientsBank':
             idd1 = idd.split(".")
             idd2 = ".".join(idd1[0:2])
             #print idd2
             ques.append(idd2)
             
         elif ds == 'Beetle':
            idd1 = idd.split(".")
            ques.append(idd1[0])


     quesnp = np.array(ques)
     ques_uniq = np.unique(quesnp)
     ll = list(ques_uniq)        # extract the set of unique questions in each dataset 'ds'. 

     print ll

     print len(ll)








fl4 = ['location-where-wish-to-store-files/thres=' + r1 + '/'+ds+'/'+ type_file +'/m_prec/m_prec'+"_"+str(i)+".txt" for i in range(1,3)] 
m_prec = [open(fl4[j], "r") for j in range(len(fl4))]


macro_avg_prec= []

for kk in range(len(m_prec)):
    m1 = m_prec[kk].readlines()    

    queswise_prec = [[] for i in range(len(ll))]
    for jj in range(0, len(ll)):      
     
        for line in m1:
            
            id_value = line.split("\t")
            
            id1 = id_value[0].split(".")
           
            if ds == 'Beetle':
               id2 = id1[0]
              
            else:
               id2 = ".".join(id1[0:2])          

            
            if id2 == ll[jj]:
               queswise_prec[jj].append(float(id_value[1].rstrip()))

   

    ques_means = []

    for jj in range(0, len(ll)):
     
        ques_means.append(np.mean(queswise_prec[jj]))

    macro_avg_prec.append('model' + " " + str(kk + 1) + ":"+" " + str(np.mean(ques_means)))


print macro_avg_prec

  



macro_avg_rec = []

fl5 = ['location-where-wish-to-store-files/thres=' + r1 + '/'+ds+'/'+ type_file +'/m_rec/m_rec'+"_"+str(i)+".txt" for i in range(1,3)] 
m_rec = [open(fl5[j], "r") for j in range(len(fl5))]


for kk in range(len(m_rec)):
    m1 = m_rec[kk].readlines()
    #print m1

    queswise_rec = [[] for i in range(len(ll))]
    for jj in range(0, len(ll)):      

        for line in m1:
            id_value = line.split("\t")
            id1 = id_value[0].split(".")

            if ds == 'Beetle':
               id2 = id1[0]
            else:
               id2 = ".".join(id1[0:2])

            if id2 == ll[jj]:

               queswise_rec[jj].append(float(id_value[1].rstrip()))


    ques_means = []

    for jj in range(0, len(ll)):
     
        ques_means.append(numpy.mean(queswise_rec[jj]))  


    macro_avg_rec.append('model' + " " + str(kk + 1) + ":"+ " " + str(numpy.mean(ques_means)))

print macro_avg_rec



macro_avg_f1 = []

fl6 = ['location-where-wish-to-store-files/thres=' + r1 + '/'+ds+'/'+ type_file +'/m_f1/f1'+"_"+str(i)+".txt" for i in range(1,3)] 
m_f1 = [open(fl6[j], "r") for j in range(len(fl6))]


for kk in range(len(m_f1)):
    m1 = m_f1[kk].readlines()
   
    queswise_f1 = [[] for i in range(len(ll))]
    for jj in range(0, len(ll)):      


        for line in m1:
            id_value = line.split("\t")
            id1 = id_value[0].split(".")
            if ds == 'Beetle':
               id2 = id1[0]
            else:
               id2 = ".".join(id1[0:2])
            

            if id2 == ll[jj]:

               queswise_f1[jj].append(float(id_value[1].rstrip()))




    ques_means = []

    for jj in range(0, len(ll)):
     
        ques_means.append(numpy.mean(queswise_f1[jj]))  


 


    macro_avg_f1.append('model' + " " + str(kk + 1) + ":" + " " + str(numpy.mean(ques_means)))

print macro_avg_f1










    


    











        
        
        
        
                    
        



  








       


           
           
           
    

















                
         
