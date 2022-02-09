#!/usr/bin/env python
# coding: utf-8

#
import pandas as pd
import py2neo as neo


# This class is used to build a link between our datafile and the remote graph,
# subsequently create the nodes and relationships from the datafile.
class File2Neo(object):
    def __init__(self, filepath, graph_link="http://localhost:7474/",
                 graph_auth=("neo4j", "neo4j")):

        # Link to the remote graph.
        graph = neo.Graph(graph_link, auth=graph_auth)
        self.graph = graph
        self.filepath = filepath
        try:
            self.data = pd.read_excel(filepath)
        except ValueError:
            self.data = pd.read_csv(filepath, encoding="GB2312")

    def file2nodes(self):   # To create a graph, first create all the nodes.
        data = self.data
        graph = self.graph

        for i in range(data.index.stop):
            if not isinstance(data.nodes.loc[i], str):  # Eliminate `nan`.
                continue
            clause = "MERGE (:%s {name:'%s'})"\
                % (str(data.labels.loc[i]).strip(),
                   str(data.nodes.loc[i]).strip())
            clause = clause.replace("'nan'", "NULL")
            graph.run(clause)

    def file2relations(self):
        data = self.data
        graph = self.graph

        # Deal with one main node for each loop.
        for i in range(data.index.stop):

            relations = data.relations.loc[i]
            if not isinstance(relations, str):  # Eliminate `nan`.
                continue
            relations = relations.split("|")

            main_node = data.nodes.loc[i].strip()
            main_node_label = data.labels.loc[i].strip()

            related_nodes = []      # The nodes that related to the main node.
            related_node_labels = []    # The labels of the related nodes.
            # The types of the relationships.
            # `related_nodes` and `relation_types` should have the same length.
            relation_types = []
            for relation in relations:
                relation = relation.strip()
                rel_list = relation.split()
                if len(rel_list) == 2:
                    related_nodes.append(rel_list[0])
                    related_node_labels.append(rel_list[1])
                    relation_types.append("CONTAINS")
                elif len(rel_list) == 3:
                    related_nodes.append(relation.split()[0])
                    related_node_labels.append(rel_list[1])
                    relation_types.append(relation.split()[2])

            # Deal with one related node for each loop.
            for j in range(len(related_nodes)):
                clause = "MATCH (main_node:%s {name:'%s'}), (related_node:%s {name:'%s'}) MERGE (main_node)-[:%s]->(related_node)"\
                    % (main_node_label, main_node, related_node_labels[j],
                       related_nodes[j], relation_types[j])
                print(clause)
                graph.run(clause)
