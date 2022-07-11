import Classes

# это простой алгоритм - заглушка
"""
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
"""




def alorithm(cargo: Classes.consignment, without_smp):
    #res = req_find(cargo.id_refer,cargo.node_destination_id,[],without_smp)
    res = req_find(cargo.id_refer, cargo.node_destination_id, cargo, without_smp)
    if res == None:
        return []
    else:
        del res[0]
    return res  #  возвращай список id нод

def req_find(start_node, end_node, cargo, without_smp):
    graph = generate_graph(cargo.cargo_type == "oil", without_smp)
    """
    print("from ", start_node, "to ", end_node)    
    for i in graph:
        print(i,graph[i].neighbours)
    """

    open_list = [graph[start_node]]
    closed_list = []

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0

        for i, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = i

        open_list.pop(current_index)
        closed_list.append(current_node)

        #print("-------current node id", current_node.id)
        if current_node.id == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.id)
                current = current.parent
            return path[::-1]  # Return reversed path


        children = [graph[i] for i in current_node.neighbours]

        for child in children:

            child_is_dead = False

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    child_is_dead = True
                    break

            if child_is_dead:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + get_dist(child.id, current_node.id)
            child.h = get_h(current_node.id, child.id, cargo)
            child.f = child.g + child.h
            child.parent = current_node

            #print("child id ", child.id, "parent id ", current_node.id)

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


# тут собираем инфу о графе из инфы о ребрах специально для алгоритма и если груз это oil то еще добавляем в граф трубопровод
def generate_graph(is_oil, without_smp):
    graph = {id: Node(id=id) for id in Classes.indexes.node}

    for edge_id in Classes.indexes.edges:
        edge: Classes.edges = Classes.indexes.edges[edge_id]
        if (is_oil or edge.count_cargo != "oil")\
            and (not without_smp or edge.ice_condition == 0):
            graph[edge.id_begin_node].neighbours.append(edge.id_end_node)
            graph[edge.id_end_node].neighbours.append(edge.id_begin_node)
    return graph


def get_dist(a_id, b_id):
    node_a: Classes.node = Classes.indexes.node[a_id]
    edge: Classes.edges = node_a.edges_list[b_id]
    return edge.length

def get_h(a_id, b_id, cargo):
    node_a = Classes.indexes.node[a_id]
    current_edge = node_a.edges_list[b_id]

    # Если ребро loading, то его тариф = 0
    if current_edge.edge_type == "loading":
        return 0

    tarifes = {
        "cont": current_edge.tariff_cont,
        "oil": current_edge.tariff_oil,
        "weight": current_edge.tariff_weight
    }

    return tarifes[cargo.cargo_type] * cargo.size

class Node:

    def __init__(self, id, parent=None, neighbours=None):
        if neighbours is None:
            neighbours = []

        self.parent = parent
        # self.position = position

        self.id = id

        self.neighbours = neighbours

        self.g = 0
        self.h = 0
        self.f = 0
        
# для теста
if __name__ == '__main__':
    Classes.full_info()
    Classes.preparing()
    """
    gr = generate_graph(False,False)
    for i in gr:
        print(i,gr[i].neighbours)
    """

    cargo = Classes.indexes.consignment[1]
    res = req_find(cargo.id_refer, cargo.node_destination_id, cargo, False)
    print("res", res)