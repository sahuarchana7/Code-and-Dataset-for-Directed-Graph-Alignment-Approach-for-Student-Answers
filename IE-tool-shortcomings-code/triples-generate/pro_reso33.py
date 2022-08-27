import nltk
from nltk import word_tokenize
from xml.dom import minidom

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def pronoun_resolve(fs_tag):
    
    
    f1 = fs_tag.read()

    f2 = '<root>' + f1 + '</root>'

    f3 = open('/location-where-to-store-output-files/mm.tagged', 'w')

    f3.write(f2)
    f3.close()
    return (f3)




fs_tag = open('/location-where-to-store-output-files/m.tagged', 'r')   # running the shell script arkref.sh generates m.tagged file


f3= pronoun_resolve(fs_tag)



f = open('/location-where-to-store-output-files/m.txt', 'r')

f1 = f.read()


text = word_tokenize(f1)
text_pos = nltk.pos_tag(text)     # POS tagging of model answer text


A = [i[0] for i in text_pos]      # word
B = [i[1] for i in text_pos]      # part-of-speech


dom = minidom.parse('/location-where-to-store-output-files/mm.tagged')
conference=dom.getElementsByTagName('mention')


a = []
for node in conference:
  
    conf_no=node.getAttribute('entityid')
    
    a.append(conf_no)


b = [[] for k in range(0, len(a))]



for node in conference:
    conf_no=node.getAttribute('entityid')
     
    
    if len(conf_no) == 1:
        conf = int(conf_no)
    else:
        conf_no = conf_no.split("_")
        conf = int(conf_no[0])
    
    
    
    if node.firstChild.nodeValue != None:
       
       v11 = node.firstChild.nodeValue
       
       
       b[conf - 1].append(v11)
       


f.close()

ll = []
for i in range(0, len(b)):
    l = len(b[i])
    ll.append(l)





    
      
       
def pronoun_reso(b):

    for i in range(0, len(b)):
        
    
        if len(b[i]) > 1:
           pp = []
           indx = []
           rep = []
           indd = []
       
           for j in range(0, len(b[i])): 
                         
               b1 = b[i][j].split(" ")   
               
        
               if len(b1) == 1:              
                  if b1[0] in A:                
                     I = A.index(b1[0])                 
                     part = B[I]
                 
                     if part == 'PRP': 
                        pp.append(b1[0])
                        indx.append(I)                    
                        indd.append("h")

                     if part == 'PRP$':               
                    
                        pp.append(b1[0])                    
                        indx.append(I)
                        indd.append("k")
                             
               else:
                 rep.append(b1)
         
      
           repp1 = []
           

           if rep == []:
              for i in range(0, len(indx)):
                  if indd[i] == "k":
                     repp1.append(pp[0])
                  else:
                     repp1.append(pp[0])
           else:              
              


              for i in range(0, len(indx)):
                  if indd[i] == "k":
                     repp1.append(" ".join(rep[0][:])+"'s")
                  else:
                     repp1.append(" ".join(rep[0][:]))

       

       
           for (index, replacement) in zip(indx, repp1):
          
                A[index] = replacement         
                A2 = " ".join(A[:])
     
    return A2;      
        

           
if "PRP" in B:    
    if any(i > 1 for i in ll) == True:
      
       A2 = pronoun_reso(b)
       f = open('/location-where-to-store-output-files/pro_opm.txt', 'w')
       
       f.write(A2)
       f.close()
       
else:
   
   f = open('/location-where-to-store-output-files/m.txt', 'r')
   f1 = f.read()
   
   fm = open('/location-where-to-store-output-files/pro_opm.txt', 'w')
   
   fm.write(f1)
   
   fm.close()
   f.close()       




       




