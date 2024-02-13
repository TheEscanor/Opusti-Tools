import bpy
import bmesh
import shutil
from mathutils import Vector
import random
from mathutils import Vector, Matrix
import re
import subprocess
import threading
from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
import os
from . import Opus_Update
from . import Opus_ComboPanel
from bpy.types import Panel
from bpy.types import Scene
from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)
import sys
from bpy_extras.io_utils import ExportHelper
# Define an operator to set the active UV map for rendering
class SetActiveUVMapOperator(bpy.types.Operator):
    bl_idname = "object.uvmap_set_active"
    bl_label = "Set Active UV Map"

    uvmap_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.object
        uvmap = obj.data.uv_layers.get(self.uvmap_name)
        if uvmap:
            uvmap.active_render = not uvmap.active_render
        return {'FINISHED'}


# Define an operator to remove UV maps
class RemoveUVMapOperator(bpy.types.Operator):
    bl_idname = "object.uvmap_remove"
    bl_label = "Remove UV Map"

    uvmap_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.object
        uvmap = obj.data.uv_layers.get(self.uvmap_name)
        if uvmap:
            obj.data.uv_layers.remove(uvmap)
        return {'FINISHED'}


# Define an operator to add UV maps
class AddUVMapOperator(bpy.types.Operator):
    bl_idname = "object.uvmap_add"
    bl_label = "Add UV Map"

    def execute(self, context):
        obj = context.object
        uvmap_name = "UVMap" + str(len(obj.data.uv_layers) + 1)
        obj.data.uv_layers.new(name=uvmap_name)
        return {'FINISHED'}
##---------------------------------------Fix name of .001-.099
def fix_object_names(name):
    # Check if the name has a valid suffix
    name_parts = name.split('.')
    if len(name_parts) > 1:
        suffix = name_parts[-1]
        if suffix.startswith("00") or suffix.startswith("0"):
            try:
                suffix_num = int(suffix)
                if suffix_num >= 1 and suffix_num <= 99:
                    # Increment the suffix by 1
                    new_suffix_num = suffix_num + 1
                    new_suffix = str(new_suffix_num).zfill(3)
                    # Replace the old suffix with the new one
                    new_name = name.replace(suffix, new_suffix)
                    return new_name
            except ValueError:
                pass

    # If the name does not have a valid suffix, return it as is
    return name

    return filtered_objects
# Operator to update the active object's name
class UpdateObjectNameOperator(bpy.types.Operator):
    bl_idname = "object.update_object_name"
    bl_label = "Update Object Name"

    def execute(self, context):
        active_object = context.view_layer.objects.active
        if active_object:
            active_object.name = fix_object_names(active_object.name)
        return {'FINISHED'}
##---------------------------------------End
##---------------------------------------Icon
def iconLib(name="Opus_icon"):
    pcoll = preview_collections["main"]
    icon = pcoll[name]
    return(icon.icon_id)
###-----------------------------------------------------------vertex-----vertex
# Operator to select the furthest vertex, including furthest from the currently selected vertex
class SelectFurthestOperator(bpy.types.Operator):
    bl_idname = "object.select_furthest"
    bl_label = "Select Furthest Vertex"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        if len(selected_objects) == 1 and selected_objects[0].type == 'MESH':
            obj = selected_objects[0]
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')

            bm = bmesh.from_edit_mesh(obj.data)

            # Find the furthest vertex, including furthest from the currently selected vertex
            selected_verts = [v for v in bm.verts if v.select]
            cursor_location = bpy.context.scene.cursor.location if not selected_verts else selected_verts[0].co

            furthest_vert = max(bm.verts, key=lambda v: (v.co - cursor_location).length)
            furthest_vert.select_set(True)

            # Update the viewport
            bmesh.update_edit_mesh(obj.data)

        return {'FINISHED'}
# Operator to select the furthest face, including furthest from the currently selected face
class SelectFurthestOperatorFace(bpy.types.Operator):
    bl_idname = "object.select_furthestface"
    bl_label = "Select Furthest Face"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')

                bm = bmesh.from_edit_mesh(obj.data)

                # Find the furthest face, including furthest from the currently selected face
                selected_faces = [f for f in bm.faces if f.select]
                cursor_location = bpy.context.scene.cursor.location if not selected_faces else selected_faces[0].calc_center_median()

                furthest_face = max(bm.faces, key=lambda f: (f.calc_center_median() - cursor_location).length)
                furthest_face.select_set(True)

                # Update the viewport
                bmesh.update_edit_mesh(obj.data)

        return {'FINISHED'}
        
##-------------------------------------------------------------------multi function Vertex
# Function 1
def function1():
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
    print("Function 1 called!")

# Function 2
def function2():
    bpy.ops.object.select_furthest()
# Function 3
def function3():
    toggle_property: bpy.props.BoolProperty(default=False)
    try:
        bpy.context.scene.transform_orientation_slots[0].type = 'Face'
        bpy.ops.transform.delete_orientation()
        bpy.ops.transform.create_orientation(use=True)
    except:
        bpy.ops.transform.create_orientation(use=True)
    bpy.ops.wm.tool_set_by_id(name="builtin.move")
    bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')#center of mesh
    bpy.ops.transform.transform(mode='ALIGN')
    print("Function 3 called!")
def function4(): ##---------create box
        # Get the selected objects
    selected_objects = bpy.context.selected_objects
        
        # Check if any object is selected
    if not selected_objects:
        self.report({'ERROR'}, "Please select an object.")
        return {'CANCELLED'}
        # Get the active object
    active_obj = bpy.context.active_object
        # Create a new cube mesh
    bpy.ops.mesh.primitive_cube_add(size=1)
        # Get the newly created cube object
    new_obj = bpy.context.active_object
        # Match the dimensions of the new cube with the active object
    new_obj.dimensions = active_obj.dimensions
        # Match the rotation of the new cube with the active object
    new_obj.rotation_euler = active_obj.rotation_euler
        # Move the new cube to the center of the active object
    new_obj.location = active_obj.location
    print("Function 3 called!")
