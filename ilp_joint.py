import json
#import pathos.multiprocessing as mp
import time
import math
import sys
import os
#import cPickle as pickle
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from os.path import join
from gurobipy import *
from collections import defaultdict
#from tqdm import tqdm
import article_utils
from time import sleep
from io import open
import math
__author__ = 'iralp'

noOfArticles = 0

labels = [0,1]
f = ""
# set the number of parallel processes to be run.
'''num_processes = mp.cpu_count() \
        if ilp_config.max_processes is None \
        else min(ilp_config.max_processes, mp.cpu_count())
'''

def get_entailment_score(args):
    """ Returns entailment score. First checks if the entailment score is cached,
    if not AI2 service is used to get the score."""
    arg1, arg2 = args
    if args in e_data:
        # print ".",
        # sys.stdout.flush()
        return (args, e_data[args])
    else:
        # print ".",
        # sys.stdout.flush()
        print (args)
        # return (args, ilp_utils.get_similarity_score(arg1, arg2))

def get_sentence_from_id(s_id, p_data):
    sent_to_id, id_to_args, arg_role_scores = p_data
    s_map =  {v: k for k, v in sent_to_id.items()}
    return s_map[s_id]


def joint_inference_ilp(path, article):
    """Generate ILP optimization function with constraints with the input data
    and run the gurobi optimizer.

    Args:
        process: A string representing process name.
        p_data: A tuple containing process (a string) and srl_data (a dictionary)
        f: A integer representing cross validation fold number.

    Returns:
        A tuple containing a list of ILP role assignment vars and a dictionary
        containing entailment scores that were used.
    """
    # print "\nProcessing process :", process,"\t"
    # Integer Linear Programming for Joint Inference.
    rel_path = "..\data\Data_format\ILP_1_8_log\\"
    art = str(article).split()
    article = art[0]
    ilp_out_path = os.path.join(os.path.dirname(__file__),rel_path)
    ilp_lp = ilp_out_path + "_" + article + "_ilp.lp"
    ilp_sol = ilp_out_path + "_" + article + "_ilp.sol"
    ilp_mps = ilp_out_path + "_" + article + "_ilp.mps"
    #\Azuki_bean_scores_ilp
    article = article.strip()
    simple_sens = article_utils.get_sentences(path,article + '_simple_article')
    print('simple sentences: ',len(simple_sens))
    std_sens = article_utils.get_sentences(path,article + '_standard_article')
    print('std sentences: ',len(std_sens))
  
        
    sentences = article_utils.get_sentences(path + "\Revisited\\",article + '_collection_scores')
    print('scores : ',len(sentences))
    print('sentence : ',sentences[0])
    
    lambda_1 = 0.8
    print ("LAMBDA : ",lambda_1)
    lambda_2 = 0.2 #populate a map of similarity scores for the sentence pairs
    role_score_vals = {}
    label_indicator = {}
    # alignment_indicator = {}
    # temp_indicator = {}

    lp = Model(article+'_ilp')
    # Supress Gurobi Output
    lp.setParam('OutputFlag', True)
    sentences = list(filter(lambda a :a!= '\n',sentences))
    indx = 0
    len_of_std = len(std_sens)
    len_of_simple = len(simple_sens)
      
    #if article == 'Absolute_zero':
     #   len_of_simple = 16
        
    for std_indx in range(len_of_std):
        for simpl_indx in range(len_of_simple):
            line = sentences[indx]
            elements = line.split('\t')
            role_score = elements[4]
            role_score_vals[std_indx,simpl_indx] = float(role_score)
                
            for l_id, label in enumerate(labels):
                # add indicator variable
                label_indicator[std_indx,simpl_indx,l_id] = lp.addVar(vtype=GRB.BINARY,
                                                              name='Z_' + '(' + str(std_indx) +',' +  str(simpl_indx) + ')' +'_' + str(l_id))
                '''if std_indx == 0 and simpl_indx == 8 and l_id == 0:
                    print('inserted')
                    print(label_indicator[std_indx,simpl_indx,0])'''
            indx += 1
            
    print('role_score_vals : ',len(role_score_vals))
    print('label indicators : ',len(label_indicator))
        
    lp.update()
    
    '''for k,s in role_score_vals.items():
        if s < 0.5:
            role_score_vals[k] = 0
        else:
            role_score_vals[k] = s
    '''
    sent_corefs_map = {}
    pair_indices_map = {}
    for indx in range(len(sentences)):
        simpl_indx,std_indx,simple_corefs,stand_corefs = article_utils.get_sentence_corefs(indx,article,len(simple_sens))
        pair_indices_map[indx] = (std_indx,simpl_indx)
        list_of_coref_pairs = []
        #print('indx : ',indx)
        #print('simple_corefs : ',simple_corefs)
        #print('stand_corefs : ',stand_corefs)
        for ind1 in stand_corefs:
            for ind2 in simple_corefs:
                list_of_coref_pairs.append((ind1-1,ind2-1))
        sent_corefs_map[std_indx,simpl_indx] = list_of_coref_pairs

    #print('sent_corefs_map : ',sent_corefs_map)
    
    
    # generate the objective function to maximize the score
    print ("- generating objective function for article:", article)
    # black_listed_process = [line.rstrip() for line in open('filtered_process')]

    obj = LinExpr()
    for l_id, label in enumerate(labels):
        for s_id1 in range(len(sentences)):
            tuples = pair_indices_map[s_id1]
            coref_pairs = sent_corefs_map[tuples[0],tuples[1]]  
            delta = 0
            div = 1.0
            nabla = 0
            div2 = 1.0
                
            for pair in coref_pairs:
                dist1 = math.fabs(int(pair[0]) - int(tuples[0]))
                dist2 = math.fabs(int(pair[1]) - int(tuples[1]))
                totDist = dist1 + dist2
                logDist = math.log2(totDist)
                invLogDist = (1/logDist)
                if label != 'NONE':
                    #if ilp_config.penalty_ilp == True:
                    for l_id2, label2 in enumerate(labels):
                        #not aligned,then reduce the score of the original pair
                        if (label == 1 and label2 == 0):
                            # delta += temp_indicator[s_id1, a_id1, s_id2, a_id2, r_id] * sim_data2[(arg1, arg2)]
                            delta += label_indicator[pair[0],pair[1], l_id2] * role_score_vals[pair[0],pair[1]] * (invLogDist) 
                            div += (1 * (invLogDist))
                        if (label == 0 and label2 == 1):
                        #increase the score of the pair
                        # nabla += temp_indicator[s_id1, a_id1, s_id3, a_id3, r_id2] * sim_data2[(arg1, arg3)]
                            nabla += label_indicator[pair[0],pair[1], l_id2] * role_score_vals[pair[0],pair[1]] * (invLogDist)
                            div2 += (1 * invLogDist)
            obj += label_indicator[tuples[0], tuples[1], l_id] * ((float(role_score_vals[tuples[0], tuples[1]]) * lambda_1) + (lambda_2 * (nabla/float(div2) - delta/float(div))))
                # obj += label_indicator[s_id1, a_id1, r_id] * ((float(role_score_vals[s_id1, a_id1, r_id]) * lambda_1) + (lambda_2 * (delta/float(div)))) - (lambda_2 * (nabla/float(div2)))

    lp.setObjective(obj, GRB.MAXIMIZE)
    lp.update()

    print('updated the optimizer')
    # Constraints
    #find the shorter of the two documents and then set one of the following two constraints
    
    if len(std_sens) < len(simple_sens):
        print('here 1')
        # Every sentence in standard article should be aligned with only one sentence in simple article 
        for std_indx in range(len(std_sens)):
                lp.addConstr(quicksum([label_indicator[std_indx, simpl_indx,1] for simpl_indx in range(len(simple_sens))]) <= 1, 'constraint1_standard_' + str(std_indx))
    
    else:
        print('here 2 ')
        # Every sentence in simple article should be aligned with only one sentence in standard article 
        for simple_indx in range(len(simple_sens)):
            lp.addConstr(quicksum([label_indicator[std_indx, simple_indx, 1] for std_indx in range(len(std_sens))]) <= 1, 'constraint1_simple_' + str(simple_indx))
        
    print('constraints set')
    lp.optimize()

    print('optimize done')  
    print('output path : ',join(ilp_out_path,'output', article +'_ilp.lp'))
    lp.write(ilp_lp)
    lp.write(ilp_sol)
    lp.write(ilp_mps)

    global noOfArticles
    noOfArticles += 1
    print ("Finished ",article,"\n")
    print('Finished : ',noOfArticles,"\n")
    return ([(var.varName, var.x) for var in lp.getVars()], role_score_vals)


