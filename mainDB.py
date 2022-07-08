import sqlite3 as sq

coordinates = "0.000000, 0.000000"

class indexes:
    edges = dict()
    ship = dict()
    consignment = dict()
    icebreaker = dict()
    node = dict()

class edges: #edges = ребра
    def __init__(self, edge_type = "sea", edge_id = None, ice_condition = 1, length = 1, incident_nodes = "*id_begin_node*_*id_end_node*", max_throughput = 1, tariff = 1500):
        self.edge_type = edge_type
        self.edge_id = edge_id
        self.ice_condition = ice_condition
        self.length = length
        self.incident_nodes = incident_nodes
        self.max_throughput = max_throughput
        self.tariff = tariff
        if edge_id != None:
            indexes.edges[edge_id] = self
    def create(self):
        #вытаскиваем поля из таблицы с помощью select и increment counter
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"insert into edges (edge_type, edge_id, ice_condition, length, incident_nodes, max_throughput, tariff) values ('{edge_type}', '{edge_id}', '{ice_condition}', '{length}', '{incident_nodes}', '{max_throughput}', '{tariff}')")
            cur.execute("""SELECT `AUTO_INCREMENT`
                            FROM  INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_SCHEMA = 'Ships_Icebreakers.db'
                            AND   TABLE_NAME   = 'edges';""")
            result = cur.fetchall()
            self.edge_id = result[0][0]
            indexes.edges[result[0][0]] = self
    def update(self):
        #обновление поля из таблицы
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE edges
            SET edge_id = {self.edge_id}, ice_condition = {self.ice_condition}, length = {self.length}, incident_nodes = {self.incident_nodes}, max_throughput = {self.incident_nodes}, tariff = {self.tariff};
            """)

class ship: #ship = корабль
    def __init__(self, ship_id = None, edge_position = 1, edge_id = -1, port_id = 1, in_port = True, icebreaker_id = 1, max_capacity = 1, node_id = 1, cargo_type = "", caravan_condition = True):
        self.ship_id = ship_id
        self.edge_position = edge_position
        self.edge_id = edge_id
        self.port_id = port_id
        self.in_port = in_port
        self.icebreaker_id = icebreaker_id
        self.max_capacity = max_capacity
        self.node_id = node_id
        self.coordinates = coordinates
        self.cargo_type = cargo_type
        self.caravan_condition = caravan_condition
        if ship_id != None:
            indexes.ship[ship_id] = self
    def create(self):
        #вытаскиваем поля из таблицы с помощью select и increment counter
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"insert into ship (ship_id, edge_position, edge_id, port_id, in_port, icebreaker_id, max_capacity, node_id, coordinates, cargo_type, caravan_condition) values ('{ship_id}', '{edge_position}', '{edge_id}', '{port_id}', '{in_port}', '{icebreaker_id}', '{max_capacity}, '{node_id}', '{coordinates}', '{cargo_type}', '{caravan_condition}')")
            cur.execute("""SELECT `AUTO_INCREMENT`
                            FROM  INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_SCHEMA = 'Ships_Icebreakers.db'
                            AND   TABLE_NAME   = 'ship';""")
            indexes.ship[ship_id] = self
    def update(self):
        #обновление поля из таблицы
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE ship
            SET ship_id = {self.ship_id}, edge_position = {self.edge_position}, edge_id = {self.edge_id}, port_id = {self.port_id}, in_port = {self.in_port}, icebreaker_id = {self.icebreaker_id}, max_capacity = {self.max_capacity}, node_id = {self.node_id}, coordinates = {self.coordinates}, cargo_type = {self.cargo_type}, caravan_condition = {self.caravan_condition}
            """)

class consignment: #consignment = партия груза
    def __init__(self, cargo_id = None, size = 1, node_destination_id = 1, ship_immediately = True, type_refer = 1, id_refer = 1, contracted = True):
        self.cargo_id = cargo_id
        self.size = size
        self.node_destination_id = node_destination_id
        self.ship_immediately = ship_immediately
        self.type_refer = type_refer
        self.id_refer = id_refer
        self.coordinates = coordinates
        self.contracted = contracted
        if cargo_id != None:
            indexes.consignment[cargo_id] = self
    def create(self):
        #вытаскиваем поля из таблицы с помощью select и increment counter
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"insert into consignment (cargo_id, size, node_destination_id, ship_immediately, type_refer, id_refer, coordinates, contracted) values ('{cargo_id}', '{size}', '{node_destination_id}', '{ship_immediately}', '{type_refer}', '{id_refer}', '{coordinates}', '{contracted}')")
            cur.execute("""SELECT `AUTO_INCREMENT`
                            FROM  INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_SCHEMA = 'Ships_Icebreakers.db'
                            AND   TABLE_NAME   = 'consignment';""")
            indexes.consignment[cargo_id] = self
    def update(self):
        #обновление поля из таблицы
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE consignment
            SET cargo_id = {self.cargo_id}, size = {self.size}, node_destination_id = {self.node_destination_id}, ship_immediately = {self.ship_immediately}, type_refer = {type_refer}, id_refer = {self.id_refer}, coordinates = {self.coordinates}, contracted = {self.contracted}
            """)

class icebreaker: #icebreaker = ледокол
    def __init__(self, icebreaker_id = None, edge_position = 0, prepare_caravan = True, edge_id = 0, port_id = 0, node_destination_id = 1, speed = 40,shipsin_caravan = True):
        self.icebreaker_id = icebreaker_id
        self.edge_position = edge_position
        self.prepare_caravan = prepare_caravan
        self.edge_id = edge_id
        self.port_id = port_id
        self.node_destination_id = node_destination_id
        self.speed = speed
        self.shipsin_caravan = shipsin_caravan
        if icebreaker_id != None:
            indexes.icebreaker[icebreaker_id] = self
    def create(self):
        #вытаскиваем поля из таблицы с помощью select и increment counter
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"insert into icebreaker (icebreaker_id, edge_position, prepare_caravan, edge_id, port_id, node_destination_id, speed, shipsin_caravan) values ('{icebreaker_id}', '{edge_position}', '{prepare_caravan}', '{edge_id}', '{node_destination_id}', '{speed}', '{shipsin_caravan}')")
            cur.execute("""SELECT `AUTO_INCREMENT`
                            FROM  INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_SCHEMA = 'Ships_Icebreakers.db'
                            AND   TABLE_NAME   = 'icebreaker';""")
            indexes.icebreaker[icebreaker_id] = self
    def update(self):
        #обновление поля из таблицы
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE icebreaker
            SET icebreaker_id = {self.icebreaker_id}, edge_position = {self.edge_position}, prepare_caravan = {self.prepare_caravan}, edge_id = {self.edge_id}, port_id = {self.port_id}, node_destination_id = {self.node_destination_id}, speed = {self.speed}, shipsin_caravan = {self.shipsin_caravan}
            """)

