import py2neo as neo


def get_labels_clause(label_list):
    return ":".join(label_list)


def get_prop_clause(property_dict):
    if property_dict == {}:
        return ""

    prop_clause = ""
    for property_name in property_dict:
        prop_clause +=\
            "%s:'%s'," % (property_name, property_dict[property_name])
    return prop_clause.rstrip(prop_clause[-1])


def get_item_type(item_dict):
    types = item_dict.keys()
    if len(types) != 1:
        return False
    [type] = types
    return type


class List2Neo(object):

    def __init__(self, list, graph_auth, graph_link="http://localhost:7474/"):
        self.graph = neo.Graph(graph_link, auth=graph_auth)
        self.data = list

    def list2nodes(self):
        data = self.data
        graph = self.graph

        # Each graph_item represents a node or a path
        for graph_item in data:
            if not get_item_type(graph_item) == "n":
                continue

            node = graph_item["n"]
            [node_attributes] = node["nodes"]

            labels_clause = get_labels_clause(node_attributes["labels"])
            prop_clause = get_prop_clause(node_attributes["properties"])
            create_node_clause = "MERGE (:%s {%s})"\
                % (labels_clause, prop_clause)

            print(create_node_clause)
            graph.run(create_node_clause)

    def list2relations(self):
        data = self.data
        graph = self.graph

        # Each graph_item represents a node or a pate
        for graph_item in data:
            if not get_item_type(graph_item) == "p":
                continue

            path = graph_item["p"]
            [path_attributes] = path["paths"]

            # Get attributes of the start node and the end node
            sn_prop_clause =\
                get_prop_clause(path_attributes["start_node"]["properties"])
            sn_labels_cluase =\
                get_labels_clause(path_attributes["start_node"]["labels"])
            en_prop_clause =\
                get_prop_clause(path_attributes["end_node"]["properties"])
            en_labels_cluase =\
                get_labels_clause(path_attributes["end_node"]["labels"])

            # Get attributes of the relation to be created
            [relationship_attributes] = path_attributes["relationships"]
            type = relationship_attributes["type"]
            r_prop_clause =\
                get_prop_clause(relationship_attributes["properties"])

            # The clause to create the relation
            create_relation_clause =\
                "MATCH (sn:%s {%s}), (en:%s {%s}) MERGE (sn)-[:%s {%s}]->(en)"\
                % (sn_labels_cluase, sn_prop_clause,
                   en_labels_cluase, en_prop_clause, type, r_prop_clause)

            print(create_relation_clause)
            graph.run(create_relation_clause)
