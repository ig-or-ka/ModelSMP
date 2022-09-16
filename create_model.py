import Classes
from values import *


#---------------------от Васи: сделал модель, как я понял---------------------------------------------


graph_nodes = []
graph_edges = []

print(len(nodes_default))

# добавляю дефолтные узлы портов из своего файла
for i in range(len(nodes_default)):
    coordinate = f"{nodes_default[i][0]}_{nodes_default[i][1]}"
    graph_nodes.append(Classes.node(node_id=i, coordinates=coordinate))
    graph_nodes[-1].create()

def add_node(edge,edge_type):
    incident_nodes = f"{edge[0]+1}_{edge[1]+1}"
    # для длины ребра использую тупа расстояние между двумя точками по пифагору
    # шутка: как вы все знаете, 1 + 1 = 2. разобравшись с этим выражением мы приходим к следующим вычислениям:
    length = ((nodes_default[edge[1]][0] - nodes_default[edge[0]][0])**2 +
              (nodes_default[edge[1]][1] - nodes_default[edge[0]][1])**2)**(1 / 2)
    graph_edges.append(Classes.edges(edge_id=i,
                                     incident_nodes=incident_nodes,
                                     length=length,
                                     edge_type=edge_type))
    graph_edges[-1].create()

for i in range(45):
    add_node(edges_default[i],'sea')
for i in range(45,51):
    add_node(edges_default[i],'train')
add_node(edges_default[51],'pipe')
for i in range(52,55):
    add_node(edges_default[i],'loading')

for i in range(25):
    edge: Classes.edges = Classes.indexes.edges[i+1]

    iceb1 = Classes.icebreaker(port_id=edge.id_begin_node,node_destination_id=edge.id_end_node)
    iceb1.create()

    iceb2 = Classes.icebreaker(port_id=edge.id_end_node,node_destination_id=edge.id_begin_node)
    iceb2.create()

for i in range(1,37):
    for _ in range(20):
        ship1 = Classes.ship(in_port=True,port_id=i,max_capacity=10,cargo_type="oil")
        ship1.create()

        ship2 = Classes.ship(in_port=True,port_id=i,max_capacity=10,cargo_type="cont")
        ship2.create()

        ship3 = Classes.ship(in_port=True,port_id=i,max_capacity=10,cargo_type="weight")
        ship3.create()

cargo1 = Classes.consignment(id_refer=1,node_destination_id=20,cargo_type="oil",size=2)
cargo1.create()

# проверка
print("nodes", len(graph_nodes))
for node in graph_nodes:
    print(node.node_id, node.coordinate_X, node.coordinate_Y)

print("edges")
for edge in graph_edges:
    print(edge.edge_id, edge.length, edge.id_begin_node, edge.id_end_node)





