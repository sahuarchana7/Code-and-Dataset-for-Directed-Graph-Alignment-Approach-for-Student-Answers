# Readme for gap finding problem


1. Run the code predicate_clusters.py to obtain the predicates from the triples extracted for all pairs of student-answer, model-answer in the dataset (UNT / SciEntsBank / Beetle) and the corresponding vectors for the predicates. We have used a file containing words from wikipredia and vectors corresponding to the words obtained using a pre-trained model trained on Wikipedia articles. This file was available on the internet. The files containing the predicates and corresponding vectors are cluster_words.txt, model_vector.txt, respectively. Since the entire dataset containing the answer-pairs was ran for this code in chunks, i.e. a certain number of answer-pairs at a time, to check for intermediate errors, the final file for the predicates and corresponding vectors is obtained by combining all such cluster_words.txt, model_vector.txt files into single files namely, final_cluster_words.txt and final_pred_vectors.txt, respectively.  

2. The predicates in final_cluster_words.txt and the corresponding vectors in final_pred_vectors.txt are further clustered into a number of groups using K-means clustering algorithm in get_clusters.py. The number of groups is determined using an Elbow method in det_number_clusters.py and an output file all_clusters49.txt is created (for example, this file has 49 clusters/groups, each cluster containing similar words/ words having same meaning or different syntactic variations of the same word.   




3. Please run the code overall_combine.py to obtain the gaps in student answer. Student answers and model answers belonging to SciEntsBank dataset have been taken for illustration purpose. 

All the intermediate codes mentioned in overall_combine.py are present in this folder Original-Gap-finding-Code. 

the string 'location-to-store-output-files' indicates the location where you want to keep the current folder containing the code, other folders and output files. 