def get_ilp_assignment(lp_vars, p_data):
    """Returns ilp assignments given ilp output vars and the tuple p_data"""
    output_map = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for var, ind in lp_vars:
        var_ids = var.split("_")
        if var_ids[0] == 'Z':
            s = int(var_ids[1])
            a = int(var_ids[2])
            r = int(var_ids[3])
            output_map[s][a][r] = int(ind)
        elif var_ids[0] == 'A':
            pass
            # s1 = int(var_ids[1])
            # a1 = int(var_ids[2])
            # s2 = int(var_ids[3])
            # a2 = int(var_ids[4])
            # output_map[s1, a1, s2, a2] = int(ind)
    return output_map

def process_data(file_path,article):
    """Process srl data by calling joint_inference_ilp, getting ilp assignments,
    scores and normalizing them.

    Args:
        p_data: A tuple containing process (a string) and srl_data (a dictionary)

    Returns: A tuple containing process name, ilp assignments and normalized ILP
    scores.
    """
   
    #load the data
    
    # print '\n', process
    lp_vars, sim_data = joint_inference_ilp(file_path,article)
    #print('lp_vars : ',lp_vars)
    #ilp_map = get_ilp_assignment(lp_vars, srl_data[process][:3])
    #process_ilp_scores = ilp_utils.get_ilp_scores(process, srl_data, sim_data)
    # norm_ilp_scores = ilp_utils.normalize_ilp_scores(process_ilp_scores)
    #return (process, ilp_map, process_ilp_scores)
    # return (process, ilp_map, norm_ilp_scores)


