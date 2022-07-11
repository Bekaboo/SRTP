#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import py2neo as pn
import os.path as path
import re

# This class is used to build a link between our datafile and the remote graph,
# subsequently create the nodes and relationships from the datafile.


class File2Neo(object):
    def __init__(self, filepath, graph_link="http://localhost:7474/",
                 graph_auth=("neo4j", "neo4j")):

        # Link to the remote graph.
        graph = pn.Graph(graph_link, auth=graph_auth)
        self.graph = graph
        self.filepath = filepath
        datapath_split = path.splitext(filepath)
        if datapath_split[1] == ".xlsx" or datapath_split[1] == ".xls":
            self.data = pd.read_excel(filepath)
        elif datapath_split[1] == ".csv":
            self.data = pd.read_csv(filepath)

    def _parse_node_labels(self, idx):
        return str(self.data.node_labels.loc[idx]).strip().replace(";", ":")

    def _parse_node_props(self, idx):
        return str(self.data.node_props.loc[idx]).strip().replace(";", ",")

    def _parse_relations(self, idx):
        if pd.isna(self.data.relations.loc[idx]):
            return
        relations = [re.split("->", _)
                     for _ in self.data.relations.loc[idx].strip().split("|")]
        relation_types = [_[0].split(";") for _ in relations]
        related_to = [_[1].split("@") for _ in relations]
        related_to = [[_[0].replace(";", ","), _[1].replace(";", ":")]
                      for _ in related_to]
        return {"types": relation_types, "to": related_to}

    def file2nodes(self):   # To create a graph, first create all the nodes.
        data = self.data
        graph = self.graph

        for i in range(data.index.stop):
            if not isinstance(data.node_props.loc[i], str):  # Eliminate `nan`.
                continue
            clause = "MERGE (:%s {%s})"\
                % (self._parse_node_labels(i),
                   self._parse_node_props(i))
            #print(clause)
            clause = clause.replace("'nan'", "NULL")
            graph.run(clause)

    def file2relations(self):
        data = self.data
        graph = self.graph

        # Deal with one main node for each loop.
        for i in range(data.index.stop):
            relations = self._parse_relations(i)
            if not relations:  # Continue if no relations are attached
                continue
            for relation in zip(relations.get("types"), relations.get("to")):
                for relation_type in relation[0]:
                    related_to_node_props = relation[1][0]
                    if len(relation[1]) >= 1:
                        related_to_node_labels = relation[1][1]
                    clause = "MATCH (main_node:%s {%s}) "\
                             "WITH main_node MATCH (related_to:%s {%s}) "\
                             "MERGE (main_node)-[:%s]->(related_to)"\
                        % (self._parse_node_labels(i),
                           self._parse_node_props(i),
                           related_to_node_labels,
                           related_to_node_props,
                           relation_type)
                    #print(clause)
                    graph.run(clause)