# Panel Operator
class CustomPanelOperatorMulticall(bpy.types.Operator):
    bl_idname = "object.custom_panel_operator"
    bl_label = "Custom Panel Operator"
    bl_description="Enable custom origins first, then you can use Orien Vertex and Orien Face to randomly find origin axes from vertices."
    def execute(self, context):
        loopsConvexHull()
        function1()
        function2()
        function2()
        function2()
        function2()
        loopsfunction3()
        #function4()
        #bpy.ops.object.create_cube()
        return {'FINISHED'}
##-------------------------------------------------------------------multi function FaceInt
# Function 1
def function01():
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
    print("Function 1 called!")

# Function 2
def function02():
    bpy.ops.object.select_furthestface()
    return {'FINISHED'}
def function03():
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Function 3 called!")
# Function 3
def function04():
    # Get the currently selected objects
    selected_objects = bpy.context.selected_objects

    for obj in selected_objects:
        # Set the current object as the active object
        bpy.context.view_layer.objects.active = obj

        # Switch to Edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Set a toggle property
        bpy.types.Scene.toggle_property = bpy.props.BoolProperty(default=False)

        try:
            # Set the transform orientation to 'Face'
            bpy.context.scene.transform_orientation_slots[0].type = 'FACE'

            # Delete the existing transform orientation
            bpy.ops.transform.delete_orientation()

            # Create a new transform orientation using the 'Face' orientation
            bpy.ops.transform.create_orientation(use=True)
        except:
            # If the 'Face' orientation doesn't exist, create a new one
            bpy.ops.transform.create_orientation(use=True)

        # Set the tool to 'Move'
        bpy.ops.wm.tool_set_by_id(name="builtin.move")

        # Switch back to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Set the object's origin to the center of mass
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

        # Perform a transform alignment
        bpy.ops.transform.transform(mode='ALIGN')
# Panel Operator
class CustomPanelOperatorMulticallFace(bpy.types.Operator):
    bl_idname = "object.custom_panel_operatorface"
    bl_label = "Custom Panel Operator"
    bl_description= "Enable custom origins first, then you can use Orien Vertex and Orien Face to randomly find origin axes from faces"
    def execute(self, context):
        loopsConvexHull()
        function01()
        function02()
        function02()
        function02()
        function02()
        function03()
        bpy.ops.object.random_deselect_operator()
        loopsfunction3()
        #function04()
        return {'FINISHED'}
class RandomDeselectOperator(bpy.types.Operator):
    bl_idname = "object.random_deselect_operator"
    bl_label = "Random Deselect"

    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            mesh = obj.data
            selected_faces = [i for i, f in enumerate(mesh.polygons) if f.select]

            # Deselect all but one random face
            if len(selected_faces) > 1:
                random_face = random.choice(selected_faces)
                for i in selected_faces:
                    if i != random_face:
                        mesh.polygons[i].select = False

        return {'FINISHED'}
##--------------------------------Create Collsion box
class CreateGeometryOperator(bpy.types.Operator):
    bl_idname = "object.create_cube"
    bl_label = "Create Cube"
    bl_description = "Create a new cube based on the active object"
    bl_description ="Create a box or UBX to surround all selected models, rotating it according to the angle calculated from OrienVertex, OrienFace, Coll. Vertex, and Coll. Face."
    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for active_obj in selected_objects:
            name_prefix = "UBX_" + active_obj.name + "_"

            bpy.ops.mesh.primitive_cube_add(size=1)
            new_obj = bpy.context.active_object

            new_obj.dimensions = active_obj.dimensions
            new_obj.rotation_euler = active_obj.rotation_euler
            new_obj.location = active_obj.location

            # Get the cube count in the scene to determine the suffix index
            cube_count = sum(1 for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.name.startswith(name_prefix))

            # Generate the new name with the suffix index
            new_name = name_prefix + str(cube_count + 1).zfill(2)
            new_obj.name = new_name

        return {'FINISHED'}
def createBoxesGoback():
    # Store the previous selection
    previous_selection = bpy.context.selected_objects

    selected_objects = previous_selection

    for active_obj in selected_objects:
        name_prefix = "UBX_" + active_obj.name + "_"

        bpy.ops.mesh.primitive_cube_add(size=1)
        new_obj = bpy.context.active_object

        new_obj.dimensions = active_obj.dimensions
        new_obj.rotation_euler = active_obj.rotation_euler
        new_obj.location = active_obj.location

        # Get the cube count in the scene to determine the suffix index
        cube_count = sum(1 for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.name.startswith(name_prefix))
        # Generate the new name with the suffix index
        new_name = name_prefix + str(cube_count + 1).zfill(2)
        new_obj.name = new_name

    # Restore the previous selection
    bpy.context.view_layer.objects.active = None
    bpy.ops.object.select_all(action='DESELECT')
    for obj in previous_selection:
        obj.select_set(True)

    return {'FINISHED'}
##-----------------------------------Create Collsion boxes loops
##------------Generate all done
# Operator to perform the separation
class SeparateLoosePartsOperator(bpy.types.Operator):
    bl_idname = "object.separate_loose_parts"
    bl_label = "Separate Loose Parts"
    bl_description = "Separate the mesh by loose parts"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')
        # Deselect all objects except the active object
        for obj in bpy.context.selected_objects:
            obj.select_set(False)
        context.active_object.select_set(True)
        return {'FINISHED'}
class OperatorLoopsCreateBoxesGenerate(bpy.types.Operator):
    bl_idname = "object.operator_loops_create_boxes_generate"
    bl_label = "Operator Loops Create Boxes"
    bl_description = "Generate UBX for objects within this collection"
    def execute(self, context):
        bpy.ops.object.separate_loose_parts()
        button_callbackGen(self, context)
        # Get the active object
        active_object = bpy.context.active_object
        # Get the collection of the active object
        active_collection = active_object.users_collection[0]
        # Select all objects in the active collection
        for obj in active_collection.objects:
            obj.select_set(True)
        createBoxesGoback()
        return {'FINISHED'}
