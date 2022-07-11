# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:56:30 2022
@author: XSRTP0522-TEAM


"""

import os
import re
import csv


"""

dict2csv is a script for converting some information saved in a dict to a csv,
    which is used to import the data to neo4j

Input: info_dict:
    {'subs',{sub-topic code: chapter code}}
    {'chap_list',{chapter code: chapter}}
    {'know_list',{knowledge point code: knowledge point}}
    {'chap_know',{chapter code: knowledge point code}}
    {'prq',{point-out: point-in}}

Output: a csv file named "data_KG.csv".

Form:
    node_props: properties of the node.
        name: the knowledge represented by the node, like "Electricity".
        abl (only for Kpt): Ability, the kpt reflects what kind of ablility that a learner should obtain
        kc (only for Kpt): Knowledge color, (Newton, Energy, Momentum, Electricity, Magnetism)
    node_labels: labels of the node, seperated by ";".
        Sub: Sub-topic
        Chap: Chapter
        Kpt: Knowledge point
    relations: rela-type->node
        rela-type:
            Inc: Inclusion, A->B means A contains B
            Prq: Pre-requisite, A->B means required obtain A to learn B
        node:
            In general, properties1;properties2@label1;label2 for node
            We will only use name:'ABCDE' for property since we ensure that we won't have the same 
            name for two nodes.
        
"""
def dict2csv(info_dict):
    # 0. Import the data
    subs = info_dict['subs']
    chap_list = info_dict['chap_list']
    know_list = info_dict['know_list']
    chap_know = info_dict['chap_know']
    prq = info_dict['prq']
    with open('./raw2csv/data/data_KG.csv','w',encoding = 'utf-8') as f:
        f.write('node_props,node_labels,relations\n')
        # 1. Process the sub-chap relationship, inclusion.
        for sub in subs.keys():
            sub_chap_list = []
            for chap_name in subs[sub]:
                temp = "Inc"
                temp = temp + "->name:'" + chap_list[chap_name] + "'"
                # Will add other props later ...
                temp = temp + "@Chap"
                sub_chap_list.append(temp)
            chap = '|'.join(sub_chap_list)
            sub = "name:'" + sub + "'"
            f.write(sub + ',Sub,' + chap + '\n')
        # 2. Process the chap-know relationship, inclusion.
        for chap in chap_list:
            chap_know_list = []
            chap_name = chap_list[chap]
            for know_code in chap_know[chap]:
                know_name = know_list[know_code]
                temp = "Inc"
                temp = temp + "->name:'" + know_name + "'"
                # Will add other props later ...
                temp = temp + "@Kpt"
                chap_know_list.append(temp)
            kpt = '|'.join(chap_know_list)
            chap_name = "name:'" + chap_name + "'"
            f.write(chap_name + ',Chap,' + kpt + '\n')
        # 3. Add Kpt nodes
        for know in know_list:
            know_name = know_list[know]
            know_with_info = "name:'" + know_name + "'"
            know_with_info = know_with_info + ";" + "abl:'" + "0" + "'"
            know_with_info = know_with_info + ";" + "kc:'" + "0" + "'"
            f.write(know_with_info + ',Kpt' + '\n')
        # 4. Process the pre-requisite relationship.
        for u1 in prq.keys():
            f.write("name:'" + know_list[u1] + "'")
            f.write(',Kpt,')
            prq_list = []
            for u2 in prq[u1]:
                temp = "Prq"
                temp = temp + "->name:'" + know_list[u2] + "'"
                temp = temp + "@Kpt"
                prq_list.append(temp)
            prq_ = '|'.join(prq_list)
            f.write(prq_)
            f.write('\n')
        
        f.close()
    #csv2xls('./raw2xls/data/data_KG.csv')