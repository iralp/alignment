# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 17:32:28 2016

@author: iralp
"""

from pycorenlp import StanfordCoreNLP
#import pprint
import json


with open(r'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_Format/all_articles',encoding='utf8') as fd:
    lines = fd.readlines()
    
nlp = StanfordCoreNLP("http://localhost:9000")

count = 0
for each_articles in lines:
    each_articles = each_articles.strip()
    with open(r'C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/'+each_articles+'_standard_article',encoding = 'utf8') as fd:
        lines = fd.readlines()
        
    #lines = "Pranathi is good.She is the best"
    output = nlp.annotate("".join(lines), properties={
      'annotators': 'mention,coref',
      'outputFormat': 'json',
      'timeout':'10000000'
      })
    
    count += 1
    print('article name :',each_articles)
    print('count : ',count)
    
    #with open('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/Azuki_bean_simple_corefs_string', 'w+',encoding = 'utf8') as outfile:
        #json.dump(output,outfile)
     #   outfile.write(output)
    
    #outputJson = json.loads(output)  
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(output['corefs'])
        
    with open('C:/Personal_Docs/Course_Work/NLP/Simple_Standard_Wiki_ALignment/Data/Data_format/'+ each_articles +'_standard_corefs', 'w+',encoding = 'utf8') as outfile:
        if isinstance(output,dict) and ('corefs' in output.keys()):
            json.dump(output['corefs'],outfile)
        else:
            json.dump(output,outfile)