def button_callbackGen(self, context):
    selected_collection = bpy.context.collection
    model_count = len(selected_collection.objects)

    for i in range(model_count):
        loopsByObjects()
        bpy.ops.object.custom_panel_operatorface()
        #createBoxesGoback()
    ##StartFace
class OperatorLoopsCreateBoxes(bpy.types.Operator):
    bl_idname = "object.operator_loops_create_boxes"
    bl_label = "Operator Loops Create Boxes"
    bl_description="The operation works similarly to OrienFace, but the usage method of Coll. Vertex is to click on just one model, and it will calculate all models within the same collection"
    def execute(self, context):
        button_callback(self, context)
        return {'FINISHED'}
def button_callback(self, context):
    selected_collection = bpy.context.collection
    model_count = len(selected_collection.objects)

    for i in range(model_count):
        loopsByObjects()
        bpy.ops.object.custom_panel_operatorface()
        print(f"Processing model {i+1}/{model_count}")
    ##En Face
    ##StartVertex
class OperatorLoopsCreateBoxesVertex(bpy.types.Operator):
    bl_idname = "object.operator_loops_create_boxes_vertex"
    bl_label = "Operator Loops Create Boxes"
    bl_description="The operation works similarly to Orien Vertex, but the usage method of Coll. Vertex is to click on just one model, and it will calculate all models within the same collection"
    
    def execute(self, context):
        button_callbackVertex(self, context)
        return {'FINISHED'}
def button_callbackVertex(self, context):
    selected_collection = bpy.context.collection
    model_count = len(selected_collection.objects)

    for i in range(model_count):
        loopsByObjects()
        bpy.ops.object.custom_panel_operator()
        print(f"Processing model {i+1}/{model_count}")
    ##End Vertex
def loopsByObjects():
        # Get the active collection
    collection = bpy.context.collection
        # Get all objects in the collection
    objects = [obj for obj in bpy.data.objects if obj.users_collection[0] == collection]
        # Find the currently selected object, if any
    active_obj = bpy.context.active_object
        # Find the index of the active object
    active_index = objects.index(active_obj) if active_obj in objects else -1
        # Select the next object in the collection
    next_index = (active_index + 1) % len(objects)
    next_obj = objects[next_index]
        # Deselect the previously selected object
    if active_obj:
        active_obj.select_set(False)
        # Select the next object
    next_obj.select_set(True)
    bpy.context.view_layer.objects.active = next_obj
        ##
def loopsfunction3():
    bpy.ops.object.mode_set(mode='EDIT')
    active_orientation = bpy.context.scene.transform_orientation_slots[0].type
    if active_orientation != 'GLOBAL' and len(bpy.context.scene.transform_orientation_slots) > 0:
        bpy.ops.object.delete_all_transform_orientation()            
    try:
        bpy.context.scene.transform_orientation_slots[0].type = 'Face'
        bpy.ops.transform.delete_orientation()
        bpy.ops.transform.create_orientation(use=True)
    except:
        bpy.ops.transform.create_orientation(use=True)
    
    bpy.ops.wm.tool_set_by_id(name="builtin.move")
    bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')  # center of mesh
    bpy.ops.transform.transform(mode='ALIGN')
    return {'FINISHED'}
    
def loopsConvexHull():
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.convex_hull()
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].decimate_type = 'DISSOLVE'
    bpy.ops.object.modifier_apply(modifier="Decimate")

##-----------------------------------End boxes loops
##--------------------------------Rename UV all object selection 
class OBJECT_OT_RenameUV(bpy.types.Operator):
    bl_idname = "object.rename_uv"
    bl_label = "Rename UV"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        first_uv_name = context.scene.first_uv_name
        second_uv_name = context.scene.second_uv_name

        for obj in selected_objects:
            if obj and obj.type == 'MESH':
                uv_names = obj.data.uv_layers.keys()
                if len(uv_names) >= 2:
                    for i, uv_name in enumerate(uv_names):
                        if i == 0:
                            obj.data.uv_layers[uv_name].name = first_uv_name
                        elif i == 1:
                            obj.data.uv_layers[uv_name].name = second_uv_name
                    self.report({'INFO'}, "Renamed UV layers in object '{}'".format(obj.name))
                elif len(uv_names) >= 1:
                    obj.data.uv_layers[uv_names[0]].name = first_uv_name
                    self.report({'INFO'}, "Renamed first UV layer in object '{}'".format(obj.name))
                else:
                    self.report({'WARNING'}, "Object '{}' does not have at least one UV layer".format(obj.name))
            else:
                self.report({'WARNING'}, "Skipping non-mesh object '{}'".format(obj.name))

        return {'FINISHED'}
class OBJECT_OT_ResetUVNames(bpy.types.Operator):
    bl_idname = "object.reset_uv_names"
    bl_label = "Reset UV Names"

    def execute(self, context):
        context.scene.first_uv_name = "UVmap0"
        context.scene.second_uv_name = "UVmap1"
        self.report({'INFO'}, "UV names reset to default values")
        return {'FINISHED'}
##-----------------------------------remove uselees material
class OBJECT_OT_RemoveUnusedMaterials(bpy.types.Operator):
    bl_idname = "object.remove_unused_materials"
    bl_label = "Remove Unused Materials"
    
    def execute(self, context):
        scene = context.scene
        bpy.ops.object.material_slot_remove_unused({
            "object": scene.objects[0],
            "selected_objects": scene.objects
        })
        return {'FINISHED'}
        #bpy.ops.object.remove_unused_materials()
