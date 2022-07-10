import Classes


node1 = Classes.node()
node1.create()
node2 = Classes.node()
node2.create()
node3 = Classes.node()
node3.create()
node4 = Classes.node()
node4.create()
"""
node5 = Classes.node()
node5.create()
node6 = Classes.node()
node6.create()
node7 = Classes.node()
node7.create()
"""

edge1 = Classes.edges(edge_type="sea",length=10,ice_condition=1)
edge1.id_begin_node = node1.node_id
edge1.id_end_node = node2.node_id
edge1.create()

edge2 = Classes.edges(edge_type="sea",length=30,ice_condition=1)
edge2.id_begin_node = node2.node_id
edge2.id_end_node = node3.node_id
edge2.create()

edge3 = Classes.edges(edge_type="sea",length=5)
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