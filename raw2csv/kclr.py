import os
import json

def SaveDataset(filename, dataset):
    dict_json = json.dumps(dataset)
    with open(filename,'w+') as f:
        f.write(dict_json)
        f.close()

def LoadDataset(filename):
    with open(filename,'r+') as f:
        read_dict = f.read()
        f.close()
    read_dict = json.loads(read_dict)
    return read_dict

with open('./data/0-5.CSV','r',encoding='utf-8') as f:
    content = f.readlines()
    f.close()

content = content[1:]
kc_dict = {}
for line in content:
    line = line.strip('\n')
    st = line.split(',')
    kc_dict[st[0]] = {'NT':st[1],'EN':st[2],'MT':st[3],'EL':st[4],'MG':st[5]}

SaveDataset('./data/kc.json',kc_dict)