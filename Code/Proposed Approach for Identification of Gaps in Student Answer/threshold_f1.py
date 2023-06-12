import os
import sys

def remove_punc(string):    
   
    punctuations = ['[', ']']

    no_punct = ""
    for char in string:
       
        if char not in punctuations:
           no_punct = no_punct + char

# display the unpunctuated string

    
    return(no_punct)


def remove_punc1(string):
    
    
    punctuations = ['(', ')']

    no_punct = ""
    for char in string:
        
        if char not in punctuations:
           no_punct = no_punct + char

# display the unpunctuated string

    
    return(no_punct)




def remove_punc2(string):
    
   
    punctuations = ["'"]

    no_punct = ""
    for char in string:
        
        if char not in punctuations:
           no_punct = no_punct + char

# display the unpunctuated string

   
    return(no_punct)








def system_gaps(sys_gaps_old, argument, tau):

    nodes_model = []
    
    f = open('/location-to-store-output-files/woutm_2.txt', 'r') ####    orig code
   
    f1 = f.readlines()
   
    for line in f1:
        if line != '\n':
           line = line.split('\t')
    
           tup = []
           tup.append(line[0])
           tup.append(line[1])
           tup.append(line[2].rstrip())

           nodes_model.append(tup)

    f.close()   

    sys_gaps_final = []
    for gp in sys_gaps_old:
   
        n1 = [item[2] for item in nodes_model if gp in item[0]]     # matching a gap in old_gaps with a node in model graph...extracting the neighbouring nodes from model answer graph.
    

        if n1 != []:
           if n1[0] in sys_gaps_old:       # if the neighboring node of MA graph also in old_gaps, then some sense for gap to occur (useful for extracting gaps in student answers)
         
              n11 = [item[1] for item in nodes_model if gp in item[0]] 
              n12 = n11[0]
              gp1 = gp +" "+n12+" "+n1[0]
              sys_gaps_final.append(gp1)                      # phrasal gaps extracted very good for definition-type answers
          
           else:
      
              sys_gaps_final.append(gp)     # both lone nodes (single node gaps) as well as phrasal gaps are being taken 



        else:

           n1_1 = [item[0] for item in nodes_model if gp in item[2]]  

           if n1_1 != []:
       
              if n1_1[0] in sys_gaps_old:       # if the neighboring node of MA graph also in old_gaps, then some sense for gap to occur (useful for extracting gaps in student answers)
         
                 n11 = [item[1] for item in nodes_model if gp in item[0]] 
                 if n11 != []:
                    n12 = n11[0]
                    gp1 = gp +" "+n12+" "+n1_1[0]
                    sys_gaps_final.append(gp1)
           
              else:
       
                 sys_gaps_final.append(gp)     # both lone nodes (single node gaps) as well as phrasal gaps are being taken 
    
    
    
    

    
    ss = []
    for ii in sys_gaps_final:
    
        sa = []
        ii = ii.lower()
        for jj in sys_gaps_final:
            jj = jj.lower()
            if jj != ii:                     # unique gaps are being taken
               sa.append(jj)
        if not any(ii in s for s in sa):
               ss.append(ii)


    #print ss
    
    f = open('/location-to-store-output-files/old_gaps/sys_gapsold'+"_"+str(argument)+"_"+str(tau)+'.txt', 'a')
   
    for j in ss:
        
        f.write(str(j))
        f.write('\n')
    f.close()



