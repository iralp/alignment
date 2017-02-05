# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 11:22:54 2016

@author: iralp
"""

#Use coreference to reduce the number of negative examples

'''from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP("http://localhost:9000")

sentences = "Alchemy is an influential philosophical tradition whose early practitioners ' claims to profound powers were known from antiquity.\
    The defining objectives of alchemy are varied ; these include the creation of the fabled philosopher 's stone possessing powers including the\
    capability of turning base metals into the noble metals gold or silver,\
    as well as an elixir of life conferring youth and immortality.\
    Western alchemy is recognized as a protoscience that contributed to the development of modern chemistry and medicine .\
    Alchemists developed a framework of theory , terminology , experimental process and basic laboratory techniques that are still recognizable today .\
    But alchemy differs from modern science in the inclusion of Hermetic principles and practices related to mythology , religion , and spirituality ."

    
sentences = "The defining goals of alchemy are often given as the transmutation of common metals into gold ( known as chrysopoeia ) , \
            the creation of a panacea , and the discovery of a universal solvent . \
            However , this only highlights certain aspects of alchemy ."
output =   nlp.annotate(sentences,properties={ 'annotators': 'dcoref',
  'outputFormat': 'json','timeout': 30000})


corefs = output['corefs']
print(corefs)
    
'''
import pandas as pd

#read the csv
dataFrame = pd.read_csv(r'C:/Personal Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Test.csv')
dataFrame = dataFrame.dropna()

neg = 0
pos = 0

dataFrame = dataFrame.reset_index()
for indx in range(1,len(dataFrame)):
    if dataFrame.get_value(indx,'typeOfMatch') == 0  or dataFrame.get_value(indx,'typeOfMatch') == '0\r\n' :
        dataFrame.set_value(indx,'typeOfMatch',0)
        neg = neg + 1
    if dataFrame.get_value(indx,'typeOfMatch') == 3 or  dataFrame.get_value(indx,'typeOfMatch') == 1 or dataFrame.get_value(indx,'typeOfMatch') == 2 or  dataFrame.get_value(indx,'typeOfMatch') == '3\r\n' or dataFrame.get_value(indx,'typeOfMatch') == '2\r\n' or dataFrame.get_value(indx,'typeOfMatch') == '1\r\n':
        dataFrame.set_value(indx,'typeOfMatch',1)
        pos = pos + 1

    
uniqArt = set(dataFrame['article'].values)
print(uniqArt)
simp = []
stand = []
typ = []
art = []
finalDF = pd.DataFrame(columns = ['article','simpSent','StandSent','typeOfMatch'])
for each in uniqArt:
    #get the simple frame of simple,stand sentences,type of match
    subFrame = dataFrame[dataFrame['article'] == each]
    #get the unique simp sentences
    uniqSimp = set(subFrame['simpSent'].values)
    print('len of uniq simple',len(uniqSimp))
    count = 0
    for each_simp in uniqSimp:
        #get the index with typeOfMatch = 1 0r 2 or 3
        sub = dataFrame[dataFrame['simpSent'] == each_simp]
        #get the frame with 1 or 2 or 3 
        sub1 = sub[sub['typeOfMatch'] == 1]
        if len(sub1) == 0:
            continue
        count = count + len(sub1)
        print('count : ',count)
        for row in sub1.iterrows():
            index = row[0]
            start = 0
            if index > 2 :
                start = index - 2
            for i in range(start,index + 2):
                simp.append(dataFrame.get_value(i,'simpSent'))    
                stand.append(dataFrame.get_value(i,'standSent'))                
                typ.append(dataFrame.get_value(i,'typeOfMatch'))
                art.append(each)        
            
finalDF['article'] = art
finalDF['simpSent'] = simp
finalDF['standSent'] = stand
finalDF['typeOfMatch'] = typ

finalDF = finalDF.drop_duplicates(['simpSent','standSent'])    

print(len(finalDF))
print('pos ',len(finalDF[finalDF['typeOfMatch'] == 1]))

finalDF.to_csv(r'C:/Personal Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/TestReArrange.csv',encoding='utf8')
