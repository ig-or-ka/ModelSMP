import Classes
from alg import alorithm
from time import sleep
from LaunchScreen import GUI

Classes.full_info()
Classes.preparing()
GUI.start()
GUI.selected_cargo = Classes.indexes.consignment[3]

def add_ship_cargo_edge(ship:Classes.ship, edge:Classes.edges):
    edge.count_cargo += len(ship.cargos)
    for cargo in ship.cargos:
        edge.weight_cargo += cargo.size
    print(f"Загрузка ребра {edge.edge_id}: {edge.count_cargo} {edge.weight_cargo}")

def remove_ship_cargo_edge(ship:Classes.ship, edge:Classes.edges):
    edge.count_cargo -= len(ship.cargos)
    for cargo in ship.cargos:
        edge.weight_cargo -= cargo.size
    print(f"Загрузка ребра {edge.edge_id}: {edge.count_cargo} {edge.weight_cargo}")

def is_wait_icebreaker(start_node:Classes.node, edge:Classes.edges):
    if edge.id_begin_node == start_node.node_id:
        end_node_id = edge.id_end_node
    else:
        end_node_id = edge.id_begin_node
    for iceb in start_node.allow_ships['iceb']:
        if iceb.node_destination_id == end_node_id:
            return True
    for iceb in edge.icebreakers:
        if iceb.node_destination_id == start_node.node_id and iceb.edge_position >= 80:
            return True
    return False

def cargos_move():
    for cargo_id in Classes.indexes.consignment:
        cargo: Classes.consignment = Classes.indexes.consignment[cargo_id]
        if cargo.way == None:
            cargo.way = alorithm(cargo,False)
            print(cargo.way)
        if cargo.type_refer == 1: # груз на узле
            
            if cargo.id_refer == cargo.node_destination_id:
                if cargo.contracted:
                    print(f'Груз {cargo_id} доставлен!')
                    cargo.contracted = False
                    cargo.update()
                    #TODO do remove
                continue

            this_node: Classes.node = Classes.indexes.node[cargo.id_refer]
            next_node_id = cargo.way[0]
            del cargo.way[0]
            
            next_edge: Classes.edges = this_node.edges_list[next_node_id]
            
            if next_edge.edge_type == "sea":
                if next_edge.ice_condition > 0\
                    and cargo.ship_immediately\
                    and not is_wait_icebreaker(this_node,next_edge):

                    way = alorithm(cargo,True)
                    if len(way) > 0:
                        cargo.way = way
                        print(f"Груз {cargo.cargo_id} не будет ждать ледокол",cargo.way)
                        cargo.update()
                        continue

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
                    ship.update()
                    cargo.type_refer = 3
                    cargo.id_refer = ship.ship_id
                    break
                else:
                    cargo.way.insert(0,next_node_id)
            else:
                if next_edge.edge_type == "pipe" and cargo.cargo_type != "oil":
                    print("error wrong way edge type")
                    continue
                
                # edit cargo on edge count
                next_edge.count_cargo += 1
                next_edge.weight_cargo += cargo.size
                print(f"Загрузка ребра {next_edge.edge_id}: {next_edge.count_cargo} {next_edge.weight_cargo}")

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
                # edit cargo on edge count
                this_edge.count_cargo -= 1
                this_edge.weight_cargo -= cargo.size
                print(f"Загрузка ребра {this_edge.edge_id}: {this_edge.count_cargo} {this_edge.weight_cargo}")
                cargo.type_refer = 1
                if cargo.coordinates > 0:
                    cargo.id_refer = this_edge.id_end_node
                else:
                    cargo.id_refer = this_edge.id_begin_node
                print(f'Груз {cargo_id} прибыл на узел {cargo.id_refer}')
            cargo.update()
        #если груз на корабле, то на данном шаге ничего не делаем

def unloading_ship(ship: Classes.ship, this_node: Classes.node):
    print(f"Корабль {ship.ship_id} причалил к узлу {this_node.node_id}")

    ship.in_port = True
    ship.port_id = this_node.node_id
    this_node.allow_ships[ship.cargo_type].append(ship)

    for cargo in list(ship.cargos):
        out_cargo = len(cargo.way) == 0
        if not out_cargo:
            next_edge: Classes.edges = this_node.edges_list[cargo.way[0]]
            out_cargo = next_edge.edge_type != "sea"
            if not out_cargo\
                    and cargo.ship_immediately\
                    and next_edge.ice_condition > 0\
                    and not is_wait_icebreaker(this_node,next_edge):
                temp_id_refer = cargo.id_refer
                cargo.id_refer = this_node.node_id
                way = alorithm(cargo,True)
                cargo.id_refer = temp_id_refer
                if len(way) > 0:
                    cargo.way = way
                    print(f"Груз {cargo.cargo_id} не будет ждать ледокол",cargo.way)
                    out_cargo = True
        if out_cargo:
            ship.cargos.remove(cargo)
            ship.fill_count -= cargo.size
            cargo.type_refer = 1
            cargo.id_refer = this_node.node_id            
            print(f"Груз {cargo.cargo_id} доставлен на узел {this_node.node_id}")
        else:
            del cargo.way[0]
        cargo.update()
    ship.update()

