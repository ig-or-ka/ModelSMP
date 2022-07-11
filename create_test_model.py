import Classes
"""
nodes = [
	(213, 301),
	(282, 232),
	(447, 193),
	(628, 199),
	(564, 416),
	(481, 395),
	(366, 375),
	(258, 320),
	(207, 421),
	(396, 538),
	(464, 239),
	(552, 255)
]

edges = [
	(1,2,"sea",1,"0_0_0"),
	(2,3,"sea",1,"0_0_0"),
	(3,4,"sea",1,"0_0_0"),
	(4,5,"sea",0,"0_0_0"),
	(5,6,"train",0,"0_0_0"),
	(6,7,"train",0,"0_0_0"),
	(7,8,"train",0,"0_0_0"),
	(8,1,"train",0,"0_0_0"),
	(1,9,"sea",0,"0_0_0"),
	(9,10,"sea",0,"0_0_0"),
	(10,5,"sea",0,"0_0_0"),
	(3,11,"pipe",0,"0_0_0"),
	(11,12,"pipe",0,"0_0_0"),
	(12,4,"train",0,"0_0_0")
]

for node_p in nodes:
	node = Classes.node(coordinates=f"{node_p[0]}_{node_p[1]}")
	node.create()

for edge_p in edges:
	edge = Classes.edges(incident_nodes=f"{edge_p[0]}_{edge_p[1]}",edge_type=edge_p[2],ice_condition=edge_p[3],tariff=edge_p[4])
	edge.create()
"""

node1 = Classes.node(coordinates="339_302")
node1.create()
node2 = Classes.node(coordinates="389_273")
node2.create()
node3 = Classes.node(coordinates="453_227")
node3.create()
node4 = Classes.node(coordinates="458_284")
node4.create()

edge1 = Classes.edges(edge_type="sea",length=10,ice_condition=1)
edge1.id_begin_node = node1.node_id
edge1.id_end_node = node2.node_id
edge1.create()

edge2 = Classes.edges(edge_type="sea",length=30,ice_condition=1)
edge2.id_begin_node = node2.node_id
edge2.id_end_node = node3.node_id
edge2.create()

edge3 = Classes.edges(edge_type="sea",length=5, tariff="15_15_15")
edge3.id_begin_node = node2.node_id
edge3.id_end_node = node4.node_id
edge3.create()

edge4 = Classes.edges(edge_type="sea",length=7)
edge4.id_begin_node = node4.node_id
edge4.id_end_node = node3.node_id
edge4.create()

iceb1 = Classes.icebreaker(port_id=node1.node_id,node_destination_id=node2.node_id)
iceb1.create()

iceb2 = Classes.icebreaker(port_id=node3.node_id,node_destination_id=node2.node_id)
iceb2.create()

ship1 = Classes.ship(in_port=True,port_id=node1.node_id,max_capacity=10,cargo_type="oil")
ship1.create()

ship2 = Classes.ship(in_port=True,port_id=node2.node_id,max_capacity=10,cargo_type="oil")
ship2.create()

ship3 = Classes.ship(in_port=True,port_id=node3.node_id,max_capacity=10,cargo_type="oil")
ship3.create()

cargo1 = Classes.consignment(id_refer=node1.node_id,node_destination_id=node3.node_id,cargo_type="oil",size=2)
cargo1.create()

cargo2 = Classes.consignment(id_refer=node1.node_id,node_destination_id=node3.node_id,cargo_type="oil",size=2,ship_immediately=True)
cargo2.create()

cargo3 = Classes.consignment(id_refer=node3.node_id,node_destination_id=node1.node_id,cargo_type="oil",size=2,ship_immediately=True)
cargo3.create()