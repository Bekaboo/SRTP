import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import data2neo

handler = data2neo.FromFile(filepath="data/tree.xls",
                            graph_auth=("neo4j", "bekaboo"))
handler.graph.delete_all()
handler.file2nodes()
handler.file2relations()
