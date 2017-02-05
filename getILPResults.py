# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:25:52 2016

@author: iralp
"""
import pandas as pd
from copy import deepcopy

articles = None
article_path = 'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/all_articles'
with open(article_path,encoding='utf8') as fd:
        articles = fd.readlines()

simple_sens = []
        
 
for each_ in articles:
        
    #get results from ilp.sol file
    each_ = str(each_).split('\n')
    each_article = each_[0]
    with open('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/ILP_1_8/_'+ each_article +'_ilp.sol') as fd:
        lines = fd.readlines()
    
    with open('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/'+ each_article +'_collection',encoding = 'utf8') as fd:
        sents = fd.readlines()
        sents = list(filter(lambda a: a != '\n', sents))
       
    with open('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/'+ each_article +'_simple_article',encoding = 'utf8') as fd:
        simple_sens = fd.readlines()
        simple_sens = list(filter(lambda a: a != '\n', simple_sens))
    
    align_frame = pd.DataFrame(columns = ['article','tuple','actual_annotation','index_in_file'])
        
    print(len(lines))
    print(len(sents))
    
    sens = []
    
    for indx in range(len(sents)):
        sens.append(sents[indx])
    
    print(len(sens))
    
    
    count = 0
    alignments = {}
    for indx in range(2,len(lines)):
        line = lines[indx]
        if indx % 2 == 0:
            continue
        #print('line : ',line)
        tupl = line[line.index('('):]
        align = line[line.index('_1') + 2:]
        align_score = int(align.strip())
        if align_score == 1:
            list_of_resulst = []
            alignments[align] = 1
            std = int(tupl[tupl.index('(')+1:tupl.index(',')])
            simp = int(tupl[tupl.index(',')+1:tupl.index(')')])
            count = std * len(simple_sens)+ simp
            print('count : ',count)
            try:
                sentence = sens[count]
            except IndexError:
                print('nothing')
                
            print('sentence :',sentence)
            list_of_resulst.append(each_article)
            list_of_resulst.append(str(tupl[:tupl.index('_')]))
            elements = sentence.split('\t')
            list_of_resulst.append(str(elements[3].strip()))
            list_of_resulst.append(str(count))
            print(list_of_resulst)
            align_frame.loc[count] = list_of_resulst
    
    actual_results = pd.DataFrame(columns = ['article','std_index','simple_index','sentence_no','annotation'])
    count = 0
    len_of_simple = len(simple_sens)
    for indx in range(len(sens)):
        sentence = sens[indx]
        elements = sentence.split('\t')
        score = int(elements[3].strip())
        lst = []
        if score == 3:
            #note the indices required
            simple = indx % len_of_simple
            std = int(indx / len_of_simple)
            lst.append(each_article)
            lst.append(str(std))
            lst.append(str(simple))
            lst.append(str(indx))
            lst.append(str(score))
            actual_results.loc[count] = lst
            count += 1
    
            
    actual_results.to_csv('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/ILP_1_8/' + each_article + '_actual_results.csv',encoding = 'utf8')
    #print(align_frame)
    
    align_frame.to_csv('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/ILP_1_8/' + each_article + '_ilp_results.csv',encoding = 'utf8')