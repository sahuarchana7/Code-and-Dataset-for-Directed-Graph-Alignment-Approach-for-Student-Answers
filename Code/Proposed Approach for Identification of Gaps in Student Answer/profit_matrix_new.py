import sys

def remove_punc(string):
    
    punctuations = '''['''

    no_punct = ""
    for char in string:
        if char not in punctuations:
           no_punct = no_punct + char


    return(no_punct)



def remove_punc1(string):   
    

    punctuations = ['(', ')', '[', ']']

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

    #print(no_punct)
    return(no_punct)



aa1 = sys.argv[1]


tuple_pairs1 = []
tuple_pairs2 = []
tuple_sim = []
tuple_init = []

if int(aa1) != 13 and int(aa1) != 14 and int(aa1) != 15:


    tuple_pairs1 = []
    tuple_pairs2 = []
    tuple_sim = []
    tuple_init = []

    f = open('/location-to-store-output-files/FA_err1.txt', 'r')
   
    f1 = f.readlines()
#f1 = f.readlines()
    for line in f1:
    #print line
        line = line.split(": ")
        l1 = line[1].split(", ")
        l2 = l1[0].split("=")
        l3 = l2[1]                          # similarity value
        tuple_sim.append(l3)

        l4 = l1[1].split("=")
        l5 = l4[1]
        tuple_init.append(l5)               # initial similarity value init indicating simi measure based on word2vec 

    #for x in line[0]:
    #    if x ==                              # remove [ character
        pairs = remove_punc(line[0])
        pp1 = pairs.split(',')
    
        tuple_pairs1.append(pp1[0])
        tuple_pairs2.append(pp1[1])
    
    f.close()








    tuple_pairs1_u = []

    tuple_pairs2_u = []

    for i in set(tuple_pairs1):                # this always contains model answer nodes
        tuple_pairs1_u.append(i)

    for i in set(tuple_pairs2):                 # this always contains student answer nodes
        tuple_pairs2_u.append(i)







    if len(set(tuple_pairs1))  > len(set(tuple_pairs2)):
       print "Hello"

       tt =  len(set(tuple_pairs2))
       ttbig = len(set(tuple_pairs1))
   

       Matrix = [[0 for x in range(ttbig)] for y in range(tt)] 

       tp = zip(tuple_pairs2, tuple_pairs1, tuple_sim, tuple_init)

   
       for ii in tp:

       #print ii
           jj1 = ii[0]
           jj2 = ii[1]

       #print jj1

           ind1 = tuple_pairs2_u.index(jj1)
           ind2 = tuple_pairs1_u.index(jj2)

           Matrix[ind1][ind2] = ii[2]


   #print Matrix
   
       jnew = []
       for im in Matrix:
           inew = []
           for imm in im:
               inew.append(float(imm))
           jnew.append(inew)

   #print jnew

       #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/profit_matrix.txt', 'a')
       f = open('./best_filter/profit_matrix.txt', 'w')
       #print jnew
       f.write(str(jnew))
       f.close()

       #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/tuple_pairs2_u.txt', 'a')
       f = open('./best_filter/tuple_pairs2_u.txt', 'w')
       #print tuple_pairs2_u 
       f.write(str(tuple_pairs2_u))
       f.close()

       #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/tuple_pairs1_u.txt', 'a')
       f = open('./best_filter/tuple_pairs1_u.txt', 'w')
       #print tuple_pairs1_u
       f.write(str(tuple_pairs1_u))
       f.close()

   
       
#[float(i) for i in lst]


    else:                                                          # no. of model answer nodes is less than no. of student answer nodes

       print "Hi"
       tt =  len(set(tuple_pairs1))                     # model answer nodes set length
       ttbig = len(set(tuple_pairs2))                   # student answer nodes set length
       x = [[] for i in range(tt)]

       Matrix = [[0 for x in range(ttbig)] for y in range(tt)] 

       #print x

       tp = zip(tuple_pairs1, tuple_pairs2, tuple_sim, tuple_init)
   
       for ii in tp:
           jj1 = ii[0]
           jj2 = ii[1]

           ind1 = tuple_pairs1_u.index(jj1)
           ind2 = tuple_pairs2_u.index(jj2)

           Matrix[ind1][ind2] = ii[2]


   #print Matrix
       
       jnew = []
       for im in Matrix:
           inew = []
           for imm in im:
               inew.append(float(imm))
           jnew.append(inew)

   #print jnew

       #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/profit_matrix.txt', 'a')
       f = open('./best_filter/profit_matrix.txt', 'w')
       #print jnew
       f.write(str(jnew))
       f.close()


       #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/tuple_pairs2_u.txt', 'a')
       f = open('./best_filter/tuple_pairs2_u.txt', 'w')
       #print tuple_pairs2_u 
       f.write(str(tuple_pairs2_u))
       f.close()

       #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/tuple_pairs1_u.txt', 'a')
       f = open('./best_filter/tuple_pairs1_u.txt', 'w')
       #print tuple_pairs1_u
       f.write(str(tuple_pairs1_u))
       f.close()


