from sklearn.cluster import KMeans 
from sklearn import metrics 
from scipy.spatial.distance import cdist 
import numpy as np 
import matplotlib.pyplot as plt  





import numpy as np

data = np.loadtxt('/location-to-store-output-files/final_pred_vectors.txt')

print data



X = np.array(list(zip(*data))).reshape(len(data[0]), 1757)
print X

distortions = [] 
inertias = [] 
mapping1 = {} 
mapping2 = {} 
#K = range(1,9) 
#K = range(30, 70, 2)
#K = range(30, 51, 2)
#K = range(40, 61, 2)

#K = range(30, 41) ## K = 32
K = range(38, 50)
#K = range(40, 55)
  
for k in K: 
    #Building and fitting the model 
    kmeanModel = KMeans(n_clusters=k).fit(X) 
    kmeanModel.fit(X)     
      
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 
                      'euclidean'),axis=1)) / X.shape[0]) 
    inertias.append(kmeanModel.inertia_) 
  
    mapping1[k] = sum(np.min(cdist(X, kmeanModel.cluster_centers_, 
                 'euclidean'),axis=1)) / X.shape[0] 
    mapping2[k] = kmeanModel.inertia_ 











plt.plot(K, inertias, 'bx-') 
plt.xlabel('Values of K') 
plt.ylabel('Inertia') 
plt.title('The Elbow Method using Inertia') 
plt.show() 