def best_filter(argument):


    
    cmdstr = 'python /location-to-store-output-files/profit_matrix_new.py' + " " + str(argument)
    os.system(cmdstr)
   
    os.system('python /location-to-store-output-files/hungarian.py')


    f = open('/home/location-to-store-output-files/best_filter/profit_matrix.txt', 'r')
    f1 = f.readlines()
    #print f1
    a = f1[0]
    #a = "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]"
    #profit_matrix = a
    
    aa = a.split("], [")
    

    profit_matrix = []
    for i in aa:
        i1 = remove_punc(i)
        
        i1 = i1.replace(" ", "")
        j = i1.split(",")
        
        profit_matrix.append(j)

   

    f.close()


    f = open('/location-to-store-output-files/best_filter/tuple_pairs2_u.txt', 'r')
    tuple_pairs2_u = f.readlines()
    f.close()


    new_t2 = []
    tt2_u = tuple_pairs2_u[0].split(", ")
    for x in tt2_u:
        x1 = remove_punc(x)
        
        new_t2.append(x1)                           # nodes from student answer

    



    f = open('/location-to-store-output-files/best_filter/tuple_pairs1_u.txt', 'r')
    tuple_pairs1_u = f.readlines()
    f.close()

    new_t1 = []
    tt1_u = tuple_pairs1_u[0].split(", ")
    for x in tt1_u:
        x1 = remove_punc(x)
        
        new_t1.append(x1)                       # nodes from model answer

    


    f = open('/location-to-store-output-files/hungarian_results.txt', 'r')
    f1 = f.readlines()     # ('Results:\n\t', [(2, 1), (1, 3), (0, 2)])
    


    
    j1 = remove_punc(f1[0])
    j11 = j1.split(", (")
        
   

    k11 = []
    for k in j11:
        
        k1 = remove_punc1(k)
        
        k2 = k1.split(",")
        
        k3 = [k22.replace(" ", "") for k22 in k2]
         
        k33 = [int(iter1) for iter1 in k3]
        k11.append(k33)   

    f.close()

    print k11                                # this contains node-pairs obtained as output of Hungarian algorithm   
        
        

    
    
 
    cc = []
    for i in k11:
       
        pp1 = profit_matrix[i[0]][i[1]]    # profit matrix is constructed s.t. the nodes of smaller answer appear as rows, nodes of larger answer appear as columns

        if len(new_t1) < len(new_t2) or len(new_t1) == len(new_t2):  # if length of model answer graph is less than or equal to length of student answer graph
           t1 = new_t1[i[0]]              # model answer is smaller one...i[0] refers to index that shud be taken from the smaller graph that leads to being nodes of MA graph
           t2 = new_t2[i[1]]               # i[1] refers to index that shud be taken from bigger graph.. here nodes of SA graph
        else:
           t2 = new_t2[i[0]]              # student answer is smaller one...i[0] refers to index that shud be taken from nodes of SA graph
           t1 = new_t1[i[1]]              # i[1] refers to index taken from bigger graph...here it is MA graph       

        

        bb = []
        t1 = t1.replace("'", "")
        t2 = t2.replace("'", "")
        bb.append(t1)      # model answer node first ... t1 will always contain MA node
        bb.append(t2)      # student answer node then .... t2 will always contain SA node
        bb.append(pp1)     # similarity value
        cc.append(bb)         # hungarian results selected nodes are put in cc

    print cc


       
    
    f = open('/location-to-store-output-files/outm_24.txt', 'r')
    
    f1 = f.readlines()

    gg = []

    for line in f1:
        line = line.split("\t")
        aa = line[0]
        bb = line[-1]
        gg.append(aa)
        gg.append(bb.strip())



    gg1 = set(gg)

    gg2 = []

    for ii in gg1:
        gg2.append(ii)

    

    
    gg2new = []
    for ij in range(len(gg2)):
        
        tpp1 = [item[0] for item in cc]
        
        if gg2[ij] not in tpp1:
           gg2new.append(gg2[ij])     # if particular node of model answer graph not among hungarian results paired nodes....that is gap

        else:
           tpp2 = [item[2] for item in cc]   # sim values of hungarian results paired nodes
           tx1 = tpp1.index(gg2[ij])   # particular node of MA graph
           tpp3 = tpp2[tx1]            # hungarian results paired nodes ....sim value
           if float(tpp3) < 0.5:
              
              gg2new.append(gg2[ij])     # the sim-value corresponding to that node in MA graph           
           
           
      


   

    sys_gaps_old = []
    for i in set(gg2new):
        sys_gaps_old.append(i)


    

    system_gaps(sys_gaps_old, argument, tau)  
    f.close()    

     

   

    

    
    


