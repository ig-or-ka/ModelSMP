import Classes

# это простой алгоритм - заглушка
def req_find(start_node, end_node, used_nodes: list,without_smp):
    used_nodes.append(start_node)
    node: Classes.node = Classes.indexes.node[start_node]
    if end_node in node.edges_list:
        if not without_smp or node.edges_list[end_node].ice_condition == 0:
            return [start_node,end_node]
    for incident_node in node.edges_list:
        if incident_node not in used_nodes:
            if not without_smp or node.edges_list[incident_node].ice_condition == 0:
                res = req_find(incident_node,end_node,used_nodes,without_smp)
                if len(res) > 0:
                    res.insert(0,start_node)
                    return res
    return []

def alorithm(cargo:Classes.consignment, without_smp):
    res = req_find(cargo.id_refer,cargo.node_destination_id,[],without_smp)
    if len(res) > 0:
        del res[0]
    return res #возвращай список id нод