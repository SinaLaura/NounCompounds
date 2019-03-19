# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:31:51 2019

Weiterführung für semantic_project_compound_firststep.py
@author: Constantin Pap
"""
#import numpy as np
import re
import json
#import spacy
#import nltk
#import os, sys
#import logging
#import datetime
#import matplotlib.pyplot as plt

"""
extract_compound_data(filename):
    
@input filename
@output compounds sind die zusammengesetzten compounds in einen string (mit whitespace) und classes enthält alle classes zu den compounds

"""
def extract_compound_data(filename):
    open_file = open(filename, "r", encoding="utf-8", errors="ignore")
    compounds = []
    classes = []
    for line in open_file.readlines():
        if(len(line.split("\t"))== 3):
            line_splitted = line.split("\t")
            compounds.append(line_splitted[0] + " " + line_splitted[1])
            classes.append(line_splitted[2][:-1])
    return compounds, classes

"""
extract_compound_sents_data(filename):
    
@input filename
@output compound_sents_list ist eine liste aus geSTRINGten Sätzen

"""
def extract_compound_sents_data(filename):
    open_file = open(filename, "r", encoding="utf-8", errors="ignore")
    compound_sents_list = []
    used_list = []
    for line in open_file.readlines():
        if(line.startswith("[")):
           used_list = eval(line) #eval(x) damit man direkt den Inhalt der Datei als code (list) einlesen kann
           compound_sents_list.append(" ".join(used_list))
    return compound_sents_list

"""
define_verb_dic(sents)

@input sents aus extract_compound_sents_data
@output verb_dic, welches alle unique verbs enthält mit einem key 0 - n
"""
def define_verb_list(sents):
    verb_list = []
    verb_dic = {}
    for sent in sents:
        if(verb_list.count(sent.split(" ")[2]) == 0):
            verb_list.append(sent.split(" ")[2])
    for counter in range(len(verb_list)):
        verb_dic[counter] = verb_list[counter]
        #print("{}:{}".format(counter,verb_list[counter]))
    return verb_list

"""
define_vectors(compounds, sents):
    
@input compounds sind alle Wortkombinationen aus extract_compound_data() und sents sind die Listen mit string Sätzen aus extract_compound_sents_data()
@output None, aber es wird eine JSON- Datei erstellt mit allen Vectoren

"""
def define_vectors(compounds, sents):   
    verb_list = define_verb_list(sents)
    completed_dic = {}
    completed_dic_with_vec = {}
    for com in compounds:
        print("{} von {}".format(compounds.index(com),len(compounds)+1))
        verb_occ = {}
        for verb in verb_list: #damit alle Einträge vorerst auf 0 gesetzt sind
            verb_occ[verb] = 0
        for s in sents:
            result = re.match(r"" + com.split(" ")[1] + "\s+(that|which)\s+([a-z]+)\s+" + com.split(" ")[0] + "",s)
            if(result != None):
                verb_occ[result.group(2)] = verb_occ.get(result.group(2)) + 1
        completed_dic[com] = verb_occ #{"apple pie":{"contain":12,"cook":2,...},"olive oil":{"??":22,"??":3,...}}
        completed_dic_with_vec[com] = verb_occ.values #{"apple pie":[12,2,0,0,0,0,0,0,0,0,0,2,0,0,2,....],"olive oil":[22,3,2,0,0,0,2,2,1,...]}      
    #json_completed_dic_with_vec = json.dumps(completed_dic)
    with open("sem_rel_compounds_vec.json", "w") as fout:
        json.dump(completed_dic, fout)
        
    return None

if __name__ == "__main__":
   print ("Start")
   print("Currently at: extracting compound data")
   #Da es nur zwei Dateien waren, die einzulesen waren, habe ich es simpel gehalten. ALle anderen ./train.tsv enthalten nahezu die gleichen compounds
   compound_list, classes_list = extract_compound_data("Data/tratz2011_coarse_grained_lexical_full/train.tsv")
   compound_list_two, classes_list_two = extract_compound_data("Data/tratz2011_fine_grained_lexical_full/train.tsv")
   compound_list += compound_list_two
   classes_list += classes_list_two
  
   #Diese Tests dienten nur dazu, dass es keine direkten Duplikate zu finden wären. Keine Treffer bei compound_list.count(com)>2.
   #indirekte Duplikate wären, wenn es zwei mal den gleichen Compound geben würde, diese aber einer unterschiedlichen class angehören würden.
   #for com in compound_list:
   #    if(compound_list.count(com)>1):
    #       print(compound_list.count(com), com, classes_list[compound_list.index(com)])
   #for compounds in compound_list[-50:]:
   #    print (compounds)

   #for classes in classes_list:
   #   print (classes)
   print("Finished with extracting compound data")
   print("Currently at: checking and counting verb occurences with their compounds")
   compound_sents_list = extract_compound_sents_data("compound.log")
   #for sent in compound_sents_list[:10]:
   #    print(sent)
   print("Finished with extracting compound sents")
   print("Currently at: define vectors")
   define_vectors(compound_list, compound_sents_list)
   print ("Finished")