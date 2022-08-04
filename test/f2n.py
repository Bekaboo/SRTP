import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import data2neo

# account = input("Your account to neo4j server: ")
# passwd = input("Your password to neo4j server: ")

account = 'neo4j'
passwd = 'neo4j123456'

handler = data2neo.FromFile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "../raw2csv/data/data_KG.csv"), graph_auth=(account, passwd))
handler.graph.delete_all()
handler.file2nodes()
handler.file2relations()
