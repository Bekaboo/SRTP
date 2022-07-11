# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 14:26:05 2022
@author: XSRTP0522-PJTEAM
"""

import os
import re
import csv
from raw2csv.doc2dict import *
from raw2csv.dict2csv import *

inc = inc2dict('./raw2csv/data/phys_.txt')
prq = prq2dict('./raw2csv/data/prq.txt')
sub_d = subNchap('./raw2csv/data/sub.txt')


info_dict = {}
info_dict['subs'] = sub_d
info_dict['chap_list'] = inc['chap_list']
info_dict['know_list'] = inc['know_list']
info_dict['chap_know'] = inc['chap_know']
info_dict['prq'] = prq

dict2csv(info_dict)