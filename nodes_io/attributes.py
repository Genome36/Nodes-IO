#!/usr/bin/python3

# --------------------------------------------------
# ATTRIBUTES
# --------------------------------------------------

defaults = [
	"bl_idname",
#	"type", # read-only

	"name",
	"label",

#	"parent",
	"select",

	"location",
#	"dimensions", # read-only
	"width",
	"height",
#	"width_hidden",

	"use_custom_color",
	"color",

	"hide",
	"mute",

	"show_options",
	"show_preview",
	"show_texture",

#	"inputs",
#	"outputs",
]

specials = [
	"attribute_name",   # ["ATTRIBUTE"]
	"axis",             # ["TANGENT"]
	"blend_type",       # ["MIX_RGB"]
	"bytecode",         # ["SCRIPT"]
	"bytecode_hash",    # ["SCRIPT"]
	"color_mapping",    # ["TEX_IMAGE", "TEX_ENVIRONMENT", "TEX_NOISE", "TEX_GRADIENT", "TEX_MUSGRAVE", "TEX_MAGIC", "TEX_WAVE", "TEX_SKY", "TEX_VORONOI", "TEX_CHECKER", "TEX_BRICK"]
	"color_ramp",       # ["VALTORGB"]
	"color_space",      # ["TEX_IMAGE", "TEX_ENVIRONMENT"]
	"coloring",         # ["TEX_VORONOI"]
	"component",        # ["BSDF_HAIR", "BSDF_TOON"]
	"convert_from",     # ["VECT_TRANSFORM"]
	"convert_to",       # ["VECT_TRANSFORM"]
	"direction_type",   # ["TANGENT"]
	"distribution",     # ["BSDF_GLOSSY", "BSDF_REFRACTION", "BSDF_ANISOTROPIC", "BSDF_GLASS"]
	"falloff",          # ["SUBSURFACE_SCATTERING"]
	"filepath",         # ["SCRIPT"]
	"from_dupli",       # ["UVMAP", "TEX_COORD"]
	"gradient_type",    # ["TEX_GRADIENT"]
	"ground_albedo",    # ["TEX_SKY"]
	"image",            # ["TEX_IMAGE", "TEX_ENVIRONMENT"]
	"interpolation",    # ["TEX_IMAGE"]
	"invert",           # ["BUMP"]
	"is_active_output", # ["OUTPUT_MATERIAL", "OUTPUT_LAMP"]
	"label_size",       # ["FRAME"]
	"mapping",          # ["CURVE_RGB", "CURVE_VEC"]
	"max",              # ["MAPPING"]
	"min",              # ["MAPPING"]
	"mode",             # ["SCRIPT"]
	"musgrave_type",    # ["TEX_MUSGRAVE"]
	"node_tree",        # ["GROUP"]
	"object",           # ["TEX_COORD"]
	"offset",           # ["TEX_BRICK"]
	"offset_frequency", # ["TEX_BRICK"]
	"operation",        # ["VECT_MATH", "MATH"]
	"projection",       # ["TEX_IMAGE", "TEX_ENVIRONMENT"]
	"projection_blend", # ["TEX_IMAGE"]
	"rotation",         # ["MAPPING"]
	"scale",            # ["MAPPING"]
	"script",           # ["SCRIPT"]
	"shrink",           # ["FRAME"]
	"sky_type",         # ["TEX_SKY"]
	"space",            # ["NORMAL_MAP"]
	"squash",           # ["TEX_BRICK"]
	"squash_frequency", # ["TEX_BRICK"]
	"sun_direction",    # ["TEX_SKY"]
	"text",             # ["FRAME"]
	"texture_mapping",  # ["TEX_IMAGE", "TEX_ENVIRONMENT", "TEX_NOISE", "TEX_GRADIENT", "TEX_MUSGRAVE", "TEX_MAGIC", "TEX_WAVE", "TEX_SKY", "TEX_VORONOI", "TEX_CHECKER", "TEX_BRICK"]
	"translation",      # ["MAPPING"]
	"turbidity",        # ["TEX_SKY"]
	"turbulence_depth", # ["TEX_MAGIC"]
	"use_alpha",        # ["MIX_RGB"]
	"use_auto_update",  # ["SCRIPT"]
	"use_clamp",        # ["MIX_RGB", "MATH"]
	"use_max",          # ["MAPPING"]
	"use_min",          # ["MAPPING"]
	"use_pixel_size",   # ["WIREFRAME"]
	"uv_map",           # ["TANGENT", "UVMAP", "NORMAL_MAP"]
	"vector_type",      # ["MAPPING", "VECT_TRANSFORM"]
	"wave_type",        # ["TEX_WAVE"]
]

# --------------------------------------------------
# INPUTS / OUTPUTS TYPES
# --------------------------------------------------

sock_vectors = [
	"RGBA",
	"VECTOR",
]

sock_values = [
	"CUSTOM",
	"VALUE",
	"INT",
	"BOOLEAN",
	"STRING",
]
