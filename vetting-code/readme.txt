# Steps to obtain the vetting-results.

1. Obtain the gaps annotated by the first annotator. The second annotator cross-verifies the gap annotations by marking against the gaps annotated by first annotator as 1, if agreeing with the first annotator annotated gap else 0 if disagreeing with the second annotator. An excel file annotator-ratings.xlsx is created with all the above data.

2. Convert the above annotator-ratings.xlsx file to .csv file by running the code convert-to-csv.py. 

3. Calculate the count / number of student answers for which the gaps annotated by first annotator are in agreement with the second annotator and hence compute the percentage of the same so as to obtain the vetting results. 