def exact_filter(argument):

    if (argument != 13 and argument != 14 and argument != 15):

       import shutil

       
       source = '/home/archana/eclipse-workspace/graph_match/FA_err1.txt'
       destination = '/location-to-store-output-files/FA_err1.txt'

       dest = shutil.copyfile(source, destination) 


       tuple_pairs1 = []
       tuple_pairs2 = []
       tuple_sim = []
       tuple_init = []


       f = open('/location-to-store-output-files/FA_err1.txt', 'r')       
       f1 = f.readlines()
       for line in f1:
   
           line = line.split(": ")
           l1 = line[1].split(", ")
           l2 = l1[0].split("=")
           l3 = l2[1]                          # similarity value
           tuple_sim.append(l3)

           l4 = l1[1].split("=")
           l5 = l4[1]
           tuple_init.append(l5)               # initial similarity value init indicating simi measure based on word2vec 

   
           pairs = remove_punc(line[0])
           pp1 = pairs.split(',')
    
           tuple_pairs1.append(pp1[0])
           tuple_pairs2.append(pp1[1])
   
       f.close()

       tp = zip(tuple_pairs1, tuple_pairs2, tuple_sim, tuple_init)
    

       sigma_ff = []
           
       for tt in range(len(tp)):

           sigma_f = max(float(tp[tt][2]), float(tp[tt][3]))               
           sigma_ff.append(sigma_f)

       tp1 = zip(tuple_pairs1, tuple_pairs2, tuple_init, tuple_sim, sigma_ff)



       tp2 = [list(ele) for ele in tp1] 

       sorted_sigmaf = sorted(tp2, key = lambda x: x[4], reverse=True)

     
       tau_values = [0.5]

       for tau in tau_values:

           
           tpp = []
           for tt in sorted_sigmaf:     
           

               if float(tt[4]) >= float(tau):
                  tpp.append(tt)         

                            

           model_nodes1 = []
           model_nodes2 = []
           tpp_new = []
           for jj in range(len(tpp)):
               if tpp[jj][0] not in model_nodes1 and tpp[jj][1] not in model_nodes2:
                  model_nodes1.append(tpp[jj][0])
                  model_nodes2.append(tpp[jj][1])                 
                  
                  tpp_new.append(tpp[jj])
    
           #print tpp_new                          ## one-one mapping for exact filter  
        
        
   
           f = open('/location-to-store-output-files/woutm_2new.txt', 'r')    #### orig imp     
       
           f1 = f.readlines()

           gg = []

           for line in f1:
               line = line.split("\t")
               aa = line[0]
               bb = line[-1]
               gg.append(aa)
               gg.append(bb.strip())



           gg1 = set(gg)

           gg2 = []

           for ii in gg1:
               gg2.append(ii)

    
    
           gg2new = []
           for ij in range(len(gg2)):
        
               tpp1 = [item[0] for item in tpp_new]
        
               if gg2[ij] not in tpp1:
                  
                  gg2new.append(gg2[ij]) 


           #print gg2new             
    

           sys_gaps_old = []
           for i in set(gg2new):
               sys_gaps_old.append(i)


           #print sys_gaps_old
    

           system_gaps(sys_gaps_old, argument, tau)
           f.close()


    
    else:

       f = open('/location-to-store-output-files/tp.txt', 'r')
       f1 = f.readlines()

       tp = []
       for line in f1:
           line = line.split(", (")
           tp11 = []
 
           for ll in line:
               k1 = remove_punc1(ll)
               if '[' or ']' in k1:
                   k11 = remove_punc(k1)
               else:
                   k11 = k1
           
               k2 = k11.split(",")
               tp1 = []
               for kk in k2:
                   kk1 = remove_punc2(kk)
                   tp1.append(kk1)
               tp11.append(tp1)  
           tp.append(tp11)
       
       f.close()   


      


       

       model_nodes1 = []
       model_nodes2 = []
       tpp_new = []
       for jj in range(len(tpp)):
          
           if tpp[jj][0] not in model_nodes1:
              model_nodes1.append(tpp[jj][0])
              if tpp[jj][1] not in model_nodes2:
                 model_nodes2.append(tpp[jj][1]) 
                 tpp_new.append(tpp[jj])
    
       #print tpp_new                          ## one-one mapping for exact filter



       f = open('/location-to-store-output-files/outm_24.txt', 'r')      ##### imp orig
       

       f1 = f.readlines()

       gg = []

       for line in f1:
           line = line.split("\t")
           aa = line[0]
           bb = line[-1]
           gg.append(aa)
           gg.append(bb.strip())



       gg1 = set(gg)

       gg2 = []

       for ii in gg1:
           gg2.append(ii)

      

    
       gg2new = []
       for ij in range(len(gg2)):
        
           tpp1 = [item[0] for item in tpp_new]
       
           if gg2[ij] not in tpp1:
              gg2new.append(gg2[ij])


   

       sys_gaps_old = []
       for i in set(gg2new):
           sys_gaps_old.append(i)


    

       system_gaps(sys_gaps_old, argument, tau)

       f.close()
    

