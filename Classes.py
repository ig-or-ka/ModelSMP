import sqlite3 as sq

#комментарий от Васи: тут короче мы меняем координаты(вчера об этом говорили на созвоне) будем просто в пикселях использовать от 0 до напимер 900 по ширине

class indexes:
    edges = dict()
    ship = dict()
    consignment = dict()
    icebreaker = dict()
    node = dict()

class edges: #edges = ребра
    # incident_nodes: "*id_begin_node*_*id_end_node*"
    # tariff: "*tariff_cont*_*tariff_oil*_*tariff_weight*"
    # edge_types: sea, train, pipe, loading
    def __init__(self, edge_type = "sea", edge_id = None, ice_condition = 0, length = 1, incident_nodes = "0_0", tariff = "0_0_0"):
        self.edge_type = edge_type
        self.edge_id = edge_id
        self.ice_condition = ice_condition
        self.length = length

        segs = incident_nodes.split('_')
        self.id_begin_node = int(segs[0])
        self.id_end_node = int(segs[1])

        segs = tariff.split('_')
        self.tariff_cont = int(segs[0])
        self.tariff_oil = int(segs[1])
        self.tariff_weight = int(segs[2])
        
        if edge_id != None:
            indexes.edges[edge_id] = self
    def create(self):
        #вытаскиваем поля из таблицы с помощью select и increment counter
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"insert into edges (edge_type, ice_condition, length, incident_nodes, tariff) values ('{self.edge_type}','{self.ice_condition}', '{self.length}', '{self.id_begin_node}_{self.id_end_node}', '{self.tariff_cont}_{self.tariff_oil}_{self.tariff_weight}')")
            cur.execute("select count(*) from edges")      
            result = cur.fetchone()
            self.edge_id = result[0]
            indexes.edges[result[0]] = self
    def update(self):
        #обновление поля из таблицы
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE edges
                        SET
                        edge_type = '{self.edge_type}',
                        ice_condition = {self.ice_condition},
                        length = {self.length},
                        incident_nodes = '{self.id_begin_node}_{self.id_end_node}',
                        tariff = '{self.tariff_cont}_{self.tariff_oil}_{self.tariff_weight}'
                        WHERE edge_id = {self.edge_id}
            """)

class ship: #ship = корабль
    def __init__(self, ship_id = None, edge_position = 1, edge_id = -1, port_id = 1, in_port = True, icebreaker_id = 1, max_capacity = 1, node_id = 1, coordinates = 0, cargo_type = "", caravan_condition = False, way = ''):
        self.ship_id = ship_id
        self.edge_position = edge_position
        self.edge_id = edge_id
        self.port_id = port_id
        self.in_port = bool(in_port)
        self.icebreaker_id = icebreaker_id
        self.max_capacity = max_capacity
        self.node_id = node_id
        self.coordinates = coordinates
        self.cargo_type = cargo_type
        self.caravan_condition = bool(caravan_condition)
        if ship_id != None:
            indexes.ship[ship_id] = self

        self.way = [int(seg) for seg in way.split(',') if seg != '']
        self.cargos = []
        self.fill_count = 0
    def create(self):
        #вытаскиваем поля из таблицы с помощью select и increment counter
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            way_str = ''
            if way_str != None:
                way_str = ','.join([str(opl) for opl in self.way])
            cur.execute(f"insert into ship (edge_position, edge_id, port_id, in_port, icebreaker_id, max_capacity, node_id, coordinates, cargo_type, caravan_condition, way) values ('{self.edge_position}', '{self.edge_id}', '{self.port_id}', '{int(self.in_port)}', '{self.icebreaker_id}', '{self.max_capacity}', '{self.node_id}', '{self.coordinates}', '{self.cargo_type}', '{int(self.caravan_condition)}','{way_str}')")
            cur.execute("select count(*) from ship")      
            result = cur.fetchone()
            self.ship_id = result[0]
            indexes.ship[result[0]] = self
    def update(self):
        #обновление поля из таблицы
        with sq.connect("Ships_Icebreakers.db") as con:
            way_str = ''
            if self.way != None:
                way_str = ','.join([str(opl) for opl in self.way])
            cur = con.cursor()
            cur.execute(f"""UPDATE ship
                        SET
                        edge_position = {self.edge_position},
                        edge_id = {self.edge_id},
                        port_id = {self.port_id},
                        in_port = {int(self.in_port)},
                        icebreaker_id = {self.icebreaker_id},
                        max_capacity = {self.max_capacity},
                        node_id = {self.node_id},
                        coordinates = {self.coordinates},
                        cargo_type = '{self.cargo_type}',
                        caravan_condition = {int(self.caravan_condition)},
                        way = '{way_str}'
                        WHERE ship_id = {self.ship_id}
            """)

class consignment: #consignment = партия груза
    # cont - контейнер
    # oil - нефть
    # weight - весовой груз
    def __init__(self, cargo_id = None, cargo_type = "cont", size = 1, node_destination_id = 1, ship_immediately = True, type_refer = 1, id_refer = 1, coordinates = 0, contracted = True, way = 'none'):
        self.cargo_id = cargo_id
        self.cargo_type = cargo_type
        self.size = size
        self.node_destination_id = node_destination_id
        self.ship_immediately = bool(ship_immediately)
        self.type_refer = type_refer
        self.id_refer = id_refer
        self.coordinates = coordinates
        self.contracted = bool(contracted)        
        if cargo_id != None:
            indexes.consignment[cargo_id] = self
        if way == 'none':
            self.way = None
        else:
            self.way = [int(seg) for seg in way.split(',') if seg != '']
    def create(self):
        #вытаскиваем поля из таблицы с помощью select и increment counter
        with sq.connect("Ships_Icebreakers.db") as con:
            way_str = 'none'
            if self.way != None:
                way_str = ','.join([str(opl) for opl in self.way])
            cur = con.cursor()
            cur.execute(f"insert into consignment (cargo_type, size, node_destination_id, ship_immediately, type_refer, id_refer, coordinates, contracted, way) values ('{self.cargo_type}', '{self.size}', '{self.node_destination_id}', '{int(self.ship_immediately)}', '{self.type_refer}', '{self.id_refer}', '{self.coordinates}', '{int(self.contracted)}','{way_str}')")
            cur.execute("select count(*) from consignment")      
            result = cur.fetchone()
            self.cargo_id = result[0]
            indexes.consignment[result[0]] = self
    def update(self):
        #обновление поля из таблицы
        with sq.connect("Ships_Icebreakers.db") as con:
            way_str = 'none'
            if self.way != None:
                way_str = ','.join([str(opl) for opl in self.way])
            cur = con.cursor()
            cur.execute(f"""UPDATE consignment
                        SET
                        cargo_type = '{self.cargo_type}',
                        size = {self.size},
                        node_destination_id = {self.node_destination_id},
                        ship_immediately = {int(self.ship_immediately)},
                        type_refer = {self.type_refer},
                        id_refer = {self.id_refer},
                        coordinates = {self.coordinates},
                        contracted = {int(self.contracted)},
                        way = '{way_str}'
                        WHERE cargo_id = {self.cargo_id}
            """)

class icebreaker: #icebreaker = ледокол
    def __init__(self, icebreaker_id = None, edge_position = 0, prepare_caravan = True, edge_id = 0, port_id = 0, node_destination_id = 1,max_caravan_ships = 5,time_wait_caravan = 3):
        self.icebreaker_id = icebreaker_id
        self.edge_position = edge_position
        self.prepare_caravan = bool(prepare_caravan)
        self.edge_id = edge_id
        self.port_id = port_id
        self.node_destination_id = node_destination_id
        if icebreaker_id != None:
            indexes.icebreaker[icebreaker_id] = self

        self.caravan_ships = []
        self.max_caravan_ships = max_caravan_ships
        self.time_wait_caravan = time_wait_caravan
        self.ticks_wait = 0
    def create(self):
        #вытаскиваем поля из таблицы с помощью select и increment counter
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"insert into icebreaker (edge_position, prepare_caravan, edge_id, port_id, node_destination_id, max_caravan_ships, time_wait_caravan) values ('{self.edge_position}', '{int(self.prepare_caravan)}', '{self.edge_id}', '{self.port_id}', '{self.node_destination_id}', '{self.max_caravan_ships}', '{int(self.time_wait_caravan)}')")
            cur.execute("select count(*) from icebreaker")      
            result = cur.fetchone()
            self.icebreaker_id = result[0]
            indexes.icebreaker[result[0]] = self
    def update(self):
        #обновление поля из таблицы
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE icebreaker
                        SET edge_position = {self.edge_position}, 
                        prepare_caravan = {int(self.prepare_caravan)},
                        edge_id = {self.edge_id},
                        port_id = {self.port_id}, 
                        node_destination_id = {self.node_destination_id}, 
                        max_caravan_ships = {self.max_caravan_ships}, 
                        time_wait_caravan = {int(self.time_wait_caravan)}
                        WHERE icebreaker_id = {self.icebreaker_id}
            """)

