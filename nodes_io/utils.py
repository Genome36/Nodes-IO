#!/usr/bin/python3
from . import attributes

class get():

	DEBUG = True

	def __init__():
		pass

# --------------------------------------------------
#
# --------------------------------------------------

	def sockets(io):
		data = []
		for index in range(0, len(io)):
			sock = io[index]
			sock_type  = str(sock.type)

			try:
				if sock_type in ["RGBA", "VECTOR"]:
					value = [ i for i in sock.default_value ]

				elif sock_type in ["CUSTOM", "VALUE", "INT", "BOOLEAN", "STRING"]:
					value = sock.default_value

				data.append((index, value))

			except:
				pass

		return data

# --------------------------------------------------
#
# --------------------------------------------------

	def attributes(node):
		attr_dict = {}
		for attr_list in [attributes.defaults]:#, attributes.specials]:
			for attr in attr_list:

				if hasattr(node, attr):
					value = getattr(node, attr)

					if attr in ["location", "color"]:
						value = [i for i in value]

					elif hasattr(value, "default_value"):
						value = value.default_value

					attr_dict[attr] = value

		return attr_dict

# --------------------------------------------------
#
# --------------------------------------------------

	def links(tree):
		links_data = []
		for link in tree.links:

			# from
			node_outputs = link.from_socket.node.outputs
			for index in range(0, len(node_outputs)):
				if link.from_socket == node_outputs[index]:
					from_sock_index = index

			# to
			node_inputs = link.to_socket.node.inputs
			for index in range(0, len(node_inputs)):
				if link.to_socket == node_inputs[index]:
					to_sock_index = index

			links_data.append(
				{
					"from": [link.from_node.name, from_sock_index],
					"to":   [link.to_node.name,   to_sock_index]
				}
			)

		return links_data
