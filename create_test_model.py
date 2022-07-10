import Classes


node1 = Classes.node()
node1.create()
node2 = Classes.node()
node2.create()
node3 = Classes.node()
node3.create()
node4 = Classes.node()
node4.create()
node5 = Classes.node()
node5.create()
node6 = Classes.node()
node6.create()
node7 = Classes.node()
node7.create()

edge1 = Classes.edges(edge_type="sea",length=6,ice_condition=1)
edge1.id_begin_node = node1.node_id
edge1.id_end_node = node2.node_id
edge1.create()

edge2 = Classes.edges(edge_type="sea",length=10,ice_condition=1)
edge2.id_begin_node = node2.node_id
edge2.id_end_node = node3.node_id
edge2.create()

edge3 = Classes.edges(edge_type="sea",length=20,ice_condition=1)
edge3.id_begin_node = node3.node_id
edge3.id_end_node = node7.node_id
edge3.create()

edge4 = Classes.edges(edge_type="train",length=15)
edge4.id_begin_node = node2.node_id
edge4.id_end_node = node4.node_id
edge4.create()

edge5 = Classes.edges(edge_type="sea",length=7)
edge5.id_begin_node = node4.node_id
edge5.id_end_node = node5.node_id
edge5.create()

edge6 = Classes.edges(edge_type="sea",length=7)
edge6.id_begin_node = node5.node_id
edge6.id_end_node = node6.node_id
edge6.create()

"""
edge3 = Classes.edges(edge_type="train",length=10)
edge3.id_begin_node = node2.node_id
edge3.id_end_node = node4.node_id
edge3.create()

edge4 = Classes.edges(edge_type="sea",length=10)
edge4.id_begin_node = node4.node_id
edge4.id_end_node = node5.node_id
edge4.create()

edge5 = Classes.edges(edge_type="sea",length=10)
edge5.id_begin_node = node5.node_id
edge5.id_end_node = node6.node_id
edge5.create()
"""


ship1 = Classes.ship(in_port=True,port_id=node1.node_id,max_capacity=10,cargo_type="oil")
ship1.create()

ship2 = Classes.ship(in_port=True,port_id=node1.node_id,max_capacity=10,cargo_type="cont")
ship2.create()

ship3 = Classes.ship(in_port=True,port_id=node1.node_id,max_capacity=10,cargo_type="weight")
ship3.create()

ship4 = Classes.ship(in_port=True,port_id=node7.node_id,max_capacity=10,cargo_type="oil")
ship4.create()

#ship5 = Classes.ship(in_port=True,port_id=node1.node_id,max_capacity=10,cargo_type="cont")
#ship5.create()

ship6 = Classes.ship(in_port=True,port_id=node6.node_id,max_capacity=10,cargo_type="weight")
ship6.create()

ship7 = Classes.ship(in_port=True,port_id=node4.node_id,max_capacity=10,cargo_type="oil")
ship7.create()


"""
edge3 = Classes.edges(edge_type="train",length=20)
edge3.id_begin_node = node2.node_id
edge3.id_end_node = node4.node_id
edge3.create()
"""

cargo1 = Classes.consignment(id_refer=node1.node_id,node_destination_id=node6.node_id,cargo_type="oil",size=2)
cargo1.create()

cargo2 = Classes.consignment(id_refer=node1.node_id,node_destination_id=node7.node_id,cargo_type="oil",size=3)
cargo2.create()

cargo3 = Classes.consignment(id_refer=node1.node_id,node_destination_id=node7.node_id,cargo_type="cont",size=3)
cargo3.create()

cargo4 = Classes.consignment(id_refer=node1.node_id,node_destination_id=node7.node_id,cargo_type="weight",size=3)
cargo4.create()

cargo5 = Classes.consignment(id_refer=node7.node_id,node_destination_id=node6.node_id,cargo_type="oil",size=2)
cargo5.create()

cargo6 = Classes.consignment(id_refer=node6.node_id,node_destination_id=node2.node_id,cargo_type="oil",size=2)
cargo6.create()

iceb1 = Classes.icebreaker(port_id=node1.node_id,node_destination_id=node2.node_id)
iceb1.create()

iceb2 = Classes.icebreaker(port_id=node2.node_id,node_destination_id=node3.node_id)
iceb2.create()

iceb2 = Classes.icebreaker(port_id=node3.node_id,node_destination_id=node7.node_id)
iceb2.create()

iceb2 = Classes.icebreaker(port_id=node7.node_id,node_destination_id=node3.node_id)
iceb2.create()

#cargo3 = Classes.consignment(id_refer=node3.node_id,node_destination_id=node1.node_id,cargo_type="oil",size=3)
#cargo3.create()

#cargo4 = Classes.consignment(id_refer=node3.node_id,node_destination_id=node2.node_id,cargo_type="oil",size=3)
#cargo4.create()

"""
cargo3 = Classes.consignment(id_refer=node3.node_id,node_destination_id=node1.node_id,cargo_type="oil",size=3)
cargo3.create()

cargo4 = Classes.consignment(id_refer=node2.node_id,node_destination_id=node1.node_id,cargo_type="oil",size=3)
cargo4.create()

cargo5 = Classes.consignment(id_refer=node3.node_id,node_destination_id=node2.node_id,cargo_type="oil",size=3)
cargo5.create()
"""

#cargo3 = Classes.consignment(id_refer=node4.node_id,node_destination_id=node3.node_id)
#cargo3.create()