##----------------------------apply wood spinter to mesh
class RemoveMaterialSlotsOperator(bpy.types.Operator):
    bl_idname = "object.remove_material_slots"
    bl_label = "Convert to Mesh"  # Initial button label

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        obj = context.object

        # Check if the first UV map is already named "UVmap01"
        if obj.data.uv_layers and obj.data.uv_layers[0].name == "UVmap01":
            self.report({'WARNING'}, " Apply mesh Done")
            return {'CANCELLED'}

        # Remove all material slots
        obj.data.materials.clear()

        # Remove all UV maps
        uv_maps = obj.data.uv_layers[:]
        for uv_map in uv_maps:
            obj.data.uv_layers.remove(uv_map)

        # Convert to mesh
        bpy.ops.object.convert(target='MESH')

        # Assign material "WoodSplinter_53AED8F6DE6FA076"
        material_name = "WoodSplinter_53AED8F6DE6FA076"
        if material_name not in bpy.data.materials:
            bpy.data.materials.new(name=material_name)
        material = bpy.data.materials[material_name]
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

        # Call the additional code
        a = obj.data.attributes
        a.active = a['UVmap01']
        bpy.ops.geometry.attribute_convert(domain='CORNER', data_type='FLOAT2')

        return {'FINISHED'}
##--------------------------auto smooth
class ShadeSmoothOperator(bpy.types.Operator):
    bl_idname = "object.shade_smooth_operator"
    bl_label = "Shade Smooth Operator"
    
    def execute(self, context):
        bpy.ops.object.shade_smooth(use_auto_smooth=True)
        return {'FINISHED'}
# ------------------------------------------Rename object selectex
class OBJECT_OT_RenameSelectedOperator(bpy.types.Operator):
    bl_idname = "object.rename_selected"
    bl_label = "Rename Selected"
    bl_description="Rename all selected models"
    def execute(self, context):
        new_name = context.scene.new_object_name  # Get the new name from the scene property
        suffix_text = context.scene.suffix_text  # Get the text from the suffix textbox

        if not new_name:  # Check if new_name is empty
            self.report({'ERROR'}, "Please enter a new object name!")
            return {'CANCELLED'}

        selected_objects = bpy.context.selected_objects

        # Rename the objects with sequential numbering and suffix
        for index, obj in enumerate(selected_objects):
            if suffix_text:  # Check if suffix_text is not empty
                obj.name = f"{new_name}{(index + 1)}_{suffix_text}"  # Append the suffix text
            else:
                obj.name = f"{new_name}{(index + 1)}"  # Use only the new name and sequential numbering

        return {'FINISHED'}
##-------------------------------For add personal material 
class SimpleOperator(Operator, ImportHelper):
    bl_idname = "object.read_meta_file"
    bl_label = "Read Meta File"
    bl_description = "Add a personal material to your list. that file is .Meta file."
    filename_ext = ".emat.meta"

    filter_glob: StringProperty(
        default="*.emat.meta",
        options={'HIDDEN'},
    )

    def execute(self, context):
        file_path = self.filepath

        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                second_line = lines[1].strip()
                match = re.search(r'{([^}]*)}', second_line)
                if match:
                    meta_content = match.group(1)
                    file_name = os.path.splitext(os.path.basename(file_path))[0]
                    first_part = file_name.split('.')[0]
                    combined_text = f"{first_part}_{meta_content}"
                    combined_text = combined_text.replace('.emat.meta', '')
                    self.report({'INFO'}, f"Added the material: {combined_text}")
                    bpy.context.scene.my_label_text = combined_text

                    ##------------------------
                    blender_version = bpy.app.version_string.split()[0]  # Get the Blender version

                    user_directory = bpy.utils.resource_path("USER")  # Get the user directory

                    addon_directory = os.path.join(user_directory, "scripts", "addons", "Opusti_Tool", "text_data")

                    output_file_path = os.path.join(addon_directory, "Collision_Mat.txt")
                    ##------------------------
                    if not self.is_text_present(output_file_path, combined_text):
                        self.insert_unique_text(output_file_path, combined_text)
                    else:
                        self.report({'WARNING'}, "Already have this material inside")

                else:
                    self.report({'ERROR'}, "No curly braces found in the second line of the meta file")
            else:
                self.report({'ERROR'}, "Invalid meta file")
#----------------------check back rows
        # Define the path to the Collision_Mat.txt file
        file_path = os.path.join(bpy.utils.user_resource('SCRIPTS'), 'addons', 'Opusti_Tool', 'text_data', 'Collision_Mat.txt')

        # Remove blank rows from the file
        def remove_blank_rows(file_path):
            # Read the contents of the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Remove blank rows
            lines = [line.strip() for line in lines if line.strip()]

            # Write the modified contents back to the file
            with open(file_path, 'w') as file:
                file.write('\n'.join(lines))

        # Call the function to remove blank rows from the file
        remove_blank_rows(file_path)
#----------------------check back rows End
        return {'FINISHED'}

    @staticmethod
    def is_text_present(file_path, text):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == text:
                    return True
        return False

    @staticmethod
    def insert_unique_text(file_path, text):
        with open(file_path, 'a+') as file:
            file.seek(0)
            lines = file.readlines()

            if lines:
                last_line = lines[-1].strip()
                if last_line:
                    file.write('\n')  # Add a new line before writing the text

            file.write(text + '\n')
class PopupDialogOperator(Operator):
    bl_idname = "object.popup_dialog"
    bl_label = "Remove the material from the list"
    bl_description = "List all of the Collision materials"

    search_text: bpy.props.StringProperty(name="Search Text", default="")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        ##------------------------
        blender_version = bpy.app.version_string.split()[0]  # Get the Blender version

        user_directory = bpy.utils.resource_path("USER")  # Get the user directory

        addon_directory = os.path.join(user_directory, "scripts", "addons", "Opusti_Tool", "text_data")

        file_path = os.path.join(addon_directory, "Collision_Mat.txt")
        ##------------------------
        row = layout.row()
        row.prop(self, "search_text")

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                num_lines = len(lines)

                for line in lines:
                    if self.search_text.lower() in line.lower():  # Filter lines based on search text
                        display_text = "_".join(line.strip().split('_')[:-1])  # Get text after the last "_"
                        row = layout.row()
                        operator = row.operator("object.remove_line", text=display_text)
                        operator.line_text = line.strip()
        except IOError:
            layout.label(text="Collision_Mat.txt not found")
