# __init__.py
# This file can be empty or include package-level initialization code.
import importlib
import os

node_list = [ #Add list of .py files containing nodes here
    "oop_node",
    "oop_person_node",
    "oop_hair_node",
    "oop_clothing_node",
    "oop_mouth_node",
    "oop_eyes_node",
    "oop_pose_node",
    "oop_style_node",
    "oop_view_node",
    "oop_location_node"
]

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for module_name in node_list:
    imported_module = importlib.import_module(".{}".format(module_name), __name__)

    NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
    NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
