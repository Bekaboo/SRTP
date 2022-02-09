import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import ast
import data2neo

with open("data/list.txt") as list_file:
    list_data = list_file.read()
    list = ast.literal_eval(list_data)

handler = data2neo.FromList(list=list, graph_auth=("neo4j", "bekaboo"))
handler.graph.delete_all()
handler.list2nodes()
handler.list2relations()
