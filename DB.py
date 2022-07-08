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
        cur.execute("SELECT * FROM edges")
        cur.execute("SELECT * FROM ship")
        cur.execute("SELECT * FROM consignment")
        cur.execute("SELECT * FROM icebreaker")
        cur.execute("SELECT * FROM node")#вытащить все таблицы
