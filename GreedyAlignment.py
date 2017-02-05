# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 19:10:35 2016

@author: iralp
"""
import operator
import pandas as pd
# -*- coding: utf-8 -*-
#Greedy alignment of the sentences : Alignmenet of simple wikipedia and standard wikipedia  Section : 4.2


total_ = 0
correct_labels_good = 0
correct_labels_good_partial = 0

results_frame = pd.DataFrame(columns = ['article','tuple','score','sentence_no','annotation'])
frame_length = 0

# get the article names
with open(r'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Formatted_data/all_articles',encoding = "utf8") as fd:
    lines = fd.read()
    

docs = lines.split("\n")
docs = list(filter(lambda a: a != "\n", docs))
count_of_docs = 0 

def printDict(dict_):
    for key in sorted(dict_):
        print(key,dict_[key])

def removeFromDict(keys_to_remove,dict_):
    for each_key in keys_to_remove:
        dict_.pop(each_key)

def greedyAlignment(dict_Scores):
    best_scores = []
    global total_
    global correct_labels_good
    global correct_labels_good_partial
    
    #do until the dictionary gets empty
    while len(dict_Scores) != 0 :
        #Now sort the dictionary by score to get the best score
        sorted_scores = sorted(dict_Scores.items(), key=operator.itemgetter(1),reverse = True)
        
        #get the tuple with the best score
        best_score_tuple = sorted_scores[0]
        print('best_score_tuple : ',best_score_tuple[0],best_score_tuple[1])  
        
        #Note the tuple,score,the sentence no and the manual annotation
        candidate = [best_score_tuple[0],best_score_tuple[1],dict_annot[best_score_tuple[0]][0],dict_annot[best_score_tuple[0]][1]]
        print('candidate : ',candidate)
        best_scores.append(candidate)
        
        if dict_annot[best_score_tuple[0]][1] == 3:
            correct_labels_good += 1
        
        if dict_annot[best_score_tuple[0]][1] == 2:
            correct_labels_good_partial += 1
        
        #remove the entries with same row and same column from the dictionary
        keys_to_remove = list(filter(lambda a: a[0] == best_score_tuple[0][0] or a[1] == best_score_tuple[0][1], dict_Scores.keys()))
        
        print('tuple : ',best_score_tuple[0][0],best_score_tuple[0][1])
        print('keys_to_remove : ',sorted(keys_to_remove))
        #now remove all these keys from the dictionary
        removeFromDict(keys_to_remove,dict_Scores)
    
    total_ += len(best_scores)
    return best_scores


def writeResults(each_doc,best,dict_annot,scoresLines):
    global frame_length
    fs = open('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/Greedy_align/' + each_doc + '_results','w+',encoding = "utf8")
    for each_result in best:
        #get the sentence 
        sentence = scoresLines[each_result[2]]
        #append the score from baseline
        sentence += "\t" + each_result[1] + "\n"
        #write to the file
        results_frame.loc[frame_length] = [each_doc,'(' + str(each_result[0][0]) + ',' + str(each_result[0][1]) + ')',str(each_result[1]),str(each_result[2]),str(each_result[3])]
        frame_length += 1
        fs.write(sentence)
    fs.close()
    
count = 2
#for each document 
for each_doc in docs:
    print(each_doc)
    dict_Scores = {}
    dict_annot = {}
    if len(each_doc) == 0:
        break
    #read the original file with the annotations
    with open(r'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/' + each_doc + '_collection', encoding = "utf8") as fd:
        scoresLines = fd.readlines()
        scoresLines = list(filter(lambda a: a != '\n', scoresLines))
    
    #read the scores file
    with open(r'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/output/' + each_doc, encoding = "utf8") as fd:
        scores = fd.readlines()
        scores = list(filter(lambda a: a != '\n', scores))
    
    #populate a dictionary
    row_no = 0
    sentence_no = 0
    
    for ind in range(len(scores)):
        each_row = scores[ind]
        #get individual scores
        cols = each_row.split()
        col_no = 0
        for indx in range(len(cols)):
            tup = (row_no,col_no)
            dict_Scores[tup] = cols[col_no]
            col_no += 1
            
            each_entry = scoresLines[sentence_no]
            #get the manual annotation
            each_entry_split = each_entry.split("\t")
            annot = each_entry_split[3]
            #now include this and sentence no in the second dictionary
            dict_annot[tup] = [sentence_no,int(annot)]
            sentence_no += 1
        row_no += 1
    
    print("dict_annot")
    #printDict(dict_annot)
    print("dict_Scores")    
    #printDict(dict_Scores)
    best = greedyAlignment(dict_Scores)
    #write the results into a file
    #writeResults(each_doc,best,dict_annot,scoresLines)
    
    print('best ::: ',best)
    print('total_ : ',total_)
    print('correct_labels_good : ',correct_labels_good)
    print('correct_labels_good_partial : ',correct_labels_good_partial)
    print('count_of_docs : ',count_of_docs)
    count_of_docs += 1

    '''count = count - 1
    if count == 0 :
        break'''
print("frame length : ",len(results_frame))
#results_frame.to_csv('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/Greedy_align/greedy_results_per_file.csv',encoding = "utf8")