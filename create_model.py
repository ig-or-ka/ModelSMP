import Classes
from gui.values import *


#---------------------от Васи: сделал модель, как я понял---------------------------------------------


graph_nodes = []
graph_edges = []

print(len(nodes_default))

# добавляю дефолтные узлы портов из своего файла
for i in range(len(nodes_default)):
    coordinate = f"{nodes_default[i][0]}_{nodes_default[i][1]}"
    graph_nodes.append(Classes.node(node_id=i, coordinates=coordinate))

# добавляю дефолтные ребра морских путей из своего файла
for i in range(len(edges_default)):
    incident_nodes = f"{edges_default[i][0]}_{edges_default[i][1]}"
    # для длины ребра использую тупа расстояние между двумя точками по пифагору
    # шутка: как вы все знаете, 1 + 1 = 2. разобравшись с этим выражением мы приходим к следующим вычислениям:
    length = ((nodes_default[edges_default[i][1]][0] - nodes_default[edges_default[i][0]][0])**2 +
              (nodes_default[edges_default[i][1]][1] - nodes_default[edges_default[i][0]][1])**2)**(1 / 2)
    graph_edges.append(Classes.edges(edge_id=i,
                                     incident_nodes=incident_nodes,
                                     length=length))



# проверка
print("nodes", len(graph_nodes))
for node in graph_nodes:
    print(node.node_id, node.coordinate_X, node.coordinate_Y)

print("edges")
for edge in graph_edges:
    print(edge.edge_id, edge.length, edge.id_begin_node, edge.id_end_node)





