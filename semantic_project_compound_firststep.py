# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 15:00:14 2019

Formale Semantik Projekt: Semantic relations with compounds
- Extraktion von Textdateien aus dem englishEtiquetado Wiki Corpus
- Definition einer regular expression zur Extraktion von compound sents
- Konstruieren von Vektoren für jedes compound (verb frequency)
- Erschaffen einer JSON- Datei mit allen Vektoren
@author: Constantin Pap
"""

import numpy as np
import re
#import spacy
import nltk
#import os, sys
import logging
import datetime
#import matplotlib.pyplot as plt

#logger für ein log file im gleichen Ordner. Enthält stats zur Corpora, wie Anzahl der NNs, verbs, that oder which und der compounds

logging.basicConfig(filename="compound.log", level = logging.INFO, 
                    format="%(message)s")

"""
extract_corpora(filename):
    
@input filename ist der Name der Datei die einzulesen ist
@output ist eine finale liste der einen Datei mit den compounds die gefunden wurden ['pie','that','contain','apple'] lammatisiert

"""

def extract_corpora(filename):
    open_file = open(filename, "r", encoding="utf-8", errors="ignore")
    #sents_collector sammelt die lemmatisierten Worte und pos_collector den dazugehörigen POS- tag
    sents_collector = []
    pos_collector = []
    #final_compound_sent sammelt alle compounds und gibt diese am ende als output zurück
    final_compound_sent = []
    for line in open_file.readlines():
        #Diese Bedingung ist dabei um die Dokumentanfänge und alle leeren Zeilen (z.B. "\n" Zeilenumbrüche) zu überspringen
        if(line.startswith("<doc id=") or len(line.split(" ")) <4 ):
            continue
        #Zeilenumbrüche noch einmal und das Ende eines Dokuments auch wenn diese keine direkte Auswirkung hätte auf die Selektierung/regex (wenn man es benutzt hätte)
        elif(line != "\n" and line.startswith("</doc>") == False):
            sents_collector.append(str(line.split(" ")[1]))#0 ist das Wort direkt, 1 ist lemma und 2 ist der POS- tag
            pos_collector.append(str(line.split(" ")[2]))
            
    #Siehe Zeilen 83-88
    nouns = pos_collector.count("NN")
    verbs = count_verbs(pos_collector)
    that = sents_collector.count("that")
    which = sents_collector.count("which")
            
    #Grundgedanke war, dass ich slices mache aus den collector listen (pos und sents) und diese dann in einer Bedingung direkt abzulaufen
    #Lief erstaunlicherweise gut. Demnach habe ich zumindest hierfür keine Regex benötigt. Das Problem an regex war, dass man einmal POS- tags und dann dazu auch noch 
    #die lemmas checken musste und zudem noch diese groups richtig setzen musste.
    wc = 0 #word_counter_for_compound_sent zum slicen in 4er sents
    for pos in pos_collector[:-3]:
            if(pos_collector[wc] == "NN" and
               (sents_collector[wc+1] == "that" or sents_collector[wc+1] == "which") and
               pos_collector[wc+2].startswith("V") and
               pos_collector[wc+3] == "NN"):
                final_compound_sent.append(sents_collector[wc:wc+4])
                logging.info("{}\n".format(sents_collector[wc:wc+4]))
            wc += 1
    
    #Siehe Zeile 83-88
    sum_compounds = len(final_compound_sent)
    return nouns, verbs, that, which, sum_compounds

#Diese Methode zählt alle "V.*" (in regexschreibform) und gibt diese Zahl aus. Funktioniert an sich wie die <list>.counter("??")
def count_verbs(collector):
    verbs = 0
    for every in collector:
        if(every.startswith("V")):
            verbs += 1
    return verbs
    
if __name__ == "__main__":

    #start und end für das Iterieren durch die Dateien. Hätte man auch sicherlich besser machen können. Tut aber was es soll.
    start = 0
    end = 1640000
   
    #Zählvariablen für die stats
    nouns_total = 0
    verbs_total = 0
    that_total = 0
    which_total = 0
    sum_compounds_total = 0
    
    print("Started")
    while start<1640000:
        print("Currently at:{}-{}".format(start,start+10000))
        nouns, verbs, that, which, sum_compounds = extract_corpora("corpora_wiki/EnglishEtiquetado_" + str(start) + "_" + str(start+10000))
        nouns_total += nouns
        verbs_total += verbs
        that_total += that
        which_total += which
        sum_compounds_total += sum_compounds
        start += 10000 
    #Stats werden ganz am Ende des Vorgangs zum Schluss an die Datei angehängt (muss beachtet werden beim Weiterarbeiten)
    logging.info("\nCompounds found:\t{}\nNN:\t{}\nVerbs:\t{}\nThat and which:\t{}-{}\n".format(sum_compounds_total,nouns_total,verbs_total,that_total,which_total))
    print("finished")