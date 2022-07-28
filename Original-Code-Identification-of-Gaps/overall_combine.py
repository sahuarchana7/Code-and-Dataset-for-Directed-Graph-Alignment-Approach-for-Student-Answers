import nltk
from nltk import word_tokenize
import os
#import subprocess
from xml.dom import minidom
#import linecache
from nltk.translate.bleu_score import modified_precision
from nltk.corpus import stopwords
import numpy
from gensim.models.keyedvectors import KeyedVectors
import subprocess
from subprocess import Popen, PIPE
from subprocess import*



stop = stopwords.words('english')
dic = {'-LRB-':'(', '-RRB-':')', '<STOP>':''}

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


def getOutputFromJava(*args):
	process = Popen(['java', '-jar']+list(args), stdout=PIPE, stderr=PIPE)
	ret = []
	while process.poll() is None:
		line = process.stdout.readline()
		if line != '' and line.endswith('\n'):
			ret.append(line[:-1])
	stdout, stderr = process.communicate()
	ret += stdout.split('\n')
	if stderr != '':
		ret += stderr.split('\n')
	ret.remove('')
	op = string.join(ret, "")
	return op;







ctt = 0
cnt = open('/location-to-store-output-files/count.txt', 'a')

fqq = open('/location-to-store-output-files/all_questions.txt', 'r')
fqq1 = fqq.readlines()




f1_s = open('/location-to-store-output-files/student-model/sc_student.csv', 'r')  # SciEntsBank dataset shown for illustration purpose
f11 = f1_s.readlines()


f2_m = open('/location-to-store-output-files/student-model/sc_model.csv', 'r')   # model answers for SciEntsBank dataset shown here for illustration purpose
 

f22 = f2_m.readlines()






tau_values = [0.5]         # a grid-search can be done over tau_values varying from 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0

filenames1 = ['/location-to-store-output-files/final_gaps/final_gapsold1'+"_"+str(i)+".txt" for i in tau_values]                             # 
files = [open(filenames1[j], "a") for j in range(len(filenames1))]








for line in f11:     # student-answers.txt    
     
    xx = line.split("\t") 
    st_id = xx[0]                     # imp to be written to final gaps file
    xx1 = xx[0].split(".")
    if len(xx1) == 3:                          # UNT
       xx2 = ".".join(xx1[0:2])
    elif len(xx1) == 4:                         # ScientsBank
       xx2 = ".".join(xx1[0:2])
       
    elif len(xx1) == 2:                       # Beetle
       xx2 = xx[0]
    


   
         
    for j in f22:                      # model-answers.txt       
         
        n = j.split("\t") 
        
        n1 = n[0].split(".")                 
        if len(n1) == 2:                       #  UNT or Beetle
           n5 = n[0]

        else:
            
            n5 = n[0]
            


        
        
        if st_id == n5:
           
           xfinal = xx[1]
           yfinal = n[1]

           
           n6 = n5.split(".")
           n7 = n6[0]

           n8 = ".".join(n6[0:2])
            

           for jj in fqq1:
               jj1 = jj.split("  ")
               jj2 = jj1[0].split("-")
               jj3 = jj2[0].split("_")
               jj4 = ".".join(jj3[:])
               
               if n5 == jj1[0]:         #unt
                 
                  qfinal = jj1[1]
                  qfinal = qfinal.lower()
                  
                  break

               

               elif n7 == jj1[0]:           #Beetle
                    qfinal = jj1[1] 
                    qfinal = qfinal.lower()
                   
                    break 


              
               elif n8 == jj4:
                    qfinal = jj1[1]
                    qfinal = qfinal.lower()
                    
                    break


                      

            
           f3 = open('/location-to-store-output-files/m.txt', 'w')
           f3.write(yfinal)
           f4 = open('/location-to-store-output-files/s1.txt', 'w')
           f4.write(xfinal)
           f3.close()
           f4.close()

           

           try:
              #os.system("sh ./p2_updatenew.sh /home/archana/latest_FA_dir/FA_directed/TLT-paper2/all_clusters48.txt") 
              os.system("sh /location-to-store-output-files/p2_updatenew.sh") 
           
              
  
                
               
              
   
              #tau_values = [0.5]                 

              file_names = ['/location-to-store-output-files/old_gaps/sys_gapsold'+"_"+str(i)+'.txt' for i in range(1,4)] 
              
              file_s = [open(file_names[j], "r") for j in range(len(file_names))]             
             

          



              for k in range(len(file_s)):
                  final_gaps = []
                  fs1 = file_s[k].readlines()
                  for line in fs1:
                      line = line.strip()
                      line = line.lower()

                      if line not in qfinal:
                         final_gaps.append(line)

                   

                  final_gaps1 = []                  
                   

                  fg = set(final_gaps)

                  for ix in fg:
                      final_gaps1.append(ix)                        # with question demotion           
                   
                  files[k].write(st_id + "\t" +str(final_gaps1))
                  files[k].write('\n')
               
                  file_s[k].close()
                 

               
               
              

              for kk in file_names:
               os.remove(kk)
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
            
          
              os.remove('/location-to-store-output-files/outs.txt')
              os.remove('/location-to-store-output-files/outs_1.txt')
              os.remove('/location-to-store-output-files/outs_23.txt')
              os.remove('/location-to-store-output-files/outs_24.txt')
            

              os.remove('/location-to-store-output-files/m.txt')
              os.remove('/location-to-store-output-files/s1.txt')
              os.remove('/location-to-store-output-files/1_inp1.txt')
              os.remove('/location-to-store-output-files/2_inp1.txt')
              os.remove('/location-to-store-output-files/wouts_2.txt')
              os.remove('/location-to-store-output-files/woutm_2.txt')
              os.remove('/location-to-store-output-files/wouts_2new.txt')
              os.remove('/location-to-store-output-files/woutm_2new.txt')

              os.remove('/location-to-store-output-files/FA_err1.txt') 

             
           

           
            
 
              ctt = ctt + 1
              print ctt
              cnt.write(str(ctt))
              cnt.write('\n')


           except:
              for k1 in range(len(files)):
                  files[k1].write(st_id + "\t" + "error")
                  files[k1].write('\n')
                 


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
            
          
              os.remove('/location-to-store-output-files/outs.txt')
              os.remove('/location-to-store-output-files/outs_1.txt')
              os.remove('/location-to-store-output-files/outs_23.txt')
              os.remove('/location-to-store-output-files/outs_24.txt')
            

              os.remove('/location-to-store-output-files/m.txt')
              os.remove('/location-to-store-output-files/s1.txt')
              os.remove('/location-to-store-output-files/1_inp1.txt')
              os.remove('/location-to-store-output-files/2_inp1.txt')
              os.remove('/location-to-store-output-files/wouts_2.txt')
              os.remove('/location-to-store-output-files/woutm_2.txt')
           
              os.remove('/location-to-store-output-files/wouts_2new.txt')
              os.remove('/location-to-store-output-files/woutm_2new.txt')
              os.remove('/location-to-store-output-files/FA_err1.txt') 

              ctt = ctt + 1
              print ctt
              cnt.write(str(ctt))
              cnt.write('\n')
              



                   
                   
                 
   
cnt.close()
fqq.close()
f1_s.close()
f2_m.close()