class node: #node = узел
    def __init__(self, node_id = None):
        self.coordinates = coordinates
        self.node_id = node_id
        if node_id != None:
            indexes.node[node_id] = self
    def create(self):
        #вытаскиваем поля из таблицы с помощью select и increment counter
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"insert into node (coordinates, node_id) values ('{coordinates}', '{node_id}')")
            cur.execute("""SELECT `AUTO_INCREMENT`
                            FROM  INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_SCHEMA = 'Ships_Icebreakers.db'
                            AND   TABLE_NAME   = 'node';""")
            indexes.node[node_id] = self
    def update(self):
        #обновление поля из таблицы
        with sq.connect("Ships_Icebreakers.db") as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE node
            SET coordinates = {self.coordinates}, node_id = {self.node_id}, """)

import sqlite3 as sq

with sq.connect("Ships_Icebreakers.db") as con:
    cur = con.cursor()

    # добавь столбцы
    # id ребра (INT PRIMARY KEY autoincrement)
    # ледовая обстановка, 0 если не СМП (INT)
    cur.execute("DROP TABLE IF EXISTS edges")
    cur.execute("""CREATE TABLE IF NOT EXISTS edges(
        edge_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ice_condition INTEGER DEFAULT 0,
        edge_type TEXT,
        length INTEGER,
        incident_nodes TEXT,
        max_throughput INTEGER,
        tariff TEXT
    )""")

    # добавь столбцы
    # id корабля (INT PRIMARY KEY autoincrement)
    # положение на ребре (INT)
    # id ребра, если плыпет, id порта, если стоит (INT)
    # в порту или нет (BOOLEAN)
    # id ледокола, если находится в караване (INT)
    # максимальная вместимость (INT)
    # id узела назначения (INT)
    cur.execute("DROP TABLE IF EXISTS ship")
    cur.execute("""CREATE TABLE IF NOT EXISTS ship(
    ship_id INTEGER PRIMARY KEY AUTOINCREMENT,
    edge_position INTEGER,
    edge_id INTEGER,
    port_id INTEGER,
    in_port BOOLEAN,
    icebreaker_id INTEGER,
    max_capacity INTEGER,
    node_id INTEGER,
    coordinates INTEGER NOT NULL DEFAULT "0.000000, 0.000000",
    cargo_type TEXT,
    caravan_condition BOOLEAN
    )""")

    # добавь столбцы
    # id груза (INT PRIMARY KEY autoincrement)
    # объем (INT),
    # узле назвачения (INT id узла, куда необходимо доставить груз),
    # хочет ли груз отправиться немедленно (BOOLEAN),
    # тип принадлежности (INT 1 - узел, 2 - ребро, 3 - кораблю)
    # id принадлежности (INT id корабля, ребра или узла)
    # coordinates INTEGER, 0 если привязан к кораблю
    cur.execute("DROP TABLE IF EXISTS consignment")
    cur.execute("""CREATE TABLE IF NOT EXISTS consignment(
    cargo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    size INTEGER,
    node_destination_id INTEGER,
    ship_immediately BOOLEAN,
    type_refer INTEGER,
    id_refer INTEGER,
    coordinates INTEGER,
    contracted BOOLEAN
    )""")

    # добавь столбцы
    # id ледокола (INT PRIMARY KEY autoincrement)
    # положение на ребре (INT)
    # собирает караван (BOOLEAN)
    # id ребра, если плыпет, id порта, если стоит (INT)
    # id узела назначения (INT)
    cur.execute("DROP TABLE IF EXISTS icebreaker")
    cur.execute("""CREATE TABLE IF NOT EXISTS icebreaker(
    icebreaker_id INTEGER PRIMARY KEY AUTOINCREMENT,
    edge_position INTEGER,
    prepare_caravan BOOLEAN,
    edge_id INTEGER,
    port_id INTEGER,
    node_destination_id INTEGER,
    speed INTEGER,
    shipsin_caravan BOOLEAN
    )""")

    # добавь столбцы
    # добавь PRIMARY KEY autoincrement id каждого узла
    cur.execute("DROP TABLE IF EXISTS node")
    cur.execute("""CREATE TABLE IF NOT EXISTS node(
    node_id INTEGER PRIMARY KEY AUTOINCREMENT,
    coordinates TEXT
    )""")
    def full_info():
        cur.execute(SELECT * FROM edges)
        cur.execute(SELECT * FROM ship)
        cur.execute(SELECT * FROM consignment)
        cur.execute(SELECT * FROM icebreaker)
        cur.execute(SELECT * FROM node)#вытащить все таблицы