class RemoveLineOperator(Operator):
    bl_idname = "object.remove_line"
    bl_label = "Remove Line"
    bl_description = "Remove this material just click"

    line_text: StringProperty()

    def execute(self, context):
        line_to_remove = self.line_text
        ##------------------------
        blender_version = bpy.app.version_string.split()[0]  # Get the Blender version

        user_directory = bpy.utils.resource_path("USER")  # Get the user directory

        addon_directory = os.path.join(user_directory, "scripts", "addons", "Opusti_Tool", "text_data")

        output_file_path = os.path.join(addon_directory, "Collision_Mat.txt")
        ##------------------------
        if self.remove_line(output_file_path, line_to_remove):
            self.report({'WARNING'}, f"The material '{line_to_remove}' has been removed")
        else:
            self.report({'INFO'}, f"Removed a material: {line_to_remove}")

        return {'FINISHED'}

    @staticmethod
    def remove_line(file_path, line):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        with open(file_path, 'w') as file:
            for current_line in lines:
                if current_line.strip() != line:
                    file.write(current_line)
        return line not in lines
##--------------For restore to temporary material 
class CopyTextToCollisionMatOperator(Operator):
    bl_idname = "object.copy_text_to_collision_mat"
    bl_label = "Copy Text to Collision_Mat"
    bl_description = "Restore to Temporary material, be careful because will replace all "

    def execute(self, context):

        blender_version = bpy.app.version_string.split()[0]  # Get the Blender version

        user_directory = bpy.utils.resource_path("USER")  # Get the user directory

        addon_directory = os.path.join(user_directory, "scripts", "addons", "Opusti_Tool", "text_data")

        temp_file_path = os.path.join(addon_directory, "Collision_Mat_Temp.txt")
        output_file_path = os.path.join(addon_directory, "Collision_Mat.txt")
        
        try:
            with open(temp_file_path, 'r') as temp_file:
                text = temp_file.read()

            with open(output_file_path, 'w') as output_file:
                output_file.write(text)

            self.report({'INFO'}, "Restore to Temporary material")
        except FileNotFoundError:
            self.report({'ERROR'}, "Temporary of the material not found")

        return {'FINISHED'}
##-------------------------------End
class FolderSelectOperator(Operator):
    bl_idname = "object.folder_select"
    bl_label = "Select Folder"

    directory: StringProperty(subtype='DIR_PATH')
    def execute(self, context):
        # Update the textbox with the selected folder location
        context.scene.my_folder_location = self.directory
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
##--------------------------------Duplicate object
def copy_and_rename_selected_models():
    selected_objects = bpy.context.selected_objects
    
    for obj in selected_objects:
        if obj.type == 'MESH':
            parent_name = obj.name
            if not parent_name.endswith(("LOD0", "LOD1", "LOD2", "LOD3", "LOD4", "LOD5", "LOD6", "LOD7", "LOD8", "LOD9", "LOD10")):
                bpy.context.window_manager.popup_menu(no_lod_suffix_message, title="Error", icon='ERROR')
                return  # Exit the function if an object is missing the "LOD" suffix or has an invalid suffix
            
            lod_index = parent_name.split('_')[-1][3:]
            new_lod_index = str(int(lod_index) + 1)
            new_name = parent_name.replace(lod_index, new_lod_index)
            new_obj = obj.copy()
            new_obj.data = obj.data.copy()
            new_obj.name = new_name
            bpy.context.collection.objects.link(new_obj)
    
    bpy.ops.object.select_all(action='DESELECT')

def no_lod_suffix_message(self, context):
    self.layout.label(text="Objects are without LOD suffix or have an invalid suffix")

class CopyAndRenameOperator(bpy.types.Operator):
    bl_idname = "object.copy_rename"
    bl_label = "Copy and Rename"
    
    def execute(self, context):
        copy_and_rename_selected_models()
        return {'FINISHED'}
#-------------------------------------------------Copy_material_to_selected
def copy_material_to_selected(self, context):
    # Get the active object (the last selected object)
    active_object = context.view_layer.objects.active
    
    if active_object is None:
        return
    
    # Get the material from the active object
    active_material = active_object.active_material
    
    if active_material is None:
        return
    
    # Iterate over all selected objects
    for obj in bpy.context.selected_objects:
        # Assign the active material to each selected object
        obj.active_material = active_material
# Define the operator class
class OBJECT_OT_copy_material_operator(bpy.types.Operator):
    bl_label = "Copy Material"
    bl_idname = "object.copy_material_operator"

    def execute(self, context):
        copy_material_to_selected(self, context)
        return {'FINISHED'}
class SimpleOperatorReopen(bpy.types.Operator):
    bl_idname = "object.auto_reopen_panel"
    bl_label = "Auto Reopen Panel"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Re-open blender, Don't worry, the program will automatically save the latest file for you."

    def execute(self, context):
        # Save the current project
        try:
            bpy.ops.wm.save_mainfile()
        except Exception as e:
            print("Error saving file:", e)
            # If saving fails, set filepath to the desired location
            filepath = "C:\\Users\\Public\\Documents\\Temp.blend"
            # Save the file to the desired location
            bpy.ops.wm.save_as_mainfile(filepath=filepath, copy=True)
        # Close Blender
        bpy.ops.wm.quit_blender()
        # Get the current file path
        filepath = bpy.data.filepath
        # Restart Blender
        if os.name == "posix":  # For Unix-based systems (Linux, macOS)
            subprocess.Popen(["blender", filepath])
        elif os.name == "nt":   # For Windows
            subprocess.Popen(["blender.exe", filepath])
        else:
            print("Unsupported operating system.")
        
        return {'FINISHED'}
    #----------------------------------------------------------------------------------------Add DayZmulti
