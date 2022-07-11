# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 00:03:21 2022
@author: XSRTP0522-TEAM
"""

import os
import re
import csv



"""
inc2dict is the first step to build the knowledge graph database.

Input: A well-organized document, the form is stated in "form.txt"

Output: A dictionary, with the {key, value} as follows:
    Key 0: chap_list (dictionary), Value 0: a dictionary of {chapter code: chapter}
    Key 1: know_list (dictionary), Value 1: a dictionary of {knowledge point code: knowledge point}
    Key 2: chap_know (dictionary), Value 2: a dictionary of {chapter code: knowledge point code}
"""
def inc2dict(filename):
    doc_2_dict = {}
    with open(filename,'r',encoding='utf-8') as f:
        context = f.readlines()
        f.close()
    
    chap_code = 0
    chap_list = {}
    know_list = {}
    chap_know = {}
    for line in context:
        line = line.strip('\n')
        line_list = line.split(' ')
        if (line_list[0]=='Chapter'):
            chap_name = '_'.join(line_list[2:])
            chap_code = line_list[1]
            chap_list[chap_code] = chap_name
            chap_know[chap_code] = []
        else:
            know_name = '_'.join(line_list[1:])
            know_list[line_list[0]] = know_name
            chap_know[chap_code].append(line_list[0])
    doc_2_dict['chap_list'] = chap_list
    doc_2_dict['know_list'] = know_list
    doc_2_dict['chap_know'] = chap_know
    return doc_2_dict



"""
subNchap is a preparation step to build the relationship between sub-discipline and chapters

Input: A well-organized document, the form is stated in "form.txt"

Output: A dictionary, {sub-topic: chap code}

"""
def subNchap(filename):
    with open(filename,'r',encoding='utf-8') as f:
        context = f.readlines()
        f.close()
        
    sub_dict = {}
    for line in context:
        line = line.strip('\n')
        line_list = line.split(' ')
        sub_dict[line_list[0]]=line_list[1:]
    
    return sub_dict



"""
prq2dict: Construct the topology graph, implemented by a dict, implying the pre-requisite relationship.

Input: A well-organized document, the form is stated in "form.txt"
    
Output: A dictionary, {key: value} implies {u1,u2} where (u1,u2) is a topology edge, u1 to u2. 
    
"""
def prq2dict(filename):
    with open(filename,'r',encoding='utf-8') as f:
        context = f.readlines()
        f.close()

    node_dict = {}
    for line in context:
        line = line.split(' ')
        x = line[0]
        y = line[1].strip('\n')
        if (not x in node_dict.keys()):
            node_dict[x] = []
            node_dict[x].append(y)
        else:
            node_dict[x].append(y)
            
    return node_dict