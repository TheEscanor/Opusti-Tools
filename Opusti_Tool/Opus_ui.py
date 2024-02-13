
import statistics

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class 
from . import __init__
from . import Opus_Normal
from . import Opus_Utility
from . import Opus_Update
from . import Opus_ComboPanel
import bmesh
from mathutils import Vector, Matrix
import re

from bpy.types import Panel
from bpy.types import Scene
from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)
getTriHalf=0
Testnumber=0

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        clr = context.scene.mytool_color
        print (clr[0], clr[1], clr[2], clr[3])
        return {'FINISHED'}
##--------------------------------------------------- Vertex Groups for brick scatter and wood scatter

#----------------------------------------------------Toggle Wireframe
class CustomOperatorVertexGroupbrick(bpy.types.Operator):
    bl_idname = "object.custom_operatorvertexgroupbrick"
    bl_label = "Assign Vertex Group to Attribute"
    
    def execute(self, context):
        bpy.ops.object.geometry_nodes_input_attribute_toggle(prop_path='["Vertical"]', modifier_name="Geometry Nodes")
        bpy.context.object.modifiers["Geometry Nodes"]["Vertical"] = "Vertical"
        bpy.ops.object.geometry_nodes_input_attribute_toggle(prop_path='["Input_51_use_attribute"]', modifier_name="Geometry Nodes")
        bpy.context.object.modifiers["Geometry Nodes"]["Input_51_attribute_name"] = "Horizontal"
        bpy.ops.object.geometry_nodes_input_attribute_toggle(prop_path='["Input_55_use_attribute"]', modifier_name="Geometry Nodes")
        bpy.context.object.modifiers["Geometry Nodes"]["Input_55_attribute_name"] = "SingleX"
        bpy.ops.object.geometry_nodes_input_attribute_toggle(prop_path='["Input_56_use_attribute"]', modifier_name="Geometry Nodes")
        bpy.context.object.modifiers["Geometry Nodes"]["Input_56_attribute_name"] = "SingleY"
        bpy.ops.object.geometry_nodes_input_attribute_toggle(prop_path='["Input_43_use_attribute"]', modifier_name="Geometry Nodes")
        bpy.context.object.modifiers["Geometry Nodes"]["Input_43_attribute_name"] = "Random 90"
        bpy.ops.object.geometry_nodes_input_attribute_toggle(prop_path='["Input_53_use_attribute"]', modifier_name="Geometry Nodes")
        bpy.context.object.modifiers["Geometry Nodes"]["Input_53_attribute_name"] = "Random 45"
        return {'FINISHED'}