else:

     

     f = open('./tp.txt', 'r')
     f1 = f.readlines()

     tp = []

     lines = f1[0].split(", (")


     for j in lines:

    
         line1 = j.replace('[', "")
    
         line2 = line1.replace('(', "")
         line3 = line2.replace(')', "")
         line4 = line3.replace("]", "")
         line5 = line4.replace("'", "")  
   
         k2 = line5.split(", ")
    
         tp.append(k2)



     f.close()

     tuple_pairs1 = []
     tuple_pairs2 = []
     tuple_sim = []
     tuple_init = []

     for jj in tp:
         jj1 = jj[0]
         jj2 = jj[1]
         jj3 = jj[2]
         jj4 = jj[3]
         tuple_pairs1.append(jj1)
         tuple_pairs2.append(jj2)
         tuple_sim.append(jj3)
         tuple_init.append(jj4)

     #print tuple_pairs1
     #print tuple_pairs2
     #print tuple_sim
     #print tuple_init

         

         


     """tuple_pairs1_u = []

     tuple_pairs2_u = []

     for i in set(tuple_pairs1):                # this always contains model answer nodes
         tuple_pairs1_u.append(i)

     for i in set(tuple_pairs2):                 # this always contains student answer nodes
         tuple_pairs2_u.append(i)"""



     tuple_pairs1_u = []
     for i in tuple_pairs1:
         if i not in tuple_pairs1_u:
            tuple_pairs1_u.append(i)

     tuple_pairs2_u = []
     for i in tuple_pairs2:
         if i not in tuple_pairs2_u:
            tuple_pairs2_u.append(i)


     #print tuple_pairs1_u                                  # unique model answer nodes
     #print tuple_pairs2_u                                  # unique student answer nodes





     
     if len(set(tuple_pairs1))  > len(set(tuple_pairs2)):
        print "Hello"

        tt =  len(set(tuple_pairs2))                        # student answer nodes as rows
        ttbig = len(set(tuple_pairs1))                      # model answer nodes as columns
   

        Matrix = [[0 for x in range(ttbig)] for y in range(tt)] 

        tp = zip(tuple_pairs2, tuple_pairs1, tuple_sim, tuple_init)

   
        for ii in tp:

       #print ii
            jj1 = ii[0]
            jj2 = ii[1]

       #print jj1

            ind1 = tuple_pairs2_u.index(jj1)
            ind2 = tuple_pairs1_u.index(jj2)

            Matrix[ind1][ind2] = ii[2]


        #print Matrix
   
        jnew = []
        for im in Matrix:
            inew = []
            for imm in im:
                inew.append(float(imm))
            jnew.append(inew)

        #print jnew

        #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/profit_matrix.txt', 'a')
        f = open('./best_filter/profit_matrix.txt', 'w')
        #print jnew
        f.write(str(jnew))
        f.close()

        #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/tuple_pairs2_u.txt', 'a')
        f = open('./best_filter/tuple_pairs2_u.txt', 'w')
        #print tuple_pairs2_u
        f.write(str(tuple_pairs2_u))
        f.close()

        #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/tuple_pairs1_u.txt', 'a')
        f = open('./best_filter/tuple_pairs1_u.txt', 'w')
        #print tuple_pairs1_u
        f.write(str(tuple_pairs1_u))
        f.close()

   
       
#[float(i) for i in lst]


     else:                                                          # no. of model answer nodes is less than no. of student answer nodes

       print "Hi"
       tt =  len(set(tuple_pairs1))                     # model answer nodes set length
       ttbig = len(set(tuple_pairs2))                   # student answer nodes set length
       x = [[] for i in range(tt)]

       Matrix = [[0 for x in range(ttbig)] for y in range(tt)]      # model answer nodes as rows and student answer nodes as columns

       #print x

       #print tuple_pairs1
       #print tuple_pairs2
       

       tp = zip(tuple_pairs1, tuple_pairs2, tuple_sim, tuple_init)

       #print tp
   
       for ii in tp:
           jj1 = ii[0]
           jj2 = ii[1]

           #print jj1
           #print jj2

           ind1 = tuple_pairs1_u.index(jj1)
           ind2 = tuple_pairs2_u.index(jj2)

           #print ind1
           #print ind2

           #print ii[2]

           Matrix[ind1][ind2] = ii[2]


       #print Matrix
       
       jnew = []
       for im in Matrix:
           inew = []
           for imm in im:
               inew.append(float(imm))
           jnew.append(inew)

       #print jnew

       #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/profit_matrix.txt', 'a')
       f = open('./best_filter/profit_matrix.txt', 'w')
       #print jnew
       f.write(str(jnew))
       f.close()


       #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/tuple_pairs2_u.txt', 'a')
       f = open('./best_filter/tuple_pairs2_u.txt', 'w')
       #print tuple_pairs2_u
       f.write(str(tuple_pairs2_u))
       f.close()

       #f = open('/home/archana/ve/FA_feat_ASAG/best_filter/tuple_pairs1_u.txt', 'a')
       f = open('./best_filter/tuple_pairs1_u.txt', 'w')
       #print tuple_pairs1_u
       f.write(str(tuple_pairs1_u))
       f.close() 



   







