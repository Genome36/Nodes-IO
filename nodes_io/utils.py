#!/usr/bin/python3
from . import attributes

from mathutils import Euler  as math_euler
from mathutils import Vector as math_vector


class ignore():

	socket_types = [
		"NodeSocketVirtual",
	]

	# only nodes with no socket values needed
	nodes = [
		"NodeFrame",
		"NodeReroute",
		"ShaderNodeAttribute",
		"ShaderNodeCameraData",
		"ShaderNodeHairInfo",
		"ShaderNodeHoldout",
		"ShaderNodeLightPath",
		"ShaderNodeNewGeometry",
		"ShaderNodeObjectInfo",
		"ShaderNodeOutputLamp",
		"ShaderNodeOutputMaterial",
		"ShaderNodeParticleInfo",
		"ShaderNodeRGB",
		"ShaderNodeTangent",
		"ShaderNodeTexCoord",
		"ShaderNodeUVMap",
		"ShaderNodeValue"
	]


class get():

	DEBUG = True

	def __init__():
		pass

# --------------------------------------------------
# GET SOCKETS INPUTS/OUTPUTS
# --------------------------------------------------

	def sockets(tree, io):
		data = {}
		for index in range(0, len(io)):
			sock      = io[index]
			sock_type = str(sock.type)

			#~ try:
			if sock.bl_idname not in ignore.socket_types and sock.node.bl_idname not in ignore.nodes:
				value    = None
				sock_min = None
				sock_max = None

				# group input min and max values for user
				if sock.node.bl_idname == "NodeGroupInput":
					if tree.inputs[index].bl_socket_idname in ["NodeSocketFloat", "NodeSocketFloatFactor"]:
						sock_min = tree.inputs[index].min_value
						sock_max = tree.inputs[index].max_value

				# get value
				if sock_type in ["RGBA", "VECTOR"]:
					value = [ i for i in sock.default_value ]

				elif sock_type in ["CUSTOM", "VALUE", "INT", "BOOLEAN", "STRING"]:
					if hasattr(sock, "default_value"):
						value = sock.default_value

				data[index] = (sock.bl_idname, sock.name, value, sock_min, sock_max)

			#~ except:
				#~ pass

		return data

# --------------------------------------------------
# GET ATTRIBUTES
# --------------------------------------------------

	def attributes(node):
		attr_dict = {}
		for attr_list in [attributes.defaults]:#, attributes.specials]:
			for attr in attr_list:

				if hasattr(node, attr):
					value = getattr(node, attr)

					# tuple
					if attr in ["location", "color"]:
						value = [i for i in value]

					# mathutils vector
					elif isinstance(value, math_vector):
						value = value.copy()
						value = [value.x, value.y, value.z]

					# mathutils euler
					elif isinstance(value, math_euler):
						value = value.copy()
						value = [[value.x, value.y, value.z], value.order]

					# color ramp
					elif node.bl_idname in ["ShaderNodeValToRGB"]:
						attr_dict["color_mode"]    = node.color_ramp.color_mode
						attr_dict["interpolation"] = node.color_ramp.interpolation

						attr_dict["elements"] = {}
						elements = node.color_ramp.elements
						for index in range(0, len(elements)):
							pos   = elements[index].position
							color = [i for i in elements[index].color]

							attr_dict["elements"][index] = [pos, color]

					# default
					elif hasattr(value, "default_value"):
						value = value.default_value

					attr_dict[attr] = value

		# group datablock
		if node.bl_idname == "ShaderNodeGroup":
			attr_dict["datablock"] = node.node_tree.name
		else:
			attr_dict["datablock"] = None

		return attr_dict

# --------------------------------------------------
# GET LINKS
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


class set():

	DEBUG = True

	def __init__():
		pass

# --------------------------------------------------
# SET SOCKETS INPUTS/OUTPUTS
# --------------------------------------------------

	def socket(io):
		pass

# --------------------------------------------------
# SET ATTRIBUTES
# --------------------------------------------------

	def attributes(node):
		pass

# --------------------------------------------------
# SET LINKS
# --------------------------------------------------

	def links(tree):
		pass
