import nltk
from nltk.tag.stanford import StanfordPOSTagger as POS_Tag
st = POS_Tag(model_filename='/location-to-store-output-files/stanford-postagger-2018-10-16/models/english-bidirectional-distsim.tagger', path_to_jar='/location-to-store-output-files/stanford-postagger-2018-10-16/stanford-postagger.jar')


def remove_punc(string):
    
    punctuations = '''"'''

    no_punct = ""
    for char in string:
        if char not in punctuations:
           no_punct = no_punct + char


    return(no_punct)




f2 = open('/location-to-store-output-files/outm_1.txt', 'w')

lookup = '1\t'
with open('/location-to-store-output-files/outm.txt') as f:
     f1 = f.readlines()
     for num, line in enumerate(f1):
        if lookup in line:
            
            f2.write(str(f1[num]))
           

f.close()
f2.close()


g = open('/location-to-store-output-files/woutm_2.txt', 'a')
f = open('/location-to-store-output-files/outm_1.txt', 'r')
f1 = f.readlines()
for line in f1:
    
    aa = remove_punc(line)
    
    aa1 = aa.split("\t")
    aa2 = aa1[1:]
    
    if len(aa2) == 3:
       aa3 = "\t".join(aa2[:])
       g.write(aa3)
       g.write('\n')
    else:
       xx = aa1[-1]
       xxs = xx.split()
       if len(xxs) != 1:
          n1 = st.tag(xxs)
          
       
          ab = []
          for x in n1[::-1]:
              y = x[1]
              yy = y[0:2]
              if yy == "VB":
                 ab.append(x[0])
                 

          
       
       

         

          
          ac = []
          for ii in n1:
              if ii[0] != ab[0]: 
                 ac.append(ii[0])
              
              else:
                 ac.append(ii[0])
                 break

          #print ac                                # pick up the words having part-of-speech till VB   # modifying triples

          jjnew = []
          aa11 = aa1[:-1]
          
          for jj in aa11:
              jjnew.append(jj)

          jjnew.append(" ".join(ac[:]))
       
       
          jjnew.append(n1[-1][0])

       

          jj1 = "\t".join(jjnew[1:])

          g.write(jj1)
          g.write('\n')
           
           

              
              
              
              
f.close()
g.close()



f2 = open('/location-to-store-output-files/outs_1.txt', 'w')

lookup = '1\t'
with open('/location-to-store-output-files/outs.txt') as f:
     f1 = f.readlines()
     for num, line in enumerate(f1):
        if lookup in line:
            
            f2.write(str(f1[num]))
           

f.close()
f2.close()


g = open('/location-to-store-output-files/wouts_2.txt', 'a')
f = open('/location-to-store-output-files/outs_1.txt', 'r')
f1 = f.readlines()

if len(f1) > 1:
   for line in f1:
       
       aa = remove_punc(line)
   
       aa1 = aa.split("\t")
       aa2 = aa1[1:]
       if len(aa2) == 3:
          aa3 = "\t".join(aa2[:])
          g.write(aa3)
          g.write('\n')

       else:
          xx = aa1[-1]
          xxs = xx.split()
          if len(xxs) != 1:
             n1 = st.tag(xxs)
             
       
             ab = []
             for x in n1[::-1]:
                 y = x[1]
                 yy = y[0:2]
                 if yy == "VB":
                    ab.append(x[0])
                    break

                 


          
       
       

             if ab != []:                
                

                ac = []
                for ii in n1:
                    if ii[0] != ab[0]: 
                       ac.append(ii[0])
              
                    else:
                       ac.append(ii[0])
                       break

             #print ac                                # pick up the words having part-of-speech till VB   # modifying triples

                jjnew = []
                aa11 = aa1[:-1]
             
                for jj in aa11:
                    jjnew.append(jj)

                jjnew.append(" ".join(ac[:]))
       
             
                jjnew.append(n1[-1][0])

             

                jj1 = "\t".join(jjnew[1:])

                g.write(jj1)
                g.write('\n')

             else:

                g.write('')
          

          else:

             
             an1 = []
             an1.append(aa2[0])
             an1.append('pred')
             an1.append(aa2[1])

             jj1 = "\t".join(an1[0:])

             g.write(jj1)
             g.write('\n')
             