class node: #node = узел
    # coordinates: "*X*_*Y*"
    def __init__(self, node_id = None, coordinates = "0_0"):
        segs = coordinates.split("_")
        self.coordinate_X = int(segs[0])
        self.coordinate_Y = int(segs[1])

        self.node_id = node_id
        if node_id != None:
            indexes.node[node_id] = self

        self.edges_list = dict()
        self.allow_ships = {'cont':[],'oil':[],'weight':[],'iceb':[]}
    def create(self):
        #вытаскиваем поля из таблицы с помощью select и increment counter
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"insert into node (coordinates) values ('{self.coordinate_X}_{self.coordinate_Y}')")
            cur.execute("select count(*) from node")      
            result = cur.fetchone()
            self.node_id = result[0]
            indexes.node[result[0]] = self
    def update(self):
        #обновление поля из таблицы
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE node
                SET coordinates = '{self.coordinate_X}_{self.coordinate_Y}'
                WHERE node_id = {self.node_id}""")
def full_info():
    with sq.connect("Ships_Icebreakers.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM edges")
        #print("edges =============")
        result = cur.fetchall()
        for row in result:
            #print(row)
            edges(*row)
        cur.execute("SELECT * FROM ship")
        #print("ship =============")
        result = cur.fetchall()
        for row in result:
            #print(row)
            ship(*row)
        cur.execute("SELECT * FROM consignment")
        #print("consignment =============")
        result = cur.fetchall()
        for row in result:
            #print(row)
            consignment(*row)
        cur.execute("SELECT * FROM icebreaker")
        #print("icebreaker =============")
        result = cur.fetchall()
        for row in result:
            #print(row)
            icebreaker(*row)
        cur.execute("SELECT * FROM node")
        #print("node =============")
        result = cur.fetchall()
        for row in result:
            #print(row)
            node(*row)

def preparing():
    for edge_id in indexes.edges:
        edge: edges = indexes.edges[edge_id]
        node_b: node = indexes.node[edge.id_begin_node]
        node_e: node = indexes.node[edge.id_end_node]

        node_b.edges_list[node_e.node_id] = edge
        node_e.edges_list[node_b.node_id] = edge

    for ship_id in indexes.ship:
        ship_o: ship = indexes.ship[ship_id]
        if ship_o.in_port:
            node_o: node = indexes.node[ship_o.port_id]
            node_o.allow_ships[ship_o.cargo_type].append(ship_o)
        if ship_o.caravan_condition:
            icebr: icebreaker = indexes.icebreaker[ship_o.icebreaker_id]
            icebr.caravan_ships.append(ship_o)
            

    for cargo_id in indexes.consignment:
        cargo: consignment = indexes.consignment[cargo_id]
        if cargo.type_refer == 3:
            ship_o: ship = indexes.ship[cargo.id_refer]
            ship_o.cargos.append(cargo)
            ship_o.fill_count += cargo.size
    
    for iceb_id in indexes.icebreaker:
        iceb: icebreaker = indexes.icebreaker[iceb_id]
        if iceb.prepare_caravan:
            node_b: node = indexes.node[iceb.port_id]
            node_b.allow_ships["iceb"].append(iceb)
            