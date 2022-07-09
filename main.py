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
                if cargo.contracted:
                    print(f'Груз {cargo_id} доставлен!')
                    cargo.contracted = False
                    #TODO do remove
                continue

            this_node: Classes.node = Classes.indexes.node[cargo.id_refer]
            next_node_id = cargo.way[0]
            del cargo.way[0]
            
            next_edge: Classes.edges = this_node.edges_list[next_node_id]
            
            if next_edge.edge_type == "sea":
                ships = this_node.allow_ships[cargo.cargo_type]
                for ship in ships:
                    if ship.fill_count + cargo.size > ship.max_capacity:
                        continue
                    cargo_full_way = [next_node_id]
                    cargo_full_way.extend(cargo.way)
                    count_on_sea = 1
                    for i in range(len(cargo_full_way)-1):
                        node_op: Classes.node = Classes.indexes.node[cargo_full_way[i]]
                        edge_op: Classes.edges = node_op.edges_list[cargo_full_way[i+1]]
                        if edge_op.edge_type != "sea":
                            break
                        count_on_sea+=1

                    next_ship = False
                    i = 0
                    while i < count_on_sea:
                        if i == len(ship.way):
                            break
                        if ship.way[i] != cargo_full_way[i]:
                            next_ship = True
                            break
                        i+=1
                    if next_ship:
                        continue

                    if count_on_sea > len(ship.way):
                        i = len(ship.way)
                        while i < count_on_sea:
                            ship.way.append(cargo_full_way[i])
                            i+=1

                    ship.fill_count += cargo.size
                    ship.cargos.append(cargo)
                    cargo.type_refer = 3
                    cargo.id_refer = ship.ship_id
                    #cargo.update()
                    break
                else:
                    cargo.way.insert(0,next_node_id)
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
            #cargo.update()
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
            #cargo.update()
        #если груз на корабле, то на данном шаге ничего не делаем


def ships_move():
    for ship_id in Classes.indexes.ship:
        ship:Classes.ship = Classes.indexes.ship[ship_id]
        if ship.in_port:
            if ship.fill_count > 0:
                this_node: Classes.node = Classes.indexes.node[ship.port_id]
                next_node_id = ship.way[0]
                del ship.way[0]

                next_edge: Classes.edges = this_node.edges_list[next_node_id]

                this_node.allow_ships[ship.cargo_type].remove(ship)
                ship.in_port = False
                ship.edge_id = next_edge.edge_id
                if this_node.node_id == next_edge.id_begin_node:
                    ship.coordinates = 1
                else:
                    ship.coordinates = -1
                print(f"Корабль {ship_id} отчалил к узлу {next_node_id}")
        else:
            this_edge: Classes.edges = Classes.indexes.edges[ship.edge_id]
            vec = ship.coordinates // abs(ship.coordinates)
            ship.coordinates += 100 / this_edge.length * vec
            print(f'Корабль {ship_id} на ребре {this_edge.edge_id} {ship.coordinates}')
            if abs(ship.coordinates) >= 100:                
                if ship.coordinates > 0:
                    this_node_id = this_edge.id_end_node
                else:
                    this_node_id = this_edge.id_begin_node
                this_node = Classes.indexes.node[this_node_id]

                print(f"Корабль {ship_id} причалил к узлу {this_node_id}")

                ship.in_port = True
                ship.port_id = this_node_id
                this_node.allow_ships[ship.cargo_type].append(ship)

                for cargo in list(ship.cargos):
                    out_cargo = len(cargo.way) == 0
                    if not out_cargo:
                        next_edge: Classes.edges = this_node.edges_list[cargo.way[0]]
                        out_cargo = next_edge.edge_type != "sea"
                    if out_cargo:
                        ship.cargos.remove(cargo)
                        ship.fill_count -= cargo.size
                        cargo.type_refer = 1
                        cargo.id_refer = this_node_id
                        print(f"Груз {cargo.cargo_id} доставлен на узел {this_node_id}")
                    else:
                        del cargo.way[0]
time_tick = 1

while True:
    cargos_move()
    ships_move()
    sleep(time_tick)