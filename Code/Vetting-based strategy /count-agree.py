import pandas
#student_answer_id,question_paper,question_type,question_text,student_answer,model_answer,gap,Rating of gap (0 or 1)
#colnames = ['student_answer_id', 'question_paper', 'question_type', 'question_text', 'student_answer', 'model_answer', 'gap', 'rating']
#data = pandas.read_csv('Beetle1.csv', names=colnames)

colnames = ['rating']


data = pandas.read_csv('annotator-ratings-csv.csv', names=colnames)

names = data.rating.tolist()

print names

print len(names)

print names.count('1')   # 297 (Beetle) 71 % agree, # 350 (ScientsBank) 83.7 % agree, #126 (UNT)  78.3 %

