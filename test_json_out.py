# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 06:45:40 2019

@author: Constantin Pap
"""

import json


with open("sem_rel_compounds_vec.json") as test:
    dictionary = json.load(test)
    m_list = list(dictionary.values())
    d_list = list(dictionary.keys())
    print(len(m_list))
    for n in range (len(m_list)):
        for k,v in m_list[n].items():
            if(v > 0):
                print(d_list[n], k, v)