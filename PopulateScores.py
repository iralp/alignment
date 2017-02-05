# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 19:54:22 2016

@author: iralp
"""
import pandas as pd
#Map the scores and manual annotations to the sentence pairs
#stats = open('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/stats.csv','w+',encoding = 'utf8')

statsFrame = pd.DataFrame(columns = ['Article','Good_min','Good_max','Good_Partial_min','Good_Partial_max','Partial_min','Partial_max','Bad_min','Bad_max'])
countFrame = pd.DataFrame(columns = ['Article','Good_count','Good_Partial_count','Partial_count','Bad_count'])
#get the file and lengths of simple and standard docs 


#file to save the statistics 
#lines = ['A.C.F._Fiorentina']
#'A_major','A.C.F._Fiorentina','Absolute_zero','Accession_of_Romania_to_the_European_Union','Adolf_von_Henselt']


#load the txt file 
with open(r'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_Format/all_articles',encoding='utf8') as fd:
    lines = fd.readlines()

    
def writeToFile(fd,sents):
    for indx in range(len(sents)):
        fd.write(sents[indx])
        fd.write('\n')
    fd.close()        

def appendToStats(stats,countStats,lis):
    if len(lis) == 0 :
        stats.append(0)
        stats.append(0)
        countStats.append(0)
    else:
        stats.append(min(lis))
        stats.append(max(lis))
        countStats.append(len(lis))
        
article_count = -1    
for each_article in lines:
    print(each_article)
    article_count += 1
    count = 0
    each_article = each_article.strip()
    good = []
    good_partial = []
    partial = []
    bad = []

    #open the actual file for the scores
    with open(r'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/'+each_article+'_collection',encoding='utf8') as fd:
        scoreLines = fd.readlines()
        scoreLines = list(filter(lambda a: a != '\n', scoreLines))
    with open(r'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/output/'+each_article,encoding = 'utf8') as fd:
        scores = fd.readlines()
    print(each_article,' sentences : ',len(scoreLines),' scores : ',len(scores))
    #write one row at a time
    for indx in range(len(scores)):
        #get the individual scores
        each_score = str(scores[indx])
        cols = each_score.split()
        if len(cols) <= 1:
            continue
        for ide in range(len(cols)):
            score = cols[ide]
            #sent = scoreLines[count*len(cols)+ide]
            #print('count : ',count)
            sent = scoreLines[count]
            splits = sent.split("\t")
            if len(splits) != 4:
                print(len(splits),'index : ',count)
            if int(splits[3]) == 3:
                good.append(score)
            if int(splits[3]) == 2:
                good_partial.append(score)
            if int(splits[3]) == 1:
                partial.append(score)
            if int(splits[3]) == 0:
                bad.append(score)
                
            sent = sent.strip(' \t\n\r')
            sent = sent + "\t" + score
            #scoreLines[count*len(cols)+ide] = sent
            scoreLines[count] = sent
            count = count + 1
        
    #flush everything into a text file
    wr = open('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/Revisited/'+each_article+'_collection_scores','w',encoding = 'utf8')
    writeToFile(wr,scoreLines)
    
    stats = []
    countStats = []
    #stats.write(each_article+'\n')
    countStats.append(each_article)
    stats.append(each_article)
    appendToStats(stats,countStats,good)
    appendToStats(stats,countStats,good_partial)
    appendToStats(stats,countStats,partial)
    appendToStats(stats,countStats,bad)
    statsFrame.loc[article_count] = stats
    countFrame.loc[article_count] = countStats    

#write to the csv file
#print(statsFrame)
#statsFrame.to_csv('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/stats.csv',encoding = 'utf8')
#countFrame.to_csv('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/Countstats.csv',encoding = 'utf8')
print('written to file')