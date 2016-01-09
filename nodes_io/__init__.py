#!/usr/bin/python3
import bpy
import bpy_extras

from mathutils import Euler  as math_euler
from mathutils import Vector as math_vector

# serialization
import json
import os

# tools
from . import utils


bl_info = {
	"name":        "Nodes IO",
	"author":      "Oren Titane (Genome36)",
	"version":     (0, 1, 0),
	"blender":     (2, 75, 0),
	"location":    "Properties > Material > Nodes IO",
	"description": "Import and export shaders as files.",
	"warning":     "Alpha.",
	"wiki_url":    "",
	"tracker_url": "",
	"category":    "Material"
}


__author__    = "Titane Amram Oren"
__copyright__ = "Copyright (C) 2015 Titane Amram Oren <orentitane@gmail.com>"
__license__   = "Proprietary software"
__version__   = "Nodes IO version %s.%s.%s" % bl_info["version"]


# --------------------------------------------------
# IMPORT OPERATOR
# --------------------------------------------------

class sio_import(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	bl_idname = "sio.import"
	bl_label  = "Import file as shader"

	directory = bpy.props.StringProperty(
		maxlen  = 1024,
		subtype = "NONE",
		options = {"HIDDEN", "SKIP_SAVE"}
	)

	files = bpy.props.CollectionProperty(
		type    = bpy.types.OperatorFileListElement,
		options = {"HIDDEN", "SKIP_SAVE"}
	)

	filter_glob = bpy.props.StringProperty(
		default = "*.mat",
		options = {"HIDDEN"},
	)


	def execute(self, context):
		active_object = context.active_object
		material      = active_object.material_slots[0].material
		mat_tree      = material.node_tree

		for shader in self.files:
			#~ try:
			# load shader data
			file_path = os.path.join(self.directory, shader.name)
			with open(file_path, "r") as shader_file:
				shader = json.load(shader_file)

			# deselect all nodes prior to import
			for node in mat_tree.nodes:
				if hasattr(node, "select"):
					node.select = False

			# create nodes
			for tree_index in range(len(shader["trees"])-1, -1, -1):
				tree = shader["trees"][str(tree_index)] # json converts int keys to str

				# determine whats node tree to use (either base or group)
				if tree_index > 0: # groups trees
					# prevent any duplicates
					if tree["name"] in [ i.name for i in bpy.data.node_groups ]:
						nodes_tree = bpy.data.node_groups[tree["name"]]
					else:
						nodes_tree = bpy.data.node_groups.new(tree["name"], tree["type"])
				else:
					nodes_tree = mat_tree


				# parse
				for node_data in tree["nodes"]:
					#~ try:
					# create instance
					node = nodes_tree.nodes.new(node_data["attributes"]["bl_idname"])
					node.select = True

					# add datablock to node group
					if node_data["attributes"]["bl_idname"] == "ShaderNodeGroup":
						node.node_tree = bpy.data.node_groups[node_data["attributes"]["datablock"]]

					# remove read-only attributes before applying
					del node_data["attributes"]["bl_idname"]
					del node_data["attributes"]["datablock"]

					# set attributes

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
							node_attr = getattr(node, attr)
							value     = node_data["attributes"][attr]

							# mathutils vector
							if isinstance(node_attr, math_vector):
								setattr(node, attr, math_vector(value))

							# mathutils euler
							elif isinstance(node_attr, math_euler):
								setattr(node, attr, math_euler(*value))

							# all others
							else:
								setattr(node, attr, value)

					# set inputs
					for index in range(0, len(node_data["inputs"])):
						if str(index) in node_data["inputs"]:
							bl_idname, sock_name, value = node_data["inputs"][str(index)] #json
							if "NodeGroupOutput" == node.bl_idname:
								nodes_tree.outputs.new(bl_idname, sock_name)

							if hasattr(node.inputs[index], "default_value"):
								node.inputs[index].default_value = value

					# set outputs
					for index in range(0, len(node_data["outputs"])):
						if str(index) in node_data["outputs"]:
							bl_idname, sock_name, value = node_data["outputs"][str(index)] #json
							if "NodeGroupInput" == node.bl_idname:
								nodes_tree.inputs.new(bl_idname, sock_name)

							if hasattr(node.outputs[index], "default_value"):
								node.outputs[index].default_value = value

					# parent
					parent = node_data["parent"]
					if parent:
						node.parent = nodes_tree.nodes[parent]

					#~ except Exception as error:
						#~ print(error)


				# create links
				for link_data in tree["links"]:
				#~ try:
					name, index = link_data["from"]
					from_socket = nodes_tree.nodes[name].outputs[index]

					name, index = link_data["to"]
					to_socket   = nodes_tree.nodes[name].inputs[index]

					nodes_tree.links.new(from_socket, to_socket)

				#~ except Exception as error:
					#~ print(error)

		return {'FINISHED'}

# --------------------------------------------------
# EXPORT OPERATOR
# --------------------------------------------------

class sio_export(bpy.types.Operator):
	bl_idname = "sio.export"
	bl_label  = "Export shader to file"

	def execute(self, context):
		active_object = context.active_object
		material      = active_object.material_slots[0].material
		mat_tree      = material.node_tree

		trees_list = {
			0: ("base", mat_tree.bl_idname, mat_tree)
		}

		# find groups via recursion
		#~ groups = {}
		def recursive_search(tree, level=1):
			# parse nodes
			for node in tree.nodes:
				if node.type == "GROUP":
					# create level index
					#~ if not level in groups:
						#~ groups[level] = []

					# if node group has node tree
					if node.node_tree != None:
						for datablock in bpy.data.node_groups:
							if datablock == node.node_tree:

								# search for stored duplicate
								inside = False
								for index in trees_list:
									name, bl_idname, block = trees_list[index]
									if datablock == block:
										inside = True
										break

								# len(trees_list) is already +1
								if not inside:
									trees_list[len(trees_list)] = (datablock.name, datablock.bl_idname, datablock)

								# recursion
								level += 1
								recursive_search(datablock, level=level)
								level -= 1

								# stop loop for efficiency
								break

		recursive_search(mat_tree)


		trees_dump = {}
		for index in range(len(trees_list)-1, -1, -1):
			name, bl_idname, tree = trees_list[index]

			nodes_list = []
			for node in tree.nodes:
				parent = None
				if node.parent:
					parent = node.parent.name

				nodes_list.append(
					{
						"attributes": utils.get.attributes(node),
						"inputs":     utils.get.sockets(node.inputs),
						"outputs":    utils.get.sockets(node.outputs),
						"parent":     parent
					}
				)

			trees_dump[index] = {
				"name":  name,
				"type":  bl_idname,
				"nodes": nodes_list,
				"links": utils.get.links(tree)
			}


		# format name
		mat_name = material.name
		for i in [".", " "]:
			mat_name = mat_name.replace(i, "_")

		# get directory
		blend_path = bpy.data.filepath
		directory  = os.path.dirname(blend_path)
		file_path  = os.path.join(directory, "%s.mat" % mat_name)

		#~ # dump shader data
		with open(file_path, "w") as shader_file:
			json.dump(
				{
					"engine":  context.scene.render.engine,
					"version": bpy.app.version,
					"trees":   trees_dump,
					#~ "groups":  groups
				},
				shader_file,
				indent = 4
			)

		return {'FINISHED'}

# --------------------------------------------------
# ADD OPERATOR TO NODE EDITOR HEADER
# --------------------------------------------------

def node_editor_operator(self, context):
	active_object = context.active_object

	layout = self.layout
	row    = layout.row(align=True)

	row.operator(sio_import.bl_idname, icon="PASTEFLIPDOWN", text="")
	row.operator(sio_export.bl_idname, icon="PASTEFLIPUP",   text="")

	if active_object.type == "MESH" and len(active_object.material_slots.items()) > 0:
		row.enabled = True
	else:
		row.enabled = False


def register():
	bpy.utils.register_module(__name__)
	bpy.types.NODE_HT_header.append(node_editor_operator)

	import imp
	imp.reload(utils)
	imp.reload(attributes)

	#bpy.types.USERPREF_HT_header.append()
	# debugging - actually prevents blender from running and launches a python console in a terminal to probe script values
	#__import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})


def unregister():
	bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
	try:
		unregister()
	except:
		pass
	register()