def process_fold(article_file_path, ilp_out_path, f):
    """Process srl output file in srl_file_path, call ilp optimizer and dump
    the output in ilp_out_path.

    Args:
        srl_file_path: Path of the input srl file (string)
        ilp_out_path: Path of the ilp output file (string)
    """
    article_data = article_utils.load_article_data(article_file_path+"all_articles")
    
    for article in article_data:
        print ('article : ',article) 
        process_data(article_file_path,article)
		   
    


def plot_pr_overall_concatenated(srl_fold_data, ilp_fold_data, semafor_fold_data, easysrl_fold_data):
    """Plots overall precision recall after joining data from all the folds"""
    # concatenate data from all folds into a single dictionary which has
    # as key (sentence_id, start_index, end_index)
    # as value (gold_role, (predicted_role, prediction_score))
    # (i.e all fold id based separation is taken off).
    srl_all_data = {}
    for f, f_data in srl_fold_data.iteritems():
        srl_all_data.update(f_data)

    ilp_all_data = {}
    for f, f_data in ilp_fold_data.iteritems():
        ilp_all_data.update(f_data)

    '''
    semafor_all_data = {}
    for f, f_data in semafor_fold_data.iteritems():
        semafor_all_data.update(f_data)
    
    easysrl_all_data = {}
    for f, f_data in easysrl_fold_data.iteritems():
        easysrl_all_data.update(f_data)
    '''
    # SRL Stuff
    # check documentation above :)
    filtered_srl_correct = filter(lambda x: x[1][0] in ilp_config.positive_roles or x[1][1][0] in ilp_config.positive_roles, srl_all_data.items())
    sorted_srl_correct = sorted(filtered_srl_correct, key=lambda x: x[1][1][1], reverse=True)

    srl_yield = []
    gold_role_total = 0
    gold_role_predicted = 0
    total_role_predicted = 0

    for x in sorted_srl_correct:
        key, data = x
        gold_role, srl_data = data
        srl_role, srl_score = srl_data

        if gold_role in ilp_config.positive_roles:
            gold_role_total += 1
            if srl_role == gold_role:
                gold_role_predicted += 1

        if srl_role in ilp_config.positive_roles:
            total_role_predicted += 1

        if gold_role_predicted != 0 and total_role_predicted != 0:
            precision = gold_role_predicted/float(total_role_predicted)
        else:
            precision = 0
        srl_yield.append((gold_role_predicted, gold_role_total, precision))

    srl_df = pd.DataFrame(srl_yield)
    srl_df.columns = ['yield', 'total_predicted', 'precision']
    srl_df['recall'] = srl_df['yield']/max(srl_df.total_predicted.tolist())
    srl_yield_df = srl_df.set_index(['recall'])
    srl_yield_df = srl_yield_df['precision']
    srl_plot_df = pd.DataFrame(srl_yield_df)
    overall_precision = gold_role_predicted/float(total_role_predicted)
    overall_recall = gold_role_predicted/float(gold_role_total)
    overall_f1 = 2 * overall_precision * overall_recall/(overall_precision + overall_recall)
    
    print ("SRL\t\t P : "+str(overall_precision)+" R: "+str(overall_recall)+" F1: "+str(overall_f1))

    # ILP Stuff
    # check documentation above :)
    filtered_ilp_correct = filter(lambda x: x[1][0] in ilp_config.positive_roles or x[1][1][0] in ilp_config.positive_roles, ilp_all_data.items())
    sorted_ilp_correct = sorted(filtered_ilp_correct, key=lambda x: x[1][1][1], reverse=True)

    ilp_yield = []
    gold_role_total = 0
    gold_role_predicted = 0
    total_role_predicted = 0

    for x in sorted_ilp_correct:
        key, data = x
        gold_role, ilp_data = data
        ilp_role, ilp_score = ilp_data
        if gold_role in ilp_config.positive_roles:
            gold_role_total += 1
            if ilp_role == gold_role:
                gold_role_predicted += 1

        if ilp_role in ilp_config.positive_roles:
            total_role_predicted += 1
        if gold_role_predicted != 0 and total_role_predicted != 0:
            precision = gold_role_predicted/float(total_role_predicted)
        else:
            precision = 0
        ilp_yield.append((gold_role_predicted, gold_role_total, precision))

    ilp_df = pd.DataFrame(ilp_yield)
    ilp_df.columns = ['yield', 'total_predicted', 'precision']
    ilp_df['recall'] = ilp_df['yield']/max(ilp_df.total_predicted.tolist())
    ilp_yield_df = ilp_df.set_index(['recall'])
    ilp_yield_df = ilp_yield_df['precision']
    ilp_plot_df = pd.DataFrame(ilp_yield_df)
   
    if (total_role_predicted == 0):
        overall_precision = 0
    else: 
        overall_precision = gold_role_predicted/float(total_role_predicted)
    overall_recall = gold_role_predicted/float(gold_role_total)
    if (overall_precision == 0 and overall_recall == 0):
        overall_f1 = 0
    else:
        overall_f1 = 2 * overall_precision * overall_recall/(overall_precision + overall_recall)
    print (gold_role_predicted,"\t", float(gold_role_total))
    print ("ILP\t\t P : "+str(overall_precision)+" R: "+str(overall_recall)+" F1: "+str(overall_f1))
    f = open('lambda_eval_scores.txt', 'a')
    f.write(str(ilp_config.lambda_1)+"\t"+str(overall_precision)+"\t"+str(overall_recall)+"\t"+str(overall_f1)+"\n")
    f.close()
    
