# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 19:15:05 2016

@author: iralp
"""

pathToWrite = 'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/'
#read the annotations file
with open(r'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/annotations.txt',encoding = "utf8") as fd:
    lines = fd.readlines()

lines = list(filter(lambda a: a != '\n', lines))

simple_sent = []
stand_sent = []
prevArticle = "A.C.F._Fiorentina"
all_articles = []
all_sentences = []

total_simple = 0
total_standard = 0
total_collection = 0

cur_length_simple = 0 
cur_length_standard = 0
cur_length_collection = 0
 
count = 2

def checkPresenceAndAdd(candidate,listToAddTo,collection = False):
    if collection == False:
        for idx in range(len(listToAddTo)):
            if listToAddTo[idx] == candidate:
               # if len(candidate) < 3:
                    #print("Matched : ",candidate)
                return
    listToAddTo.append(candidate)

def writeToFile(fileDesc,listToWrite):
    for idx in range(len(listToWrite)):
        fileDesc.write(listToWrite[idx])
        fileDesc.write("\n")
        

def writeToStandard(article_name,listToWrite):
    #open the file to write to in write mode
    print("article : ",article_name," len(standard_sentences) : ",len(listToWrite))
    global total_standard
    total_standard = total_standard + len(listToWrite)
    global cur_length_standard
    cur_length_standard = len(listToWrite)
    fd = open(pathToWrite + article_name + "_standard_article",'w+',encoding = "utf8")
    writeToFile(fd,listToWrite)
    fd.close()
    
def writeToSimple(article_name,listToWrite):
    #open the file to write to in write mode
    print("article : ",article_name," len(simple_sentences) : ",len(listToWrite))
    global total_simple
    total_simple = total_simple + len(listToWrite)
    global cur_length_simple
    cur_length_simple = len(listToWrite)
    fd = open(pathToWrite + article_name + "_simple_article",'w+',encoding = "utf8")
    writeToFile(fd,listToWrite)
    fd.close()
    
    
def writeToCollection(article_name,listToWrite):
    #open the file to write to in write mode
    print("article : ",article_name," len(collection) : ",len(listToWrite))
    global total_collection
    total_collection = total_collection + len(listToWrite)
    global cur_length_collection
    cur_length_collection = len(listToWrite)
    product = cur_length_simple * cur_length_standard
    if cur_length_collection != product:
        print('article_name',article_name)
    fd = open(pathToWrite + article_name + "_collection",'w+',encoding = "utf8")
    writeToFile(fd,listToWrite)
    fd.close()
    
for each_line in lines:
    #split the sentences to get individual parts
    splits = each_line.split('\t')
    #print(len(splits))
    current = str(splits[0]).strip()
    if current == prevArticle:
        #article name to the list
        checkPresenceAndAdd(current,all_articles)
        #first becomes the standard wikipedia sentence
        checkPresenceAndAdd(splits[1],stand_sent)
        #second becomes the simple wikipedia sentence
        checkPresenceAndAdd(splits[2],simple_sent)
        #add the entire sequence
        checkPresenceAndAdd(each_line,all_sentences,True)
    else:
        #moving to the next article
        #write the current article into respective files
        writeToStandard(prevArticle,stand_sent)
        writeToSimple(prevArticle,simple_sent)
        writeToCollection(prevArticle,all_sentences)
        
        #empty all the lists and add the current item
        simple_sent = []
        stand_sent = []
        all_sentences = []
        prevArticle = splits[0]
        
        #article name to the list
        checkPresenceAndAdd(current,all_articles)
        #first becomes the standard wikipedia sentence
        checkPresenceAndAdd(splits[1],stand_sent)
        #second becomes the simple wikipedia sentence
        checkPresenceAndAdd(splits[2],simple_sent)
        #add the entire sequence
        checkPresenceAndAdd(each_line,all_sentences,True)
        

#moving to the next article
#write the current article into respective files
writeToStandard(prevArticle,stand_sent)
writeToSimple(prevArticle,simple_sent)
writeToCollection(prevArticle,all_sentences)

print('total_simple : ',total_simple)
print('total_standard : ',total_standard)
print('total_collection : ',total_collection)