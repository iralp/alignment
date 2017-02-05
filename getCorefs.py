# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 00:46:57 2016

@author: iralp
"""

import json
from copy import deepcopy
#get the list of dependencies

print("executing")
#open json file
#json_data = open('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/Advaita_Vedanta_standard_corefs').read()

articles = None
article_path = 'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/all_articles'
with open(article_path,encoding='utf8') as fd:
        articles = fd.readlines()
        
        
json_data = None
for indx in range(len(articles)):
    try:
        each_ = articles[indx]
        each_art = str(each_)
        each_art = each_art.split('\n')
        each_article = each_art[0]
        print('each_article : ',each_article)
        with open(r'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/'+each_article+'_simple_corefs') as json_file:
            print('reading')
            json_data = json_file.read()
        
        new_string = str.replace(json_data,"\\","")
        #new_string = str.replace(new_string,"\"","")
            
        #print('new_string : ',new_string)
        new_json = json.loads(new_string, strict = False)
        
        #print("new_json :",new_json)
        #new_string = str.replace(new_json,"\\","")
        #new_string = str.replace(new_json,"'","\"")
        #print(new_json)
        jsonData = new_json
        #['corefs']
        
        #print("jsonData : ",jsonData)
        
        #new_string = str.replace(jsonData,"'","\"")
        sent_dict = {}
        count = 5
        #dicJson = json.loads(new_string)
        
        print("I am here")
        
        #now map the individual sentences to corresponding sentences in the article
        with open('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/'+ each_article +'_simple_article',encoding = "utf8") as fd:
            lines = fd.readlines()
        
        mapping = {}
        indx = 0
        print("length of lines : ",len(lines))
        count = 0
        while indx < (len(lines)):
            line = lines[indx]
            nos = line.split(".")
            print('indx : ',indx)
            print("nos : ",len(nos))
            #print(nos)
            if len(nos) == 1 or len(nos) == 2:
                mapping[count + 1] = indx + 1
                count = count + 1
            else:
        		#map the next sentences to this indx
              lenOfSens = len(nos)
              temp = indx
              #print('lenOfSens : ',lenOfSens)
              while lenOfSens > 1:
                  print('indx + lenOfSens - 1',indx + lenOfSens - 1 ,'indx + 1',count + 1)
                  mapping[count + lenOfSens - 1] = indx + 1
                  lenOfSens = lenOfSens - 1
              count = count + len(nos) - 1
              #count = count + len(nos) - 1
            indx = indx + 1
        
        print('final mapping ',mapping)
        print('jsonData keys :',jsonData.keys())
        
        #jsonData = new_json
        for each in jsonData.keys():
            value = jsonData[each]
            len_of_list = len(value)
            lst = []
            print('each : ',each)
            for each_entry in value:
                if 'sentNum' not in each_entry.keys():
                    continue
                sentNum = each_entry['sentNum']
                if sentNum == 112:
                    print('each_entry : ',each_entry)

                lst.append(mapping[sentNum])       
                
            for each_val in lst:
                #print('lst : ',lst)
                if each_val not in sent_dict.keys():
                    sent_dict[each_val] = deepcopy(lst)
                    #print('sent_dict : ',sent_dict)
                else:
                    prev_lst = sent_dict[each_val]
                    #print('prev_lst : ',prev_lst)
                    prev_lst.extend(lst)
                    sent_dict[each_val] = prev_lst
                    #print('sent_dict',sent_dict)
            #print(value)
            '''count = count - 1
            if count == 0:
                break'''
            
        for each_key in sent_dict.keys():
            values = sent_dict[each_key]
            set_of_values = set(values)
            if each_key in set_of_values:
                set_of_values.remove(each_key)
            sent_dict[each_key] = list(set_of_values)
            
            
        print("length of dictionary : ",len(sent_dict))
        #print(sent_dict)
        
        with open('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/New_Corefs/'+ each_article +'_simple_corefs_pairs','w+') as outfile:
            json.dump(sent_dict,outfile)
    except Exception as e:
        print("Error : ",e)
        break