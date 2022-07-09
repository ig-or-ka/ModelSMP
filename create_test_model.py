import Classes

node1 = Classes.node()
node1.create()
node2 = Classes.node()
node2.create()
node3 = Classes.node()
node3.create()
#node4 = Classes.node()
#node4.create()

edge1 = Classes.edges(edge_type="sea",length=6)
edge1.id_begin_node = node1.node_id
edge1.id_end_node = node2.node_id
edge1.create()

edge2 = Classes.edges(edge_type="sea",length=10)
edge2.id_begin_node = node2.node_id
edge2.id_end_node = node3.node_id
edge2.create()

"""
edge3 = Classes.edges(edge_type="train",length=20)
edge3.id_begin_node = node2.node_id
edge3.id_end_node = node4.node_id
edge3.create()
"""

cargo1 = Classes.consignment(id_refer=node1.node_id,node_destination_id=node2.node_id,cargo_type="oil",size=2)
cargo1.create()

cargo2 = Classes.consignment(id_refer=node2.node_id,node_destination_id=node3.node_id,cargo_type="oil",size=3)
cargo2.create()

cargo3 = Classes.consignment(id_refer=node3.node_id,node_destination_id=node1.node_id,cargo_type="oil",size=3)
cargo3.create()

cargo4 = Classes.consignment(id_refer=node2.node_id,node_destination_id=node1.node_id,cargo_type="oil",size=3)
cargo4.create()

cargo5 = Classes.consignment(id_refer=node3.node_id,node_destination_id=node2.node_id,cargo_type="oil",size=3)
cargo5.create()

ship1 = Classes.ship(in_port=True,port_id=node1.node_id,max_capacity=10,cargo_type="oil")
ship1.create()

#cargo3 = Classes.consignment(id_refer=node4.node_id,node_destination_id=node3.node_id)
#cargo3.create()