else:
    for line in f1:
    
       aa = remove_punc(line)
    
       aa1 = aa.split("\t")
       aa2 = aa1[1:]
       
       if len(aa2) == 3:
          aa3 = "\t".join(aa2[:])
          g.write(aa3)
          g.write('\n')
       else:         


          xx = aa1[-1]
          xxs = xx.split()
          if len(xxs) != 1:
             n1 = st.tag(xxs)
             
             
             
          
       
             ab = []
             for x in n1[::-1]:
                 y = x[1]
                 yy = y[0:2]
                 if yy == "VB":
                    ab.append(x[0])
                    break

         
       
       

             ac = []
             for ii in n1:
                 if ii[0] != ab[0]: 
                    ac.append(ii[0])
              
                 else:
                    ac.append(ii[0])
                    break

             #print ac                                # pick up the words having part-of-speech till VB   # modifying triples

             jjnew = []
             aa11 = aa1[:-1]
             
             for jj in aa11:
                 jjnew.append(jj)

             jjnew.append(" ".join(ac[:]))
       
             
             jjnew.append(n1[-1][0])

             

             jj1 = "\t".join(jjnew[1:])

             g.write(jj1)
             g.write('\n')





f.close()
g.close()


g = open('/location-to-store-output-files/outm_23.txt', 'a')

f = open('/location-to-store-output-files/woutm_2.txt', 'r')
f1 = f.readlines()


for line in f1:
    line = line.split("\t")
    
    a = []
    b = []
    for i in line:        
        j = i.split(" ")
        if "and" in j:
            
            ind = j.index("and")
            a.append(j[0:ind])
            b.append(j[(ind+1):])
            
        else:
            a.append(j)
            b.append(j)
    

    a_1 = []
    b_1 = []
    for k in a:
       
        m = " ".join(k[:])
        
        a_1.append(m)
    

    if "\n" not in a_1[-1]:
       
       a_1[-1] = a_1[-1] + '\n'
   

    for k in b:
        
        n = " ".join(k[:])
        
        b_1.append(n)
    

    if "\n" not in b_1[-1]:
       
       b_1[-1] = b_1[-1] + '\n'


    

    a_2 = "\t".join(a_1[:])
    b_2 = "\t".join(b_1[:])
    
    
    g.write(a_2)
    
    g.write(b_2)
    

f.close()
g.close()

g = open('/location-to-store-output-files/outm_23.txt', 'r')
g1 = g.readlines()
g2 = set(g1)


g3 = []
for i in g2:
    if i != '\n':
       g3.append(i)

g.close()



gs = open('/location-to-store-output-files/outm_24.txt', 'a')
for xx in g3:
    gs.write(xx)
   
gs.close()
   

    



g = open('/location-to-store-output-files/outs_23.txt', 'a')

f = open('/location-to-store-output-files/wouts_2.txt', 'r')
f1 = f.readlines()


for line in f1:
    line = line.split("\t")
    
    a = []
    b = []
    for i in line:
        
        j = i.split(" ")
        if "and" in j:
            
            ind = j.index("and")
            a.append(j[0:ind])
            b.append(j[(ind+1):])
            
        else:
            a.append(j)
            b.append(j)
    


    a_1 = []
    b_1 = []
    for k in a:
        
        m = " ".join(k[:])
       
        a_1.append(m)
    

    if "\n" not in a_1[-1]:
      
       a_1[-1] = a_1[-1] + '\n'
    

    for k in b:
        
        n = " ".join(k[:])
       
        b_1.append(n)
    

    if "\n" not in b_1[-1]:
       
       b_1[-1] = b_1[-1] + '\n'


    

    a_2 = "\t".join(a_1[:])
    b_2 = "\t".join(b_1[:])
    
    
    g.write(a_2)
    
    g.write(b_2)
    

f.close()
g.close()

g = open('/location-to-store-output-files/outs_23.txt', 'r')
g1 = g.readlines()
g2 = set(g1)
g3 = []
for i in g2:
    if i != '\n':
       g3.append(i)

g.close()



gs = open('/location-to-store-output-files/outs_24.txt', 'a')
for xx in g3:
    gs.write(xx)    
gs.close()
    

    



# code for clustering of predicates

