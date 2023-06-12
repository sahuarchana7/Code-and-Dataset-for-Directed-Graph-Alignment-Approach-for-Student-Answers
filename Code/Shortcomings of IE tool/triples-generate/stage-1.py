# this is code for generating triples in model answer-student answer in dataset



import nltk
from nltk import word_tokenize
import os, shutil

from xml.dom import minidom

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




dataset = 'UNT' # SciEntsBank or Beetle


ctt = 0
cnt = open('/location-where-to-store-output-files'+'/'+dataset+'/'+ 'count.txt', 'a')

f1_s = open('/location-where-to-store-output-files'+'/'+dataset+'/'+ 'student-ans.txt', 'r')    # student-ans.txt is the file containing student answers of University of North Texas dataset or that of SciEntsBank or Beetle dataset.  


f11 = f1_s.readlines()

f2_m = open('/location-where-to-store-output-files'+'/'+dataset+'/'+'model-ans.txt', 'r')    # model-ans.txt is the file containing model answers of University of North Texas dataset or that of SciEntsBank or Beetle dataset.  

f22 = f2_m.readlines()

for line in f11:     # student-answers.txt    
     
    xx = line.split("  ") 
    st_id = xx[0]                     # student ans ID - imp to be written to final gaps file
    xx1 = xx[0].split(".")
    if len(xx1) == 3:                          # if student answers belong to UNT dataset
       xx2 = ".".join(xx1[0:2])
    elif len(xx1) == 4:                         # if student answers belong to SciEntsBank dataset
       xx2 = ".".join(xx1[0:2])
       
    elif len(xx1) == 2:                       # if student answers belong to Beetle dataset
       xx2 = xx[0]  
   
         
    for j in f22:                      # model-answers.txt       
         
        n = j.split("\t") 
        
        n1 = n[0].split(".")                 
        if len(n1) == 2:                       #  UNT or Beetle
           n5 = n[0]

        else:
            
            n5 = n[0]                         # SciEntsBank dataset
            


        
       
        if st_id == n5:
          
           xfinal = xx[1]
           yfinal = n[1]

          

           n6 = n5.split(".")
           n7 = n6[0]

           n8 = ".".join(n6[0:2])
                     
                          
            
           f3 = open('/location-where-to-store-output-files'+'/'+'m.txt', 'w')     # m.txt is model answer
           f3.write(yfinal)
           f4 = open('/location-where-to-store-output-files'+'/' +'s1.txt', 'w')    # s1.txt is student answer in a pair belonging to a question
           f4.write(xfinal)
           f3.close()
           f4.close()

            
           os.system("sh '/location-where-to-store-output-files/generate_triples.sh")    # this shell script contains python code for pronoun resolution on each model answer- student answer pair followed by generation of triples using CLAUSIE information extraction tool. 

           os.mkdir('/location-where-to-store-output-files/triples/'+ dataset + '/'+st_id)

           

           source1 = '/location-where-to-store-output-files/outm_1.txt'
           source2 = '/location-where-to-store-output-files/outs_1.txt'


           

           destination1 = '/location-where-to-store-output-files/triples/'+dataset+'/'+st_id+'/'+'outm_1.txt'
           destination2 = '/location-where-to-store-output-files/triples/'+dataset+'/'+st_id+'/'+'outs_1.txt'

           

           dest1 = shutil.move(source1, destination1)
           dest2 = shutil.move(source2, destination2)


           
              
               

           os.remove('/location-where-to-store-output-files/ss.tagged')
           os.remove('/location-where-to-store-output-files/mm.tagged')
           os.remove('/location-where-to-store-output-files/s1.tagged')
           os.remove('/location-where-to-store-output-files/s1.osent')
           os.remove('/location-where-to-store-output-files/s1.sst')
           os.remove('/location-where-to-store-output-files/s1.parse')
           os.remove('/location-where-to-store-output-files/m.tagged')
           os.remove('/location-where-to-store-output-files/m.osent')
           os.remove('/location-where-to-store-output-files/m.parse')
           os.remove('/location-where-to-store-output-files/m.sst')
           os.remove('/location-where-to-store-output-files/pro_opm.txt')
           os.remove('/location-where-to-store-output-files/pro_ops.txt')
           os.remove('/location-where-to-store-output-files/outm.txt')        
            
          
           os.remove('/location-where-to-store-output-files/outs.txt')       
           
           os.remove('/location-where-to-store-output-files/m.txt')
           os.remove('/location-where-to-store-output-files/s1.txt')
           os.remove('/location-where-to-store-output-files/1_inp1.txt')
           os.remove('/location-where-to-store-output-files/2_inp1.txt')         
              
 
           ctt = ctt + 1
           print ctt
           cnt.write(str(ctt))
           cnt.write('\n')
           break      



                   

cnt.close()

f1_s.close()
f2_m.close()

