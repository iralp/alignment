# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 23:26:53 2016

@author: iralp
"""
#Calculates the precision,recall,fscores for the alignments found

import pandas as pd
import operator
#from copy import deepcopy
#import sklearn.metrics as mtrc

#read the csv into a dataframe
into_frame = pd.read_csv('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/Greedy_align/greedy_results_per_file.csv',encoding = "utf8")
count_frame = pd.read_csv('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/Countstats.csv',encoding = "utf8")

#group by article to obtain the count
#print(into_frame.groupby(['article']).size())

#get the annotations into a list
y_predicted = into_frame['annotation']

'''
y_predicted_good = deepcopy(y_predicted)
y_predicted_good_partial = deepcopy(y_predicted)

#replace all 2s,1s with 0s
y_predicted_good = [0 if a == 2 else a for a in y_predicted_good]
y_predicted_good = [0 if a == 1 else a for a in y_predicted_good]
y_predicted_good = [1 if a == 3 else a for a in y_predicted_good]

print('y_predicted_good:',y_predicted_good)

len_ = len(y_predicted)

#create another list with default '3'-GOOD annotations of same size

y_output = [1]*len_

#now calculate the precision,recall and fscore
print('GOOD : ',mtrc.f1_score(y_predicted_good,y_output,average=None))
#print('GOOD_PARTIAL : ',mtrc.precision_recall_fscore_support(y_predicted_good_partial,y_output,average='micro'))
'''
good_count = len(list(filter(lambda a : a == 3 ,y_predicted)))
print('len(y_predicted) : ',len(y_predicted))
precision = good_count/sum(count_frame['Good_count'])
recall = good_count/sum(count_frame['Good_count'])
fScore = 2* ((precision*recall)/(precision + recall))
print('good_count : ',good_count)
print('precision : ',precision)
print('Total good candidates : ',sum(count_frame['Good_count']))
print('recall : ',recall)
print('fScore : ',fScore)

for_each_article = pd.DataFrame(columns = ['article','precision','recall','fscore','actual_alignments'])
#calculate precision,recall and fscore document wise
articles = list(set(into_frame['article']))
precisions = []
recalls = []
fscores = {}
count = 0
for each_article in articles:
    lst_of_result = []
    annotations = into_frame[into_frame['article'] == each_article]['annotation']
    count_of_good = len(list(filter(lambda a : a == 3 ,annotations)))
    actual_count = int(count_frame[count_frame['Article'] == each_article]['Good_count']) 
    if actual_count == 0 :
        lst_of_result.append(each_article)
        lst_of_result.append('0')
        lst_of_result.append('0')
        lst_of_result.append('0')
        lst_of_result.append('0')
        for_each_article.loc[count] = lst_of_result
        count += 1
        continue
    precision = count_of_good / len(annotations)
    recall = count_of_good / actual_count
    precisions.append(precision)
    if precision == 0 :        
        lst_of_result.append(each_article)
        lst_of_result.append('0')
        lst_of_result.append('0')
        lst_of_result.append('0')
        lst_of_result.append(actual_count)
        for_each_article.loc[count] = lst_of_result
        count += 1
        continue
    if count_of_good != actual_count:
        print('article : ',each_article)
        print('count_of_good : ',count_of_good)
        print('actual count: ',actual_count)
    
    fscore = 2* ((precision*recall)/(precision + recall))
    fscores[each_article] = fscore
    lst_of_result.append(each_article)
    lst_of_result.append(precision)
    lst_of_result.append(recall)
    lst_of_result.append(fscore)
    lst_of_result.append(actual_count)
    for_each_article.loc[count] = lst_of_result

    count += 1
    
#print('fscores : ',fscores)
#sorted_scores = sorted(fscores.items(), key=operator.itemgetter(1),reverse = True)
       
print('count : ',count)
for_each_article.to_csv('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/articles_actuals.csv',encoding = 'utf8')

#print('sorted_scores : ',sorted_scores)