# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 13:51:13 2016

@author: iralp
"""

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
count_frame = pd.read_csv('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/Countstats.csv',encoding = "utf8")
#ILP_results frame 
ilp_frame = pd.DataFrame(columns = ['article','actual_good_count','ilp_identified_count','total_count','precision','recall','fscore'])

#group by article to obtain the count
#print(into_frame.groupby(['article']).size())
#read the articles evaluated one by one
articles = None
article_path = 'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/all_articles'
with open(article_path,encoding='utf8') as fd:
        articles = fd.readlines()

precisions = []
recalls = []
fscores = {}
count = 0
for each_ in articles:
    each_ = str(each_).split('\n')
    each_article = each_[0]
    
    lst_of_result = []
    each_article_frame = pd.read_csv('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/ILP_1_8/'+ each_article +'_ilp_results.csv')
   
    annotations = each_article_frame['actual_annotation']
    count_of_good = len(list(filter(lambda a : a == 3 ,annotations)))
    actual_count = int(count_frame[count_frame['Article'] == each_article]['Good_count']) 
    lst_of_result.append(each_article)
    lst_of_result.append(actual_count)
    lst_of_result.append(count_of_good)
    lst_of_result.append(len(annotations))
        
    if actual_count == 0 :
        lst_of_result.append('0')
        lst_of_result.append('0')
        lst_of_result.append('0')
        ilp_frame.loc[count] = lst_of_result
        count += 1
        continue
    precision = count_of_good / len(annotations)
    recall = count_of_good / actual_count
    precisions.append(precision)
    recalls.append(recall)
    if precision == 0 :        
        lst_of_result.append('0')
        lst_of_result.append('0')
        lst_of_result.append('0')
        ilp_frame.loc[count] = lst_of_result
        count += 1
        continue
    if count_of_good != actual_count:
        print('article : ',each_article)
        print('count_of_good : ',count_of_good)
        print('actual count: ',actual_count)
    
    fscore = 2* ((precision*recall)/(precision + recall))
    fscores[each_article] = fscore
    lst_of_result.append(precision)
    lst_of_result.append(recall)
    lst_of_result.append(fscore)
    ilp_frame.loc[count] = lst_of_result

    count += 1
    
#print('fscores : ',fscores)
#sorted_scores = sorted(fscores.items(), key=operator.itemgetter(1),reverse = True)
       
print('count : ',count)
ilp_frame.to_csv('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/ILP_1_8/ILP_results.csv',encoding = 'utf8')

#print('sorted_scores : ',sorted_scores)