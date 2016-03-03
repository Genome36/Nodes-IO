#!/usr/bin/python3

from re import search

# serialization
from json import load
from json import dump

# tools
from . import debugging


DEBUG = debugging.get_state()


def __init__():
	pass


def get_data(file_path):
	with open(file_path, "r") as file:
		data = load(file)

	return data


def set_data(file_path, data):
	with open(file_path, "w") as file:
		dump(
			data,
			file,
			indent = 4,
			sort_keys = True
		)


def extension(tree_type):
	return {
		"ShaderNodeTree":     ".shd",
		"CompositorNodeTree": ".cmp",
		"TextureNodeTree":    ".tex",
	}[tree_type]