def threshold_filter(argument): 
    

    if (argument != 13 and argument != 14 and argument != 15):

       import shutil  

       
       source = '/home/archana/eclipse-workspace/graph_match/FA_err1.txt'
       destination = '/location-to-store-output-files/FA_err1.txt'

       dest = shutil.copyfile(source, destination) 



       tuple_pairs1 = []
       tuple_pairs2 = []
       tuple_sim = []
       tuple_init = []


       f = open('/location-to-store-output-files/FA_err1.txt', 'r')   #### imp orig
       
       #f = open('/home/archana/ve/FA_feat_ASAG/code_write/try_del_iter/FA_err1.txt', 'r')
    
       f1 = f.readlines()
       for line in f1:
    
           line = line.split(": ")
           l1 = line[1].split(", ")
           l2 = l1[0].split("=")
           l3 = l2[1]                          # similarity value
           tuple_sim.append(l3)

           l4 = l1[1].split("=")
           l5 = l4[1]
           tuple_init.append(l5)               # initial similarity value init indicating simi measure based on word2vec 

    
           pairs = remove_punc(line[0])
           pp1 = pairs.split(',')
    
           tuple_pairs1.append(pp1[0])
           tuple_pairs2.append(pp1[1])
    
    
       f.close()


       

       tau_values = [0.5]

       for tau in tau_values:

           print tau

           tp = zip(tuple_pairs1, tuple_pairs2, tuple_sim, tuple_init)

           tpp = []
           for tt in tp:       
          
               sigma_f = max(float(tt[2]), float(tt[3]))

               if float(sigma_f) >= float(tau):
                  tpp.append(tt)      
          

           print tpp

           f = open('/location-to-store-output-files/woutm_2new.txt', 'r')    #### orig imp       
      
           f1 = f.readlines()

           gg = []

           for line in f1:
               line = line.split("\t")
               aa = line[0]
               bb = line[-1]
               gg.append(aa)
               gg.append(bb.strip())



           gg1 = set(gg)

           gg2 = []

           for ii in gg1:
               gg2.append(ii)

    

    
           gg2new = []
           for ij in range(len(gg2)):
        
               tpp1 = [item[0] for item in tpp]
        
               if gg2[ij] not in tpp1:
                  gg2new.append(gg2[ij])


   

           sys_gaps_old = []
           for i in set(gg2new):
               sys_gaps_old.append(i)


    

           system_gaps(sys_gaps_old, argument, tau)
           f.close()





    else:
       f = open('/location-to-store-output-files/tp.txt', 'r')
       f1 = f.readlines()

       tp = []
       for line in f1:
           line = line.split(", (")
           
           tp11 = []
           for ll in line:
               
     
               k1 = remove_punc1(ll)
               if '[' or ']' in k1:
                   k11 = remove_punc(k1)
               else:
                   k11 = k1
               k2 = k11.split(", ")
               tp1 = []
               for kk in k2:
                   kk1 = remove_punc2(kk)
                   tp1.append(kk1)
               tp11.append(tp1)

           tp.append(tp11)
       
       f.close()   


       tpp = []
       for tt in tp[0]:           
       
           if float(tt[2]) >= float(0.5) or float(tt[3]) >= float(0.5):
              tpp.append(tt)


       print tpp


       f = open('/location-to-store-output-files/outm_24.txt', 'r')     #### imp orig       
       
       f1 = f.readlines()

       gg = []

       for line in f1:
           line = line.split("\t")
           aa = line[0]
           bb = line[-1]
           gg.append(aa)
           gg.append(bb.strip())



       gg1 = set(gg)

       gg2 = []

       for ii in gg1:
           gg2.append(ii)

    

    
       gg2new = []
       for ij in range(len(gg2)):
        
           tpp1 = [item[0] for item in tpp]
        
           if gg2[ij] not in tpp1:
              gg2new.append(gg2[ij])


   

       sys_gaps_old = []
       for i in set(gg2new):
           sys_gaps_old.append(i)


    

       system_gaps(sys_gaps_old, argument)
       f.close()

        
           
          
    

 











