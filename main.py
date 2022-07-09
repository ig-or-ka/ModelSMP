import Classes
from alg import alorithm
from time import sleep

Classes.full_info()
Classes.preparing()

def cargos_move():
    for cargo_id in Classes.indexes.consignment:
        cargo: Classes.consignment = Classes.indexes.consignment[cargo_id]
        if cargo.way == None:
            cargo.way = alorithm(cargo)
            print(cargo.way)
        if cargo.type_refer == 1: # груз на узле
            
            if cargo.id_refer == cargo.node_destination_id:
                print(f'Груз {cargo_id} доставлен!')
                #TODO do remove
                continue

            this_node: Classes.node = Classes.indexes.node[cargo.id_refer]
            next_node_id = cargo.way[0]
            del cargo.way[0]
            
            next_edge: Classes.edges = this_node.edges_list[next_node_id]
            
            if next_edge.edge_type == "sea":
                # тут бедет загрузка корабля
                pass
            else:
                if next_edge.edge_type == "pipe" and cargo.cargo_type != "oil":
                    print("error wrong way edge type")
                    continue

                cargo.type_refer = 2
                cargo.id_refer = next_edge.edge_id
                if this_node.node_id == next_edge.id_begin_node:
                    cargo.coordinates = 1
                else:
                    cargo.coordinates = -1
            cargo.update()
        elif cargo.type_refer == 2: # груз на ребре
            this_edge: Classes.edges = Classes.indexes.edges[cargo.id_refer]
            vec = cargo.coordinates // abs(cargo.coordinates)
            cargo.coordinates += 100 / this_edge.length * vec
            print(f'Груз {cargo_id} на ребре {this_edge.edge_id} {cargo.coordinates}')
            if abs(cargo.coordinates) >= 100:
                #груз прибыл на узел назначения                
                cargo.type_refer = 1
                if cargo.coordinates > 0:
                    cargo.id_refer = this_edge.id_end_node
                else:
                    cargo.id_refer = this_edge.id_begin_node
                print(f'Груз {cargo_id} прибыл на узел {cargo.id_refer}')
            cargo.update()
        #если груз на корабле, то на данном шаге ничего не делаем


def ships_move():
    pass

time_tick = 1

while True:
    cargos_move()
    ships_move()
    sleep(time_tick)