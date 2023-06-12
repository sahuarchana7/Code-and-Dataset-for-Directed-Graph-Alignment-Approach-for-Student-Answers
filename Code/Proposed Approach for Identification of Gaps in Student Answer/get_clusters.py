from sklearn.cluster import KMeans 
from sklearn import metrics 
from scipy.spatial.distance import cdist 
import numpy as np 
import matplotlib.pyplot as plt  
import nltk

from nltk.cluster import KMeansClusterer, euclidean_distance


ffg = open('/location-to-store-output-files/all_clusters49.txt', 'a')

def optimal_number_of_clusters(wcss):
    
    from math import sqrt
    x1, y1 = 2, wcss[0]
    x2, y2 = 20, wcss[len(wcss)-1]

    distances = []
    for i in range(len(wcss)):
        x0 = i+2
        y0 = wcss[i]

        numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
        denominator = sqrt((y2 - y1)**2 + (x2 - x1)**2)
        distances.append(numerator/denominator)
    return distances.index(max(distances)) + 2


def calculate_wcss(data):
    
    from sklearn.cluster import KMeans
    wcss = []
    #for n in range(2, 21):
    #for n in range(2, 40):
    #for n in range(2, 31):
    #for n in range(10, 41):
    for n in range(40, 71):
        kmeans = KMeans(n_clusters=n)
        kmeans.fit(X=data)
        wcss.append(kmeans.inertia_)

    return wcss




def Kmeans_1(data, no_of_clusters):

    clusterer = nltk.cluster.kmeans.KMeansClusterer(no_of_clusters, euclidean_distance, avoid_empty_clusters = True)  ## ran code
    
    pp = clusterer.cluster(data, True)
    return pp



def cluster_algo_output(pp):
    
    ppnew = []
    for jj in pp:
        jj1 = "c"+"_"+str(jj)
        ppnew.append(jj1)

    

    ppnew_u = set(ppnew)

    af = []
    f = open('/location-to-store-output-files/final_cluster_words.txt', 'r')
    
    f1 = f.readlines()
    for line in f1:
        af.append(line.rstrip())

    

    zzz = zip(ppnew, af)



    zzz_new1 = []
    zzz_new = []
    for ii in ppnew_u:
        ii1 = [item[1] for item in zzz if ii in item]
    
    
        zzz_new.append(ii1)
        zzz_new1.append(ii)



    final_zzz = zip(zzz_new1, zzz_new)

    print final_zzz

    ffg.write(str(final_zzz))
    ffg.write('\n')



data1 = np.loadtxt('/location-to-store-output-files/final_pred_vectors.txt')


XX = np.array(list(zip(*data1))).reshape(len(data1[0]), 1757)      ##3## check    # this is the number of vectors in the final_pred_vectors.txt



pp = Kmeans_1(data1, 49)


print pp

cluster_algo_output(pp)

ffg.close()
