class AddMaterialOperator(bpy.types.Operator):
    bl_idname = "object.add_dayz_material"
    bl_label = "Add DayZ Multi material"
    bl_description = "Multi material for DayZ and Arma3"
    def execute(self, context):
        material_name = "DayZ_Multi_01"
        addon_folder = "Opusti_Tool"  # Name of your addon folder
        
        # Construct the full path to the library blend file
        material_path = os.path.join(bpy.utils.user_resource('SCRIPTS'), 'addons', addon_folder, 'data', 'library.blend')
        
        # Append the material from the library blend file
        with bpy.data.libraries.load(material_path, link=False) as (data_from, data_to):
            data_to.materials = [material_name]
        
        # Apply the material to selected objects
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            if obj.type == 'MESH':
                obj.data.materials.append(bpy.data.materials[material_name])
        
        return {'FINISHED'}
#------------------------------------------------------Export DayZ
# Define a custom operator to export the active collection as FBX
class ExportActiveCollectionFBXOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "export.active_collection_fbx"
    bl_label = "Export Active Collection to FBX"

    filename_ext = ".fbx"
    filter_glob: bpy.props.StringProperty(default="*.fbx", options={'HIDDEN'})

    def execute(self, context):
        # Set the file path
        file_path = self.filepath
        
        # Call RenameObjectsInCollection operator
        bpy.ops.myaddon.rename_objects_in_collection()
        
        # Export the active collection to FBX
        bpy.ops.export_scene.fbx(
            filepath=file_path,
            path_mode='ABSOLUTE',
            check_existing=False,
            object_types={'MESH', 'OTHER', 'EMPTY', 'ARMATURE'},
            use_custom_props=True,
            bake_anim=False,
            add_leaf_bones=False,
            use_selection=False,
            use_active_collection=True,
            use_mesh_modifiers=True,
            mesh_smooth_type='EDGE',
        )

        self.report({'INFO'}, f"Exported active collection to FBX: {file_path}")
        
        # Call RemoveSuffixOperator operator
        #bpy.ops.myaddon.remove_suffix_operator()
        
        return {'FINISHED'}
#------------------------------------------------
class RemoveSuffixOperator(bpy.types.Operator):
    bl_idname = "myaddon.remove_suffix_operator"
    bl_label = "Remove Specific Suffixes from Object Names"

    def execute(self, context):
        # Get the active collection
        active_collection = bpy.context.view_layer.active_layer_collection.collection

        suffixes_to_remove = [
            "_LOD__0", "_LOD__1", "_LOD__2", "_LOD__3", "_LOD__4", "_LOD__5", "_LOD__6", "_LOD__7",
            "_LODGeometry", "_LODView_Geometry", "_LODFire_Geometry", "_LODRoadWay", "_LODMemory"
        ]

        # List of prefixes to preserve
        prefixes_to_preserve = ["Door", "door"]

        for suffix in suffixes_to_remove:
            for obj in active_collection.objects:
                # Check if the prefix should be preserved
                if any(obj.name.startswith(prefix) for prefix in prefixes_to_preserve):
                    continue  # Skip if it's a preserved prefix

                if suffix in obj.name:
                    new_name = obj.name.replace(suffix, "")
                    obj.name = new_name

        def remove_suffix_in_children(collection):
            for child_collection in collection.children:
                for suffix in suffixes_to_remove:
                    for obj in child_collection.objects:
                        # Check if the prefix should be preserved
                        if any(obj.name.startswith(prefix) for prefix in prefixes_to_preserve):
                            continue  # Skip if it's a preserved prefix

                        if suffix in obj.name:
                            new_name = obj.name.replace(suffix, "")
                            obj.name = new_name
                remove_suffix_in_children(child_collection)

        remove_suffix_in_children(active_collection)

        return {'FINISHED'}
#----------------------------
class RenameObjectsInCollection(bpy.types.Operator):
    bl_idname = "myaddon.rename_objects_in_collection"
    bl_label = "Rename Objects in Collection"

    def execute(self, context):
        # Get the active collection
        active_collection = bpy.context.view_layer.active_layer_collection.collection

        keywords_to_match = [
            "LOD__0", "LOD__1", "LOD__2", "LOD__3", "LOD__4", "LOD__5", "LOD__6", "LOD__7",
            "LODGeometry", "LODView_Geometry", "LODFire_Geometry", "LODRoadWay", "LODMemory"
        ]

        # Get the suffix from the active collection's name (if it matches any keyword)
        active_collection_suffix = None
        for keyword in keywords_to_match:
            if keyword in active_collection.name:
                active_collection_suffix = keyword
                break

        def add_suffix_to_model_name(model, suffix):
            if not suffix:
                return model.name  # No suffix to add
            if suffix.startswith("_"):
                suffix = suffix[1:]  # Remove leading underscore if present

            # Check if the model name already contains the suffix
            if suffix not in model.name:
                return f"{model.name}_{suffix}"
            else:
                return model.name  # Suffix is already present, no need to add it again

        for obj in active_collection.objects:
            if obj.type == 'MESH':
                new_name = add_suffix_to_model_name(obj, active_collection_suffix)
                obj.name = new_name

        def rename_models_in_children(collection):
            for child_collection in collection.children:
                for keyword in keywords_to_match:
                    if keyword in child_collection.name:
                        child_collection_suffix = keyword
                        break
                else:
                    child_collection_suffix = None

                for obj in child_collection.objects:
                    if obj.type == 'MESH':
                        new_name = add_suffix_to_model_name(obj, child_collection_suffix)
                        obj.name = new_name
                rename_models_in_children(child_collection)

        rename_models_in_children(active_collection)

        return {'FINISHED'}