def ev():
    srl_fold_data = {}
    ilp_fold_data = {}
    semafor_fold_data = {}
    easysrl_fold_data = {}
    for f, fold_dir in enumerate(listdir(ilp_config.cross_val_dir)):
        fold_path = join(ilp_config.cross_val_dir, fold_dir)

        d_gold_file = join(fold_path, 'test', 'test.srlout.json')
        d_gold = json.load(open(d_gold_file, "r"))
        gold_data = ilp_utils.get_gold_data(d_gold)

        d_srl_file = join(fold_path, 'test', 'test.srlpredict.json')
        d_srl = json.load(open(d_srl_file, "r"))
        srl_data = ilp_utils.get_prediction_data(d_srl)

        d_ilp_file = join(fold_path, 'test', 'test.ilppredict.json')
        d_ilp = json.load(open(d_ilp_file, "r"))
        ilp_data = ilp_utils.get_prediction_data(d_ilp)
        ''' 
        d_semafor_file = join(fold_path, 'test', 'test.semaforpredict.json')
        d_semafor = json.load(open(d_semafor_file, "r"))
        semafor_data = ilp_utils.get_prediction_data(d_semafor)

        d_easysrl_file = join(fold_path, 'test', 'test.easysrlpredict.json')
        d_easysrl = json.load(open(d_easysrl_file, "r"))
        easysrl_data = ilp_utils.get_prediction_data(d_easysrl)
        '''
        srl_analysis_data = {k: (gold_data[k], v) for k, v in srl_data.iteritems() if k in gold_data}
        ilp_analysis_data = {k: (gold_data[k], v) for k, v in ilp_data.iteritems() if k in gold_data}
        #semafor_analysis_data = {k: (gold_data[k], v) for k, v in semafor_data.iteritems() if k in gold_data}
        #easysrl_analysis_data = {k: (gold_data[k], v) for k, v in easysrl_data.iteritems() if k in gold_data}

        srl_fold_data[f+1] = srl_analysis_data
        ilp_fold_data[f+1] = ilp_analysis_data
        #semafor_fold_data[f+1] = semafor_analysis_data
        #easysrl_fold_data[f+1] = easysrl_analysis_data
    
    print ("-- Plotting [Overall] [Separate] plots.")
    #plot_pr_overall(srl_fold_data, ilp_fold_data, semafor_fold_data, easysrl_fold_data)
    print ("-- Plotting [Role] [Sepatate] plots.")
    #plot_pr_role(srl_fold_data, ilp_fold_data, semafor_fold_data, easysrl_fold_data)
    print ("-- Plotting [Overall] [Concatenated] plots.")
    plot_pr_overall_concatenated(srl_fold_data, ilp_fold_data, semafor_fold_data, easysrl_fold_data)


def sweep():
    print ("Using", num_processes, "parallel processes")
    file_obj = open('ilp_scores.txt', 'w+')
    file_obj.close()
    # iterate through cross-val folds and process srlpredict json to generate
    # ilppredict json by running ilp
    for f, fold_dir in enumerate(listdir(ilp_config.cross_val_dir)):
        print ("\n- fold:", f)
        fold_path = join(ilp_config.cross_val_dir, fold_dir)
        srl_predict_file_path = join(fold_path, 'test', 'test.srlpredict.json')
        ilp_predict_file_path = join(fold_path, 'test', 'test.ilppredict.json')
        process_fold(srl_predict_file_path, ilp_predict_file_path, f)
    sleep(5)
    ev() 
    print ("\n- Done!")

def main():
    article_file_path = "..\Data\Data_format\\"
    ilp_out_path = "..\data\Data_format\output\\"
    process_fold(article_file_path, ilp_out_path, f)
    sleep(5)
    #ev() 
    print ("\n- Done!")
   # sleep(3)
if __name__ == '__main__':
    main()


