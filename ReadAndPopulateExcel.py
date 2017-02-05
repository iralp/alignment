# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 13:22:24 2016

@author: iralp
"""

#read the annotations file and generate a new excel

import pandas as pd
import csv

def convertDataToExcel(file_pointer,csv_file,writer):
    
    while True:
        each_line = file_pointer.readline()
        if not each_line:
            break
        sens = each_line.split('\t')
        print("no of sens",len(sens))
        if(len(sens) < 4):
            break
        print("send[0] : ",sens[0],"sens[1]",sens[1],"sens[2] : ",sens[2],"sens[3] : ",sens[3])
        writer.writerow([sens[0],sens[1],sens[2],sens[3]])
        
        '''article.append(sens[0])
        simpSent.append(sens[1])
        standSent.append(sens[2])
        typeOfMatch.append(sens[3])'''
'''    frame['article'] = article
    frame['simpSent'] = simpSent
    frame['standSent'] = standSent
    frame['typeOfMatch'] = typeOfMatch
    frame.to_csv(csv_file)'''
        
def readData():
        
    file_pointer = open(r'C:/Personal Docs/Course_Work/NLP/Simple-Standard Wiki ALignment/Data/annotations.txt','r',encoding="utf8")
    file_csv = open(r'C:/Personal Docs/Course_Work/NLP/Simple-Standard Wiki ALignment/Data/dataRetrieved.csv','a',encoding="utf8")    
    writer = csv.writer(file_csv)
    writer.writerow(['article','simpSent','standSent','typeOfMatch'])
        
    convertDataToExcel(file_pointer,file_csv,writer)
                
    file_csv.close()
    file_pointer.close()

#extract features for the classifier
#read the data

    
    