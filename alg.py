import Classes
from gui.values import edges_default, nodes_default
from collections import deque

# это простой алгоритм - заглушка
# def req_find(start_node, end_node, used_nodes: list):
#     used_nodes.append(start_node)
#     node: Classes.node = Classes.indexes.node[start_node]
#     if end_node in node.edges_list:
#         return [start_node,end_node]
#     for incident_node in node.edges_list:
#         if incident_node not in used_nodes:
#             res = req_find(incident_node,end_node,used_nodes)
#             if len(res) > 0:
#                 res.insert(0,start_node)
#                 return res
#     return []




def alorithm(cargo: Classes.consignment):
    res = req_find(cargo.id_refer, cargo.node_destination_id, cargo)
    del res[0]
    return res  #  возвращай список id нод






# ну штош, щас будем реально кодить big cringe

def req_find(start_node, end_node, cargo):
    graph = generate_graph(cargo.cargo_type == "oil")

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

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.id)
                current = current.parent
            return path[::-1]  # Return reversed path


        children = [Node(i) for i in current_node.neighbours]

        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + get_dist(child.id, current_node)
            child.h = get_h(current_node.id, child.id, cargo)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


# тут собираем инфу о графе из инфы о ребрах специально для алгоритма и если груз это oil то еще добавляем в граф трубопровод
def generate_graph(is_oil):
    graph = {i: Node(id=i) for i in range(len(nodes_default))}

    for edge in edges_default:
        a, b = edge[0], edge[1]
        graph[a].neighbours.append(b)
        graph[b].neighbours.append(a)

    if not is_oil:
        graph.pop(43)
        graph.pop(44)

    return graph


def get_dist(a_id, b_id):
    node_a = nodes_default[a_id]
    node_b = nodes_default[b_id]

    return ((node_b[0] - node_a[0]) ** 2 + (node_b[1] - node_a[1]) ** 2) ** 0.5

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

    # def __eq__(self, other):
    #     return self.position == other.position


gr = generate_graph(False)
for i in range(len(gr)):
    print(gr[i].neighbours)