#------------------------------Multi DayZ
class AddMaterialOperator(bpy.types.Operator):
    bl_idname = "object.add_dayz_material"
    bl_label = "Add DayZ Multi material"
    bl_description = "Multi material for DayZ and Arma3"
    def execute(self, context):
        material_name = "DayZ_Multi_01"
        addon_folder = "Opusti_Tool"  # Name of your addon folder
        
        # Construct the full path to the library blend file
        material_path = os.path.join(bpy.utils.user_resource('SCRIPTS'), 'addons', addon_folder, 'data', 'library.blend')
        
        # Append the material from the library blend file
        with bpy.data.libraries.load(material_path, link=False) as (data_from, data_to):
            data_to.materials = [material_name]
        
        # Apply the material to selected objects
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            if obj.type == 'MESH':
                obj.data.materials.append(bpy.data.materials[material_name])
        
        return {'FINISHED'}
#------------------------------Super DayZ
class AddMaterialOperatorSuper(bpy.types.Operator):
    bl_idname = "object.add_dayz_materialsuper"
    bl_label = "Add DayZ Super material"
    bl_description = "Super material for DayZ and Arma3"
    def execute(self, context):
        material_name = "DayZ_Super_01"
        addon_folder = "Opusti_Tool"  # Name of your addon folder
        
        # Construct the full path to the library blend file
        material_path = os.path.join(bpy.utils.user_resource('SCRIPTS'), 'addons', addon_folder, 'data', 'library.blend')
        
        # Append the material from the library blend file
        with bpy.data.libraries.load(material_path, link=False) as (data_from, data_to):
            data_to.materials = [material_name]
        
        # Apply the material to selected objects
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            if obj.type == 'MESH':
                obj.data.materials.append(bpy.data.materials[material_name])
        
        return {'FINISHED'}
    #------------------------------Super CA DayZ
class AddMaterialOperatorSuperCA(bpy.types.Operator):
    bl_idname = "object.add_dayz_materialsuperca"
    bl_label = "Add DayZ Super CA material"
    bl_description = "Super CA material for DayZ and Arma3"
    def execute(self, context):
        material_name = "DayZ_Super_CA"
        addon_folder = "Opusti_Tool"  # Name of your addon folder
        
        # Construct the full path to the library blend file
        material_path = os.path.join(bpy.utils.user_resource('SCRIPTS'), 'addons', addon_folder, 'data', 'library.blend')
        
        # Append the material from the library blend file
        with bpy.data.libraries.load(material_path, link=False) as (data_from, data_to):
            data_to.materials = [material_name]
        
        # Apply the material to selected objects
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            if obj.type == 'MESH':
                obj.data.materials.append(bpy.data.materials[material_name])
        
        return {'FINISHED'}
    #---------------------------------DayZ Run EXE tool
class RunEXEtoolsDayZ(bpy.types.Operator):
    bl_idname = "wm.run_exe_tools_dayz"
    bl_label = "Run EXE Tools for DayZ"
    bl_options = {'REGISTER'}
    bl_description="Launch DayZ Client and manage rvmat materials"
    def execute(self, context):
        # Get the Blender add-ons directory
        addons_dir = bpy.utils.resource_path('USER') + "/scripts/addons/"

        # Construct the path to the .exe file within the add-ons directory
        exe_file_path = os.path.join(addons_dir, "Opusti_Tool", "data", "Oputi Tools.exe")

        try:
            # Check if the file exists
            if os.path.exists(exe_file_path):
                # Open the .exe file using subprocess
                subprocess.Popen(exe_file_path, shell=True)
                self.report({'INFO'}, f"Opened {exe_file_path}")
            else:
                self.report({'ERROR'}, f"File {exe_file_path} does not exist.")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to open {exe_file_path}: {str(e)}")

        return {'FINISHED'}
    #---------------------------------------Sort Objects
class OrganizeObjectsOperator(bpy.types.Operator):
    bl_idname = "object.organize_objects"
    bl_label = "Organize Objects"

    def execute(self, context):
        # Get the currently active collection
        active_collection = context.collection

        # List of keywords to search for in model names
        keywords = ["LOD__0", "LOD__1", "LOD__2", "LOD__3", "LOD__4", "LOD__5",
                    "LOD__6", "LOD__7", "proxy", "LODView_Geometry", "LODFire_Geometry", "LODRoadWay", "LODGeometry", "LODMemory"]

        # Get the prefix from the scene property
        prefix = context.scene.my_prefix

        # Iterate through objects in the active collection
        for obj in active_collection.objects:
            for keyword in keywords:
                # If the keyword is found in the object name
                if keyword in obj.name:
                    # Check if the collection already exists
                    collection_name = f"{prefix}_{keyword}" if prefix else keyword
                    if collection_name in bpy.context.collection.children:
                        keyword_collection = bpy.context.collection.children[collection_name]
                        self.report({'INFO'}, f"Model {obj.name} is already in the correct collection.")
                    else:
                        # Check if the object is already in the correct collection
                        in_correct_collection = False
                        for collection in obj.users_collection:
                            if collection.name == collection_name:
                                in_correct_collection = True
                                break
                        
                        if not in_correct_collection:
                            # Create the collection if it doesn't exist and the object is not in the correct collection
                            keyword_collection = bpy.data.collections.new(collection_name)
                            bpy.context.collection.children.link(keyword_collection)
                        else:
                            self.report({'INFO'}, f"Model {obj.name} is already in the correct collection.")

                    # Link the object to the collection and remove it from the active collection
                    keyword_collection.objects.link(obj)
                    active_collection.objects.unlink(obj)

        return {'FINISHED'}
