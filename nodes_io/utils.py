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
		"ShaderNodeAddShader",
		"ShaderNodeCameraData",
		"ShaderNodeHairInfo",
		"ShaderNodeHoldout",
		"ShaderNodeLightPath",
		"ShaderNodeNewGeometry",
		"ShaderNodeObjectInfo",
		"ShaderNodeOutputLamp",
		"ShaderNodeOutputMaterial",
		"ShaderNodeParticleInfo",
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

			try:
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

			except:
				raise Exception("Could not get %s sockets.\n" % sock.node.name)

		return data

# --------------------------------------------------
# GET ATTRIBUTES
# --------------------------------------------------

	def attributes(node):
		attr_dict = {}
		for attr_list in [attributes.defaults]:#, attributes.specials]:

		# group datablock
		if node.bl_idname in ["ShaderNodeGroup"] and node.node_tree != None:
			attr_dict["datablock"] = node.node_tree.name
		else:
			attr_dict["datablock"] = None


			for attr in attr_list:
				try:
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

						# object
						elif attr in ["object"]:
							if getattr(node, attr):
								value = getattr(node, attr).name

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

				except:
					raise Exception("Could not get %s attributes.\n" % node.name)


		return attr_dict

# --------------------------------------------------
# GET LINKS
# --------------------------------------------------

	def links(tree):
		links_data = []
		for link in tree.links:
			try:
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

			except:
				raise Exception("Could not get node links.\n")

		return links_data


class set():

	DEBUG = True

	def __init__():
		pass

# --------------------------------------------------
# SET SOCKETS INPUTS/OUTPUTS
# --------------------------------------------------

	class socket():

		def __init__():
			pass


		def inputs(tree, node, node_data):
			for index in range(0, len(node_data["inputs"])):
				#~ print(tree_index, index, node.bl_idname, node_data["inputs"])

				if str(index) in node_data["inputs"]:
					bl_idname, sock_name, sock_value, sock_min, sock_max = node_data["inputs"][str(index)] #json

					try:
						if "NodeGroupOutput" == node.bl_idname:
							# node inputs = group outputs
							socket = tree.outputs.new(bl_idname, sock_name)

						if node.bl_idname not in ignore.nodes:
							if hasattr(node.inputs[index], "default_value"):
								node.inputs[index].default_value = sock_value

					except:
						raise Exception("Could not set values for node socket %s.\n" % sock_name)


		def outputs(tree, node, node_data):
			for index in range(0, len(node_data["outputs"])):
				if str(index) in node_data["outputs"]:
					bl_idname, sock_name, sock_value, sock_min, sock_max = node_data["outputs"][str(index)] #json

					try:
						if  node.bl_idname == "NodeGroupInput":
							# node outputs = group inputs
							socket = tree.inputs.new(bl_idname, sock_name)

							# debug
							if bl_idname != socket.bl_socket_idname:
								print(node.bl_idname, "socket differs from original !")

							if socket.bl_socket_idname in ["NodeSocketFloat", "NodeSocketFloatFactor"]:
								if hasattr(socket, "min_value") and hasattr(socket, "max_value"):
									socket.min_value = sock_min
									socket.max_value = sock_max

						if node.bl_idname not in ignore.nodes:
							if hasattr(node.outputs[index], "default_value"):
								node.outputs[index].default_value = sock_value

					except:
						raise Exception("Could not set values for node socket %s.\n" % sock_name)

# --------------------------------------------------
# SET ATTRIBUTES
# --------------------------------------------------

	def attributes(tree, node, node_data):
		# parent
		parent = node_data["parent"]
		if parent:
			node.parent = tree.nodes[parent]

		# color ramp
		if node.bl_idname in ["ShaderNodeValToRGB"]:
			node.color_ramp.color_mode    = node_data["attributes"]["color_mode"]
			node.color_ramp.interpolation = node_data["attributes"]["interpolation"]

			elements = node_data["attributes"]["elements"]
			missing_pointers = len(elements) - len(node.color_ramp.elements)
			for i in range(0, missing_pointers):
				node.color_ramp.elements.new(0.0)

			for index in range(0, len(elements)):
				pos, color = elements[str(index)] #json
				node.color_ramp.elements[index].position = pos
				node.color_ramp.elements[index].color    = color

		else:
			for attr in node_data["attributes"]:
				try:
					node_attr = getattr(node, attr)
					value     = node_data["attributes"][attr]

					# mathutils vector
					if isinstance(node_attr, math_vector):
						setattr(node, attr, math_vector(value))

					# mathutils euler
					elif isinstance(node_attr, math_euler):
						setattr(node, attr, math_euler(*value))

					# object
					elif attr in ["object"]:
						setattr(node, attr, bpy.data.objects[value])

					# all others
					else:
						setattr(node, attr, value)

				except:
					raise Exception("Could not set attributes for node %s.\n" % node.name)


# --------------------------------------------------
# SET LINKS
# --------------------------------------------------

	def links(tree, links):
		for link_data in links:
			try:
				name, index = link_data["from"]
				from_socket = tree.nodes[name].outputs[index]

				name, index = link_data["to"]
				to_socket   = tree.nodes[name].inputs[index]

				tree.links.new(from_socket, to_socket)

			except:
				raise Exception("Could not set node links.\n")