def ships_move():
    for ship_id in Classes.indexes.ship:
        ship:Classes.ship = Classes.indexes.ship[ship_id]
        if ship.caravan_condition:
            continue
        if ship.in_port:
            if ship.fill_count > 0:
                this_node: Classes.node = Classes.indexes.node[ship.port_id]
                next_node_id = ship.way[0]
                del ship.way[0]

                next_edge: Classes.edges = this_node.edges_list[next_node_id]

                if next_edge.ice_condition == 1:
                    # прикрепляем к каравану
                    for iceb in this_node.allow_ships["iceb"]:
                        if iceb.node_destination_id == next_node_id and iceb.max_caravan_ships >= len(iceb.caravan_ships) + 1:
                            iceb.caravan_ships.append(ship)
                            ship.caravan_condition = True
                            ship.icebreaker_id = iceb.icebreaker_id
                            print(f"Корабль {ship_id} привязан к ледоколу {iceb.icebreaker_id}")
                            break
                    else:
                        ship.way.insert(0,next_node_id)
                else:
                    # edit cargo on edge count
                    add_ship_cargo_edge(ship,next_edge)
                    this_node.allow_ships[ship.cargo_type].remove(ship)
                    ship.in_port = False
                    ship.edge_id = next_edge.edge_id
                    if this_node.node_id == next_edge.id_begin_node:
                        ship.coordinates = 1
                    else:
                        ship.coordinates = -1
                    print(f"Корабль {ship_id} отчалил к узлу {next_node_id}")
                ship.update()
        else:
            this_edge: Classes.edges = Classes.indexes.edges[ship.edge_id]
            vec = ship.coordinates // abs(ship.coordinates)
            ship.coordinates += 100 / this_edge.length * vec
            print(f'Корабль {ship_id} на ребре {this_edge.edge_id} {ship.coordinates}')
            ship.update()
            if abs(ship.coordinates) >= 100:
                # edit cargo on edge count
                remove_ship_cargo_edge(ship,this_edge)
                if ship.coordinates > 0:
                    this_node_id = this_edge.id_end_node
                else:
                    this_node_id = this_edge.id_begin_node
                this_node = Classes.indexes.node[this_node_id]
                unloading_ship(ship,this_node)

    for iceb_id in Classes.indexes.icebreaker:
        iceb: Classes.icebreaker = Classes.indexes.icebreaker[iceb_id]
        if iceb.prepare_caravan:
            if len(iceb.caravan_ships) != 0:
                iceb.ticks_wait += 1
                print(f'Ледокол {iceb.icebreaker_id} собирает караван {iceb.ticks_wait} из {iceb.time_wait_caravan}')
                if iceb.ticks_wait == iceb.time_wait_caravan or len(iceb.caravan_ships) == iceb.max_caravan_ships:
                    print(f'Ледокол {iceb.icebreaker_id} отчалил в порт {iceb.node_destination_id}')
                    this_node: Classes.node = Classes.indexes.node[iceb.port_id]
                    next_edge: Classes.edges = this_node.edges_list[iceb.node_destination_id]

                    iceb.prepare_caravan = False
                    iceb.edge_position = 0
                    iceb.edge_id = next_edge.edge_id
                    this_node.allow_ships["iceb"].remove(iceb)
                    
                    for ship in iceb.caravan_ships:
                        # edit cargo on edge count
                        add_ship_cargo_edge(ship,next_edge)
                        this_node.allow_ships[ship.cargo_type].remove(ship)
                        ship.in_port = False
                        ship.update()
                    iceb.update()
        else:
            this_edge: Classes.edges = Classes.indexes.edges[iceb.edge_id]
            iceb.edge_position += 100 / this_edge.length
            print(f'Ледокол {iceb.icebreaker_id} на ребре {this_edge.edge_id} {iceb.edge_position}')
            iceb.update()
            if abs(iceb.edge_position) >= 100: 
                # ледокол прибыл в порт
                print(f'Ледокол {iceb.icebreaker_id} прибыл в порт {iceb.node_destination_id}')
                
                iceb.prepare_caravan = True
                iceb.port_id = iceb.node_destination_id
                this_node: Classes.node = Classes.indexes.node[iceb.port_id]
                if this_edge.id_begin_node == iceb.node_destination_id:
                    iceb.node_destination_id = this_edge.id_end_node
                else:
                    iceb.node_destination_id = this_edge.id_begin_node
                iceb.ticks_wait = 0
                this_node.allow_ships["iceb"].append(iceb)

                # разгрузка кораблей
                for ship in iceb.caravan_ships:
                    # edit cargo on edge count
                    remove_ship_cargo_edge(ship,this_edge)
                    ship.caravan_condition = False
                    unloading_ship(ship,this_node)
                iceb.caravan_ships = []
                iceb.update()

time_tick = 1

while GUI.work:
    cargos_move()
    ships_move()
    if GUI.selected_cargo != None and GUI.app != None:
        if GUI.selected_cargo.contracted:
            if GUI.selected_cargo.type_refer == 2:
                if GUI.selected_cargo.coordinates >= 0:
                    coord = GUI.selected_cargo.coordinates
                else:
                    coord = 100 + GUI.selected_cargo.coordinates
                edge = Classes.indexes.edges[GUI.selected_cargo.id_refer]
                GUI.app.draw_goods(edge,coord)
            elif GUI.selected_cargo.type_refer == 3:
                ship: Classes.ship = Classes.indexes.ship[GUI.selected_cargo.id_refer]
                if not ship.in_port:
                    if ship.caravan_condition:
                        iceb: Classes.icebreaker = Classes.indexes.icebreaker[ship.icebreaker_id]
                        edge: Classes.edges = Classes.indexes.edges[iceb.edge_id]
                        if edge.id_end_node == iceb.node_destination_id:
                            coord = iceb.edge_position
                        else:
                            coord = 100 - iceb.edge_position
                    else:
                        if ship.coordinates >= 0:
                            coord = ship.coordinates
                        else:
                            coord = 100 + ship.coordinates
                        edge = Classes.indexes.edges[ship.edge_id]
                    GUI.app.draw_goods(edge,coord)
        else:
            GUI.app.remove_goods()
    sleep(time_tick)