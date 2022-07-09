import Classes

# это простой алгоритм - заглушка
def req_find(start_node, end_node, used_nodes: list):
    used_nodes.append(start_node)
    node: Classes.node = Classes.indexes.node[start_node]
    if end_node in node.edges_list:
        return [start_node,end_node]
    for incident_node in node.edges_list:
        if incident_node not in used_nodes:
            res = req_find(incident_node,end_node,used_nodes)
            if len(res) > 0:
                res.insert(0,start_node)
                return res
    return []

def alorithm(cargo:Classes.consignment):
    res = req_find(cargo.id_refer,cargo.node_destination_id,[])
    del res[0]
    return res #возвращай список id нод