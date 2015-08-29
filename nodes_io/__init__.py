#!/usr/bin/python3
import bpy
import bpy_extras

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
		tree          = material.node_tree

		for shader in self.files:
			#~ try:
			# load shader data
			file_path = os.path.join(self.directory, shader.name)
			with open(file_path, "r") as shader_file:
				shader = json.load(shader_file)

			# create nodes
			for node_data in shader["root"]["nodes"]:
				#~ try:
				# create instance
				node = tree.nodes.new(node_data["attributes"]["bl_idname"])
				del node_data["attributes"]["bl_idname"]

				# set attributes
				for attr in node_data["attributes"]:
					setattr(node, attr, node_data["attributes"][attr])

				# set inputs
				for index, value in node_data["inputs"]:
					if hasattr(node.inputs[index], "default_value"):
						node.inputs[index].default_value = value

				# set outputs
				for index, value in node_data["outputs"]:
					if hasattr(node.outputs[index], "default_value"):
						node.outputs[index].default_value = value

				parent = node_data["parent"]
				if parent:
					node.parent = tree.nodes[parent]

				#~ except Exception as error:
					#~ print(error)

			# create links
			for link_data in shader["root"]["links"]:
				name, index  = link_data["from"]
				input_socket = tree.nodes[name].outputs[index]

				name, index   = link_data["to"]
				output_socket = tree.nodes[name].inputs[index]

				tree.links.new(input_socket, output_socket)

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
		tree          = material.node_tree

		# find groups via recursion
		groups = {}
		def recursive_search(tree, level=0):
			# parse nodes
			for node in tree.nodes:
				if node.type == "GROUP":
					# create level index
					if not level in groups:
						groups[level] = []

					groups[level].append(node.name)

					# recursion
					level += 1
					recursive_search(node.node_tree, level=level)
					level -= 1

		recursive_search(tree)
		print(groups)

		trees_list = []
		for root in [tree]:

			nodes_list = []
			for node in root.nodes:
				parent = None
				if node.parent:
					parent = node.parent.name
					print(parent)

				nodes_list.append(
					{
						"attributes": utils.get.attributes(node),
						"inputs":     utils.get.sockets(node.inputs),
						"outputs":    utils.get.sockets(node.outputs),
						"parent":     parent
					}
				)

				#~ print(nodes_list)

		# format name
		mat_name = material.name
		for i in [".", " "]:
			mat_name = mat_name.replace(i, "_")

		# get directory
		blend_path = bpy.data.filepath
		directory  = os.path.dirname(blend_path)
		file_path  = os.path.join(directory, "%s.mat" % mat_name)

		# dump shader data
		with open(file_path, "w") as shader_file:
			json.dump(
				{
					"engine":  context.scene.render.engine,
					"version": bpy.app.version,
					"root": {
						"nodes": nodes_list,
						"links": utils.get.links(tree), # parse links
					},
						"groups": groups
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
