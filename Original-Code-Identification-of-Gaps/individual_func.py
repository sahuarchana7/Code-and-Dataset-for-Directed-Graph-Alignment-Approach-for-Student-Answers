## Individual_functions.py

import os
import nltk
from nltk.cluster import euclidean_distance
from nltk import cluster
from nltk import tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stopset = list(stopwords.words('english')) + ['across'] + ['underneath'] + ['within'] + ['halfway'] + ['slipperiness'] + ['neither'] + ['besides'] + ['sleet'] + ['nowhere'] + ['beyond'] + ['could'] + ['without'] + ['Dear'] + ['dear'] + ['someplace'] + ['must'] + ['can'] + ['would']






def cluster_algo_output():  



    import ast

    f = open('/location-to-store-output-files/clusters/scientsbank/all_clusters49.txt', 'r')
    f1 = f.read().splitlines()


    res = ast.literal_eval(f1[0]) 


    g = open('/location-to-store-output-files/woutm_2new.txt', 'a')    
    
    f = open('/location-to-store-output-files/outm_24.txt', 'r')
    
    f1 = f.readlines()
    for line in f1:
    
        line1 = line.split("\t")

        line2 = nltk.word_tokenize(line1[1])
        

        if len(line2) > 1:
       

           arr = []
           for jj in line2:
               if jj not in stopset:
                  arr.append(jj)

    
   
           if len(arr) > 1:                          

              y = []
              for x in arr:

                  try:
                     ii = [item[0] for item in res if x in item[1]]
                     y.append(ii[0])
                  except IndexError:
                     print "indexerror"               

                              
              line1[1] = y[0]                



    
              jj = "\t".join(line1[:])             
    
              g.write(jj) 

        

           elif arr != []:
     
                arr1 = arr[0]        

                ii = [item[0] for item in res if arr1 in item[1]]

                if ii != []:
                   line1[1] = ii[0]
                   jj = "\t".join(line1[:])
   
                   g.write(jj)
                else:
                   jj = "\t".join(line1[:])
                   g.write(jj)

           else:

             jj = "\t".join(line1[:])
             g.write(jj)                

    

        else:       
       
            arr1 = line2[0]

            ii = [item[0] for item in res if arr1 in item[1]]

            if ii != []:
               line1[1] = ii[0]
               jj = "\t".join(line1[:])
    
               g.write(jj)
       
            else:
               jj = "\t".join(line1[:])
    
               g.write(jj)   



    g.close()
    f.close()

    g = open('/location-to-store-output-files/wouts_2new.txt', 'a')    
    
    f = open('/location-to-store-output-files/outs_24.txt', 'r')
    
    f1 = f.readlines()
    for line in f1:
    
        line1 = line.split("\t")

        line2 = nltk.word_tokenize(line1[1])
    

        if len(line2) > 1:
       

           arr = []
           for jj in line2:
               if jj not in stopset:
                  arr.append(jj)
                
          
   
           if len(arr) > 1:

              arr1 = " ".join(arr[:]) 



              y = []
              for x in arr:
                  try:
                     ii = [item[0] for item in res if x in item[1]]
                     y.append(ii[0])
                  except IndexError:
                     print "indexerror"
                     

              

              line1[1] = y[0]              



    
              jj = "\t".join(line1[:])

                 
    
              g.write(jj) 
       

           elif arr != []:
     
               
                arr1 = arr[0] 


                ii = [item[0] for item in res if arr1 in item[1]]

                if ii != []:
                   line1[1] = ii[0]
                   jj = "\t".join(line1[:])
   
                   g.write(jj)
                else:
                   jj = "\t".join(line1[:])
                   g.write(jj)


           
           else:
                jj = "\t".join(line1[:])
                g.write(jj)


   
        else:

       
       
           arr1 = line2[0]

           ii = [item[0] for item in res if arr1 in item[1]]

           if ii != []:
       
              line1[1] = ii[0]
              jj = "\t".join(line1[:])
    
              g.write(jj)

           else:

              jj = "\t".join(line1[:])
              g.write(jj)   



    g.close()
    f.close()










    



# K-means clustering algorithm:

def Kmeans_1(data, no_of_clusters):

    clusterer = nltk.cluster.kmeans.KMeansClusterer(no_of_clusters, euclidean_distance, avoid_empty_clusters = True)  ## ran code
    pp = clusterer.cluster(data, True)
    return pp






def fix_point1():
    os.system("java -jar /home/archana/eclipse-workspace/graph_match/fft22.jar /location-to-store-output-files/woutm_2new.txt /location-to-store-output-files/wouts_2new.txt")










    