#---------------------------------------SmartDuplicateObjectsOperator
class SmartDuplicateObjectsOperator(bpy.types.Operator):
    bl_idname = "object.smart_duplicate_objects"
    bl_label = "Smart Duplicate Objects"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        newly_copied_objects = []

        for obj in selected_objects:
            if obj.type == 'MESH':
                # Create a copy of the selected object
                obj_copy = obj.copy()
                obj_copy.data = obj.data.copy()
                bpy.context.scene.collection.objects.link(obj_copy)

                # Rename the copied object with an incremented suffix
                obj_name = obj.name
                parts = obj_name.split('_')
                if len(parts) >= 3 and parts[-1].isdigit():
                    new_suffix = str(int(parts[-1]) + 1)
                    new_name = "_".join(parts[:-1] + [new_suffix])
                    obj_copy.name = new_name

                newly_copied_objects.append(obj_copy)

        # Clear the current selection and select the newly copied objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in newly_copied_objects:
            obj.select_set(True)
        FixSuffixNamesOperator(self, context)
        EmptyOperator(self, context)
        # Call an empty operator to do nothing (placeholder)

        return {'FINISHED'}

def FixSuffixNamesOperator(self, context):
    selected_objects = bpy.context.selected_objects
    for obj in selected_objects:
        if obj.type == 'MESH':
            # Split the object name by the dot ('.') character
            obj_name = obj.name
            parts = obj_name.rsplit('.', 1)  # Split only at the last dot
                
            if len(parts) == 2:
                name_part, suffix_part = parts
                    
                # Check if the suffix_part is a number in the range .001-.999
                if suffix_part[1:].isdigit() and 1 <= int(suffix_part[1:]) <= 999:
                    name_parts = name_part.rsplit('_', 1)
                    if len(name_parts) == 2 and name_parts[1].startswith("LOD") and name_parts[1][3:].isdigit():
                        lod_suffix = int(name_parts[1][3:])
                        if 0 <= lod_suffix <= 9:
                            new_lod_suffix = lod_suffix + 1
                            new_name = f"{name_parts[0]}_LOD{new_lod_suffix}.{parts[1]}"
                            obj.name = new_name
                        else:
                            new_name = f"{name_parts[0]}.{parts[1]}"
                            obj.name = new_name
                    else:
                        new_name = f"{name_part}.{parts[1]}"
                        obj.name = new_name

def EmptyOperator(self, context):
    selected_objects = bpy.context.selected_objects

    for obj in selected_objects:
        if obj.type == 'MESH':
            # Split the object name by the dot ('.') character
            obj_name = obj.name
            parts = obj_name.rsplit('.', 1)  # Split only at the last dot
                
            if len(parts) == 2:
                name_part, suffix_part = parts
                    
                # Check if the suffix_part is a number in the range .001-.999
                if suffix_part[1:].isdigit() and 1 <= int(suffix_part[1:]) <= 999:
                    new_name = name_part
                    obj.name = new_name

#------------------------- Clear normals pro for DayZ
class ClearNormalsProForDayZ(bpy.types.Operator):
    bl_idname = "object.clear_normal_pro"
    bl_label = "Clear Normal Pro"
    bl_description = "Clear normal for DayZ : set auto smooth 180 and work for multi selection models"
    def execute(self, context):
        clear_normal()
        return {'FINISHED'}
class GetSharpFormAutoSmooth(bpy.types.Operator):
    bl_idname = "object.get_sharp_pro"
    bl_label = "Get Sharp Pro"
    bl_description = "Get sharp from auto smooth and set Auto smooth to 180 for multi selection models"
    def execute(self, context):
        Get_sharpFromAuto()
        return {'FINISHED'}
def clear_normal():
    selection = bpy.context.selected_objects
    for o in selection:
        try:
            #----Clear Normal
            bpy.context.view_layer.objects.active = o
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            #----Reset All
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.transforms_to_deltas(mode='ALL')
            bpy.ops.object.visual_transform_apply()
            bpy.ops.object.convert(target='MESH')
            #----smooth
            bpy.ops.object.shade_smooth(use_auto_smooth=True)

        except:
            print("Object has no custom split normals: " + o.name + ", skipping") 
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            obj.data.auto_smooth_angle = 3.14159
    return {'FINISHED'}

def Get_sharpFromAuto():
    selection = bpy.context.selected_objects
    for o in selection:
        try:
            bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
            bpy.context.object.modifiers["WeightedNormal"].keep_sharp = True  
            #----Reset All
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.transforms_to_deltas(mode='ALL')
            bpy.ops.object.visual_transform_apply()
            bpy.ops.object.convert(target='MESH')
            #----Clear Normal
            bpy.context.view_layer.objects.active = o
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            #----smooth
            bpy.ops.object.shade_smooth(use_auto_smooth=True)
        except:
            print("Object has no custom split normals: " + o.name + ", skipping") 
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            obj.data.auto_smooth_angle = 3.14159
    return {'FINISHED'}
#-------------------------------------------------------------Preset Exporter for Painter
class CopyFilePresetExportPainter(bpy.types.Operator):
    bl_label = "Copy Files"
    bl_idname = "wm.copy_file_preset_export_painter_operator"
    bl_description="Install the exporter python for substance painter, then one the painter go to Python> Export you will see them"
    def execute(self, context):
        blender_version = bpy.app.version

        # Define source and destination paths for File 1 and File 2
        blender_version_str = f"{blender_version[0]}.{blender_version[1]}"
        file1_source = os.path.expanduser(f"~\\AppData\\Roaming\\Blender Foundation\\Blender\\{blender_version_str}\\scripts\\addons\\Opusti_Tool\\etc\\Export.py")
        file1_destination = os.path.expanduser("~\\Documents\\Adobe\\Adobe Substance 3D Painter\\python\\plugins\\Export.py")

        file2_source = os.path.expanduser(f"~\\AppData\\Roaming\\Blender Foundation\\Blender\\{blender_version_str}\\scripts\\addons\\Opusti_Tool\\etc\\A4.spexp")
        file2_destination = os.path.expanduser("~\\Documents\\Adobe\\Adobe Substance 3D Painter\\assets\\export-presets\\A4.spexp")

        # Copy files
        shutil.copyfile(file1_source, file1_destination)
        shutil.copyfile(file2_source, file2_destination)

        self.report({'INFO'}, "Files copied successfully")
        return {'FINISHED'}

