import json
from io import open
import os

def load_article_data(article_file_path):
    abs_path = os.path.join(os.path.dirname(__file__),article_file_path)
    with open(abs_path,encoding='utf8') as fd:
        articles = fd.readlines()
        articles = list(filter(lambda a: a != '\n', articles))
    return articles

def get_sentences(path,article):
    total_path = path + article
    scoreLines = load_article_data(total_path)
    return scoreLines
    
def get_sentence_corefs(indx,article,simple):
    #print('indx : ',indx)
    #find the length of simple,stand documents
    #simple = 48
    #stand = 36
    #get the index of the simple and the stand sentence corresponding to the indx given
    stand_indx = int(indx/simple)
    simple_indx = int(indx % simple)
    simple_corefs = []
    stand_corefs = []

    #print('simple_indx : ',simple_indx)
    #print('stand_indx : ',stand_indx)
    article_path1 = '../data/Data_format/New_Corefs/' + article + '_simple_corefs_pairs'
    abs_path = os.path.join(os.path.dirname(__file__),article_path1)
    
    #get the corefs for simple sentence
    json_data_simple = open(abs_path).read()
    new_json = json.loads(json_data_simple)
    key1 = str((simple_indx + 1))
    if  key1 in new_json.keys():
        simple_corefs = new_json[key1]
    
    article_path2 = '../data/Data_format/New_Corefs/' + article + '_standard_corefs_pairs'
    abs_path2 = os.path.join(os.path.dirname(__file__),article_path2)
    
    #get the corefs for simple sentence
    json_data_std = open(abs_path2).read()
    new_json_std = json.loads(json_data_std)
    key2 = str((stand_indx + 1))
    if  key2 in new_json_std.keys():
        stand_corefs = new_json_std[key2]
    
    return simple_indx,stand_indx,simple_corefs,stand_corefs
    
    
    
    
