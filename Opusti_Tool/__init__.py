bl_info = {
    "name": "Oputi Tools",
    "author": "By Sunny",
    "version": (0, 9, 9),
    "blender": (3, 6, 0),
    "location": "VIEW_3D",
    "description": "Addon is free. Donations for script development via Payoneer (komsansmilenmd@gmail.com)",
    "warning": "",
    "wiki_url": "",
    "category": "3D View",
}
import statistics
import subprocess
import threading
import bpy
import sys
from bpy_extras.io_utils import ExportHelper
from bpy.props import EnumProperty
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class 
import random
import bmesh
from mathutils import Vector, Matrix
from bpy.types import Menu, Operator
import re
from . import Opus_Normal
from . import Opus_ui
from . import Opus_Utility
from . import Opus_PieMenu
from . import Opus_Update
from . import Opus_ComboPanel
import mathutils
import os
import shutil
import bpy.utils.previews
from bpy.types import Panel
from bpy.types import Scene
from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)
import bpy.types
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
from . import RvmatToBlender
from . import UptoDate
import datetime

UptoDate.main_download()
#---------------------------------------------------------------------------------------------------Collision Material   
class MyMaterial(bpy.types.PropertyGroup):
    def get_items(self, context):
        addon_directory = os.path.dirname(os.path.realpath(__file__))
        file_path = "Collision_Mat.txt"
        file_location = os.path.join(addon_directory, "text_data", file_path)
        #file_location = os.path.join("C:/Users/komsa/AppData/Roaming/Blender Foundation/Blender/3.5/scripts/addons/Opusti_Tool/text_data/", file_path)

        # Use the file_location variable in your code
        with open(file_location, "r") as file:
            lines = file.readlines()

        items = []
        for line in lines:
            line = line.strip()
            material_name = "_".join(line.split('_')[:-1])
            display_name = material_name
            items.append((line, display_name, line))

        return items

    my_enum_M: bpy.props.EnumProperty(
        name="Type",
        description="Material preset",
        items=get_items
    )
class Material_OT_my_op(bpy.types.Operator):
    bl_label = "Assign"
    bl_idname = "material.myop_operator"
    bl_description="Assign the selected material to all selected models."
    def execute(self, context):
        scene = context.scene
        mymaterial = scene.my_material

        if mymaterial.my_enum_M == mymaterial.my_enum_M:
            bpy.ops.object.material_slot_remove()
            ob = bpy.context.active_object

            # Get material
            mat = bpy.data.materials.get(mymaterial.my_enum_M)
            if mat is None:
                # Create material
                mat = bpy.data.materials.new(name=mymaterial.my_enum_M)

            # Assign it to object
            if ob.data.materials:
                # Assign to 1st material slot
                ob.data.materials[0] = mat
            else:
                # No slots
                ob.data.materials.append(mat)

            print(mymaterial.my_enum_M)
        bpy.ops.object.random_diffuse_color_operator()
        bpy.ops.object.copy_material_operator()
        return {'FINISHED'} 
##--------------------Random color of the material collider
# Define the operator class
class RandomDiffuseColorOperator(bpy.types.Operator):
    bl_label = "Random Diffuse Color"
    bl_idname = "object.random_diffuse_color_operator"

    def execute(self, context):
        # Get the active object
        active_object = bpy.context.active_object

        # Check if the active object has a material
        if active_object and active_object.material_slots:
            material_slot = active_object.material_slots[0]
            material = material_slot.material
            if material:
                # Generate a random color
                color = (random.random(), random.random(), random.random(), 1.0)

                # Set the material's diffuse color
                material.use_nodes = False  # Disable node-based material
                material.diffuse_color = color

        return {'FINISHED'}
#---------------------------------------------------------------------------------------------------Collision Preset   
class MyProperties(bpy.types.PropertyGroup):
    def get_items(self, context):
        addon_directory = os.path.dirname(os.path.realpath(__file__))
        file_path = "Collision_Preset.txt"
        file_location = os.path.join(addon_directory, "text_data", file_path)

        # Use the file_location variable in your code
        with open(file_location, "r") as file:
            lines = file.readlines()
            
        items = []
        for line in lines:
            line = line.strip()
            items.append((line, line, ""))
        return items

    my_enum: bpy.props.EnumProperty(
        name="Usage",
        description="Layer preset",
        items=get_items
    )
class ADDONNAME_OT_my_op(bpy.types.Operator):
    bl_label = "Assign"
    bl_idname = "addonname.myop_operator"
    bl_description ="Assign LayerPresets to the selected models."
    def execute(self, context):
        obj = bpy.context.object
        # Check if the object is valid and has custom properties
        if obj and obj.type == 'MESH' and obj.keys():
            # Create a copy of the custom property names
            custom_props = list(obj.keys())
            # Delete all custom properties
            for prop_name in custom_props:
                del obj[prop_name]
                print("Deleted custom property:", prop_name)
        else:
            print("No valid object selected or object has no custom properties.")

        scene = context.scene
        mytool = scene.my_tool
        
        if mytool.my_enum == mytool.my_enum:
            
            for object in context.selected_objects:
                object["usage"] = (mytool.my_enum)
        return {'FINISHED'} 
#---------------------------------------------------------------------------------------------------Normal Item    
#---------------------------------------------------------------------------------------------------LODs Preset   
class ListLODs(bpy.types.PropertyGroup):
    ListLODs_enum : bpy.props.EnumProperty(
        name= "",
        description= "sample text",
        items= [('50', "50", ""),
				('25', "25", ""),
                ('10', "10", ""),
        ]
    )
class ListLODs_OT_my_op(bpy.types.Operator):
    bl_label = "Assign"
    bl_idname = "ListLODs.myop_operator"

    def execute(self, context):
        scene = context.scene
        ListLODs = scene.myList_tool
        
        return {'FINISHED'} 
#-------------------------------
def validate_number_input(input_string):
    pattern = r'^[0-9]*\.?[0-9]*$'  # Regular expression pattern for numbers
    return re.match(pattern, input_string) is not None

def process_number_input(self, context):
    if not validate_number_input(self.my_number):
        self.my_number = "50"  # Clear the input if it's not a valid number

class OpustiStatusProperties(bpy.types.PropertyGroup):
    my_number: bpy.props.StringProperty(
        name="",
        default="50",
        description="Enter a number.",
        update=process_number_input  # Add an update callback to validate the input
    )
class MyToolOperator(bpy.types.Operator):
    bl_idname = "object.my_tool_operator"
    bl_label = "My Tool Operator"
    bl_description="will calculate by taking the number you filled and dividing it by the number of polygons of the currently opened model."
    def execute(self, context):
        scene = context.scene
        my_tool = scene.opusti_status

        getLODs = my_tool.my_number
        int_value = int(getLODs)
        lodResult = int_value * 0.01

        s = bpy.context.scene.statistics(bpy.context.view_layer)
        tris = int(s.split("Tris:")[1].split(' ')[0].replace(',', '')) 
        
        converted_num_0 = f'{"{:,}".format(int(tris))}'
        converted_num_1 = f'{"{:,}".format(int(tris)*lodResult)}'

        bpy.context.scene.my_label_text0 = converted_num_0
        bpy.context.scene.my_label_text1 = converted_num_1
        print("how many reduce:", lodResult)
        return {'FINISHED'}
bpy.types.Scene.my_label_text0 = bpy.props.StringProperty(default="00")
bpy.types.Scene.my_label_text1 = bpy.props.StringProperty(default="00")
class WireframeToggleAddon(bpy.types.Operator):
    bl_idname = "view3d.wireframe_toggle"
    bl_label = "Toggle Wireframe"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'VIEW_3D'

    def execute(self, context):
        # Get the active object
        obj = context.active_object
        if obj is not None:
            # Toggle wireframe display mode
            obj.display_type = 'WIRE' if obj.display_type != 'WIRE' else 'SOLID'
        
        return {'FINISHED'}
class WireframeToggleAddons(bpy.types.Operator):
    bl_idname = "view3d.wireframe_toggles"
    bl_label = "Toggle Overlay Wireframe"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'VIEW_3D'

    def execute(self, context):
        # Toggle overlay wireframe display mode
        context.space_data.overlay.show_wireframes = not context.space_data.overlay.show_wireframes
        
        return {'FINISHED'}

class ToggleFaceOrientationAddon(bpy.types.Operator):
    bl_idname = "wm.toggle_face_orientation"
    bl_label = "Toggle Face Orientation"
    bl_options = {'REGISTER'}

    def execute(self, context):
        space_data = context.space_data
        space_data.overlay.show_face_orientation = not space_data.overlay.show_face_orientation
        return {'FINISHED'}
class CreateToggleTransformOrientationOperator(bpy.types.Operator):
    bl_idname = "object.create_toggle_transform_orientation"
    bl_label = "Create Toggle Transform Orientation"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description="Gizmo will snap according to the angle of the selected face or edge."
    
    toggle_property: bpy.props.BoolProperty(default=False)
    
    def execute(self, context):
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
   
        return {'FINISHED'}
class MyOperator1(bpy.types.Operator):
    bl_idname = "my_operator.button1"
    bl_label = "Toggle 1"
    is_enabled = False
    bl_description="Gizmo will return to the default angle according to the Viewport."

    def execute(self, context):

        active_orientation = bpy.context.scene.transform_orientation_slots[0].type
        if active_orientation != 'GLOBAL' and len(bpy.context.scene.transform_orientation_slots) > 0:
            bpy.ops.object.delete_all_transform_orientation()
        try:
            bpy.context.scene.transform_orientation_slots[0].type = 'Face'
            bpy.ops.transform.delete_orientation()
            bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'
        except:
            bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'

        MyOperator1.is_enabled = not MyOperator1.is_enabled

        return {'FINISHED'}
# Set the initial values for Auto Merge and Threshold distance
def set_initial_values():
    bpy.context.scene.tool_settings.use_mesh_automerge = True
    bpy.context.scene.tool_settings.double_threshold = 0.001
##-----------------------------------------------------------------------------Fix materail suffixes .001--
def Removed_Useless_materials():
    # Save the current active object
    active_object = bpy.context.view_layer.objects.active
    
    # Select all objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    
    # Set the active object to the last selected object
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
    
    # Remove unused materials
    bpy.ops.object.material_slot_remove_unused()
    
    # Restore the original active object
    bpy.context.view_layer.objects.active = active_object

    # Remove unused data blocks
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)

    return {'FINISHED'}
def fix_copied_materials():
    # Get a list of all materials in the scene
    all_materials = bpy.data.materials

    # Create a dictionary to store the original materials
    original_materials = {}

    # Iterate over each material
    for material in all_materials:
        # Check if the material name has a suffix between .001 and .010
        for i in range(1, 99):
            suffix = ".{:03d}".format(i)
            if material.name.endswith(suffix):
                # Extract the original material name
                original_name = material.name[:-4]

                # If the original material is not already stored, add it to the dictionary
                if original_name not in original_materials:
                    original_materials[original_name] = material

    # Replace the copied materials
    for original_name, material in original_materials.items():
        # Check if the material without suffixes exists
        if original_name in bpy.data.materials:
            # Replace the copied materials in all objects
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    # Iterate over each material slot in the object
                    for slot in obj.material_slots:
                        # Check if the slot's material name has a suffix between .001 and .010
                        for i in range(1, 99):
                            suffix = ".{:03d}".format(i)
                            if slot.name.endswith(suffix):
                                # Extract the original material name
                                if slot.material == material:
                                    slot.material = bpy.data.materials[original_name]
        else:
            print("Done")
    # Remove unused materials
    bpy.ops.outliner.orphans_purge(do_local_ids=True)

class FixCopiedMaterialsOperator(bpy.types.Operator):
    bl_idname = "object.fix_copied_materials"
    bl_label = "Fix Copied Materials"
    bl_description = "Fixes copied materials by replacing them with the original materials"

    def execute(self, context):
        for _ in range(6):
            fix_copied_materials()
        Removed_Useless_materials()
        return {'FINISHED'}
##-----------------------------------------------------------------------------Done 
##----------------------------------------------------Reset tranform
class ApplyTransformsOperator(bpy.types.Operator):
    bl_idname = "object.apply_transforms"
    bl_label = "Apply Transforms"
    bl_description="Reset the origin to the center of each model."
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            bpy.context.view_layer.objects.active = obj
            
            # Move origin to geometry center
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            
            # Apply transforms
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.transforms_to_deltas(mode='ALL')
            bpy.ops.object.visual_transform_apply()
            bpy.ops.object.convert(target='MESH')
            #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
        bpy.ops.transform.transform(mode='ALIGN')
        return {'FINISHED'}
class DeleteAllTransformOrientationOperator(bpy.types.Operator):
    bl_idname = "object.delete_all_transform_orientation"
    bl_label = "Delete All Transform Orientation"
    bl_options = {'REGISTER', 'UNDO'}

    enabled: bpy.props.BoolProperty(default=True)
    def execute(self, context):
        orientation_slots = bpy.context.scene.transform_orientation_slots
        if orientation_slots:
            bpy.ops.transform.delete_orientation()
        return {'FINISHED'}
##--------------Collision generate
class OBJECT_OT_CreateBoxMatchDimensionsRotationMoveOperator(bpy.types.Operator):
    bl_idname = "object.create_box_match_dimensions_rotation_move_operator"
    bl_label = "Create Box, Match Dimensions, Rotation, and Move"
    
    def execute(self, context):
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
        
        return {'FINISHED'}
##-----------------------------Collision list
##----------------------------------update material Enfusion
# Specify the initial folder path
base_folder_path = r"E:\ArmaReforgerData"
relative_folder_path = r"\Common\Materials\Game"
folder_path = base_folder_path + relative_folder_path

# Define custom material property group
class CustomMaterial(bpy.types.PropertyGroup):
    def get_items(self, context):
        items = []

        # Recursive function to traverse folders and process .meta files
        def traverse_folders(folder):
            for root, dirs, files in os.walk(folder):
                for file_name in files:
                    if file_name.endswith(".meta"):
                        file_path = os.path.join(root, file_name)

                        # Open the file and read only the second line
                        with open(file_path, 'r') as file:
                            file_content = file.readlines()

                        if len(file_content) >= 2:
                            # Extract the text within the first pair of curly braces {}
                            match = re.search(r'\{(.*?)\}', file_content[1], re.DOTALL)
                            extracted_text = match.group(1) if match else ""
                        else:
                            extracted_text = ""

                        # Format the file name and extracted text
                        formatted_name = file_name.replace(".meta", "").replace(".gamemat", "")
                        formatted_text = "{}_{}".format(formatted_name, extracted_text)

                        # Add the formatted text to the items list if it's not already present
                        if formatted_text not in items:
                            items.append(formatted_text)

                for subfolder in dirs:
                    subfolder_path = os.path.join(root, subfolder)
                    traverse_folders(subfolder_path)

        # Start traversal from the main folder
        traverse_folders(folder_path)

        return items
class SaveTextDataOperator(bpy.types.Operator):
    bl_label = "Update Material from Enfusion"
    bl_idname = "text_data.save_operator"
    bl_description = "Please put the location of your project SVN of the Arma Reforger this button will update all material"

    def execute(self, context):
        scene = context.scene
        custom_material = scene.custom_material

        # Update the folder path based on the base folder path input
        folder_path = scene.base_folder_path + relative_folder_path

        # Check if the folder path exists
        if os.path.exists(folder_path):
            # Get the unique text items
            unique_text_items = custom_material.get_items(context)

            # Sort the text data
            sorted_text = sorted(unique_text_items)

            # Create a string with each line of the sorted text
            text_content = '\n'.join(sorted_text)

            # Get the user's home directory
            version = bpy.app.version_string.split(' ')[0]  # Extract the version without additional info
            version = version.rsplit('.', 1)[0]  # Remove decimal point and trailing zeros
            directory = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Blender Foundation", "Blender", version, "scripts", "addons", "Opusti_Tool", "text_data")
            save_path = os.path.join(directory, "Collision_Mat.txt")
                ##---------------------------------------------End
            # Save the text data to a file
            with open(save_path, 'w') as file:
                file.write(text_content)

            self.report({'INFO'}, "Text data saved to {}".format(save_path))
            self.report({'INFO'}, "Updated last material from Enfusion")
        else:
            self.report({'ERROR'},
                        "Patch file incorrect should be the main project from SVN of the Arma Reforger for Example E:\ArmaReforgerData")

        return {'FINISHED'} 
##-------------------------------------------------------------------DayZ
# Add a new operator to handle file selection
class CustomSelectTGAOperator(bpy.types.Operator):
    bl_idname = "custom.select_tga"
    bl_label = "Select TGA File"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        context.scene.custom_text_box = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        pass
# Function to get a list of RVMAT files in a directory
def get_rvmat_files(directory):
    rvmat_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".rvmat"):
            rvmat_files.append((filename, filename, ""))
    return rvmat_files

class CreateAssignMaterialOperator(bpy.types.Operator):
    bl_idname = "custom.create_assign_material"
    bl_label = "Create and Assign Material"
    bl_description=" Assign Fire geometry to selected models"
    def execute(self, context):
        scene = context.scene
        selected_rvmat = scene.custom_rvmat_list
        
        bpy.ops.custom.delete_material_slots()
        
        if not selected_rvmat:
            self.report({'ERROR'}, "No material selected from the dropdown menu.")
            return {'CANCELLED'}

        rvmat_directory = "P:\\dz\\data\\data\\penetration"  # Replace with your directory path
        rvmat_path = os.path.join(rvmat_directory, selected_rvmat)

        # Extract the base name of the selected .rvmat file (excluding the extension)
        texture_node_name = os.path.splitext(os.path.basename(selected_rvmat))[0]

        # Declare the texture_node variable outside of the conditional block
        texture_node = None

        # Check if a material with the same name already exists in the scene
        existing_material = bpy.data.materials.get(texture_node_name)

        if existing_material:
            # Material with the same name exists, reuse it
            new_material = existing_material
        else:
            # Create a new material
            new_material = bpy.data.materials.new(name=texture_node_name)

            # Check if the material has a shader node tree, create one if not
            if new_material.node_tree is None:
                new_material.use_nodes = True

            # Get the Principled BSDF node
            bsdf_node = None
            for node in new_material.node_tree.nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    bsdf_node = node
                    break

            # Create an image texture node
            texture_node = new_material.node_tree.nodes.new(type='ShaderNodeTexImage')

            # Set the name of the texture node to match the base name of the .rvmat file
            texture_node.name = texture_node_name

            # Set the image path for the texture node
            image_path = os.path.join(rvmat_directory, selected_rvmat)  # Add the directory path
            texture_node.image = bpy.data.images.load(image_path)

            # Connect the texture node to the Base Color input of the Principled BSDF node
            links = new_material.node_tree.links
            bsdf_node_input = bsdf_node.inputs["Base Color"]
            texture_node_output = texture_node.outputs["Color"]
            links.new(bsdf_node_input, texture_node_output)

        # Assign the material to the selected objects
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            if obj.type == 'MESH':
                # Check if the material already exists in the object's material slots
                existing_slot = None
                for index, slot in enumerate(obj.material_slots):
                    if slot.material.name == new_material.name:
                        existing_slot = index
                        break

                if existing_slot is not None:
                    # Material with the same name already exists in the object's slots
                    # Use the existing slot
                    obj.material_slots[existing_slot].material = new_material
                else:
                    # Add the new material to the object's material slots
                    obj.active_material = new_material

        if texture_node and texture_node.image:
            EmtyColl = " "
            texture_node.image.name = os.path.join(rvmat_directory, selected_rvmat)
            texture_node.image.filepath = EmtyColl

        return {'FINISHED'}
#-----------------------------------------------
# Function to get a list of TGA files in a directory
def get_tga_files(directory):
    tga_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".tga"):
            tga_files.append((filename, filename, ""))
    return tga_files

class CreateAssignTGAMaterialOperator(bpy.types.Operator):
    bl_idname = "custom.create_assign_tga_material"
    bl_label = "Create and Assign TGA Material"
    bl_description="Assign the roadway to selection models"
    def execute(self, context):
        scene = context.scene
        selected_tga = scene.custom_tga_list
        
        bpy.ops.custom.delete_material_slots()
        
        if not selected_tga:
            self.report({'ERROR'}, "No material selected from the dropdown menu.")
            return {'CANCELLED'}

        tga_directory = "P:\\dz\\surfaces\\data\\roadway"  # Updated directory path for .tga files
        tga_path = os.path.join(tga_directory, selected_tga)

        # Extract the base name of the selected .tga file (excluding the extension)
        texture_node_name = os.path.splitext(os.path.basename(selected_tga))[0]

        # Declare the texture_node variable outside of the conditional block
        texture_node = None

        # Check if a material with the same name already exists in the scene
        existing_material = bpy.data.materials.get(texture_node_name)

        if existing_material:
            # Material with the same name exists, reuse it
            new_material = existing_material
        else:
            # Create a new material
            new_material = bpy.data.materials.new(name=texture_node_name)

            # Check if the material has a shader node tree, create one if not
            if new_material.node_tree is None:
                new_material.use_nodes = True

            # Get the Principled BSDF node
            bsdf_node = None
            for node in new_material.node_tree.nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    bsdf_node = node
                    break

            # Create an image texture node
            texture_node = new_material.node_tree.nodes.new(type='ShaderNodeTexImage')

            # Set the name of the texture node to match the base name of the .tga file
            texture_node.name = texture_node_name

            # Set the image path for the texture node
            image_path = os.path.join(tga_directory, selected_tga)  # Add the directory path
            texture_node.image = bpy.data.images.load(image_path)

            # Connect the texture node to the Base Color input of the Principled BSDF node
            links = new_material.node_tree.links
            bsdf_node_input = bsdf_node.inputs["Base Color"]
            texture_node_output = texture_node.outputs["Color"]
            links.new(bsdf_node_input, texture_node_output)

        # Assign the material to the selected objects
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            if obj.type == 'MESH':
                # Check if the material already exists in the object's material slots
                existing_slot = None
                for index, slot in enumerate(obj.material_slots):
                    if slot.material.name == new_material.name:
                        existing_slot = index
                        break

                if existing_slot is not None:
                    # Material with the same name already exists in the object's slots
                    # Use the existing slot
                    obj.material_slots[existing_slot].material = new_material
                else:
                    # Add the new material to the object's material slots
                    bpy.ops.object.material_slot_add()
                    obj.active_material = new_material

        #if texture_node and texture_node.image:
            #texture_node.image.name = os.path.join(tga_directory, selected_tga)
            #texture_node.image.filepath = "   "

        return {'FINISHED'}
# Add a StringProperty for the custom directory path
bpy.types.Scene.custom_directory_path = bpy.props.StringProperty(
    name="Directory Path",
    description="Enter the directory path to read .rvmat files from and save to SaveRvmat.txt",
    default="",  # You can set a default directory path here
)

class ReadRvmatNamesAndSaveOperator(bpy.types.Operator):
    bl_idname = "custom.read_rvmat_names_and_save"
    bl_label = "Read .rvmat Names and Save"
    bl_description="Save and update your last Path file"
    def execute(self, context):
        custom_directory_path = context.scene.custom_directory_path
        if not custom_directory_path:
            self.report({'ERROR'}, "Please enter a directory path.")
            return {'CANCELLED'}

        # Save the custom_directory_path to SaveRvmat.txt
        save_path = os.path.join("C:\\Users\\Public\\Downloads", "SaveRvmat.txt")
        with open(save_path, 'w') as file:
            file.write(custom_directory_path)

        self.report({'INFO'}, f"Saved directory path to SaveRvmat.txt")
        return {'FINISHED'}
#------
class CreateAssignMaterialFromDropdownOperator(bpy.types.Operator):
    bl_idname = "custom.create_assign_material_from_dropdown"
    bl_label = "Create and Assign Material from Dropdown"
    bl_description="After assigning this rvmat, when we export it to the Object Builder program, it will automatically link the rvmat. Additionally, there is a Path field above for the Super material; if it's multi, just leave it empty."
    def execute(self, context):
        scene = context.scene
        selected_rvmat = scene.custom_new_menu_list
        bpy.ops.custom.delete_material_slots()
        if not selected_rvmat:
            self.report({'ERROR'}, "No material selected from the dropdown menu.")
            return {'CANCELLED'}

        rvmat_directory = scene.custom_directory_path
        rvmat_path = os.path.join(rvmat_directory, selected_rvmat)

        # Extract the base name of the selected .rvmat file (excluding the extension)
        texture_node_name = os.path.splitext(os.path.basename(selected_rvmat))[0]

        # Append ".rvmat" to the texture_node_name
        texture_node_name += ".rvmat"

        # Declare the texture_node variable outside of the conditional block
        texture_node = None

        # Check if a material with the same name already exists in the scene
        existing_material = bpy.data.materials.get(texture_node_name)

        if existing_material:
            # Material with the same name exists, replace the current material with it
            selected_objects = bpy.context.selected_objects
            for obj in selected_objects:
                if obj.type == 'MESH':
                    obj.data.materials.clear()
                    obj.data.materials.append(existing_material)
        else:
            # Create a new material
            new_material = bpy.data.materials.new(name=texture_node_name)

            # Check if the material has a shader node tree, create one if not
            if new_material.node_tree is None:
                new_material.use_nodes = True

            # Get the Principled BSDF node
            bsdf_node = None
            for node in new_material.node_tree.nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    bsdf_node = node
                    break

            # Create an image texture node
            texture_node = new_material.node_tree.nodes.new(type='ShaderNodeTexImage')

            # Set the name of the texture node to match the base name of the .rvmat file
            texture_node.name = texture_node_name

            # Set the image path for the texture node
            image_path = os.path.join(rvmat_directory, selected_rvmat)  # Add the directory path
            texture_node.image = bpy.data.images.load(image_path)

            # Connect the texture node to the Base Color input of the Principled BSDF node
            links = new_material.node_tree.links
            bsdf_node_input = bsdf_node.inputs["Base Color"]
            texture_node_output = texture_node.outputs["Color"]
            links.new(bsdf_node_input, texture_node_output)

            # Assign the new material to the selected objects
            selected_objects = bpy.context.selected_objects
            for obj in selected_objects:
                if obj.type == 'MESH':
                    obj.data.materials.clear()
                    obj.data.materials.append(new_material)

        if texture_node and texture_node.image:
            # Update the name of the image texture
            texture_node.image.name = image_path
            # Set the image path for the texture node using the custom_text_box value
            EmtyCollCustom = ""
            custom_text_box = context.scene.custom_text_box  # Get the value from custom_text_box
            texture_node.image.filepath = custom_text_box + ''

        return {'FINISHED'}
#------------------------------------
class DeleteMaterialSlotsOperator(bpy.types.Operator):
    bl_idname = "custom.delete_material_slots"
    bl_label = "Delete All Material Slots"
    bl_description = "Delete all material slots from selected objects"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            if obj.type == 'MESH':
                obj.data.materials.clear()
        #bpy.ops.object.fix_copied_materials()
        return {'FINISHED'}
##-------------------------------------------------------------------End DayZ
##----------------------------------End update material Enfusion
Opus_Utility.preview_collections = {}
#---------------------------------------------------------------------------------------------------
classes = [
    MyProperties, RvmatToBlender.CustomAdditionalButton, RvmatToBlender.CustomSaveFolderPath, RvmatToBlender.CustomDisplayRvmatContent, RvmatToBlender.CustomLoadRvmat, RvmatToBlender.CustomCheckTextureNodes,
    RvmatToBlender.CopyAndConvertOperator, RvmatToBlender.SaveFolderPathOperator,
    Opus_ComboPanel.ComboPanel, Opus_ComboPanel.OBJECT_OT_my_operatorCorrectUV, Opus_ComboPanel.MyButtonOperator, Opus_ComboPanel.SelectObjectOperator,
    Opus_ComboPanel.OBJECT_OT_AddVertexGroups, Opus_ComboPanel.OBJECT_OT_DeleteAllVertexGroups, Opus_ComboPanel.OBJECT_OT_RemoveVertexGroup, Opus_ComboPanel.OBJECT_OT_AssignVertexGroup,
    Opus_ComboPanel.CopyEmptySMvigor,
    ADDONNAME_OT_my_op, Opus_Utility.ClearNormalsProForDayZ, Opus_Utility.GetSharpFormAutoSmooth, Opus_Utility.CopyFilePresetExportPainter,
    MyMaterial, 
    Material_OT_my_op, 
    WireframeToggleAddon, 
    ToggleFaceOrientationAddon, 
    WireframeToggleAddons, Opus_Utility.RunEXEtoolsDayZ, Opus_Utility.OrganizeObjectsOperator,
    CreateToggleTransformOrientationOperator,
    CreateAssignMaterialOperator, CreateAssignTGAMaterialOperator, CreateAssignMaterialFromDropdownOperator, DeleteMaterialSlotsOperator, CustomSelectTGAOperator, ReadRvmatNamesAndSaveOperator, 
    Opus_Utility.CreateGeometryOperator, Opus_Utility.OperatorLoopsCreateBoxes, Opus_Utility.OperatorLoopsCreateBoxesVertex,  Opus_Utility.OperatorLoopsCreateBoxesGenerate, Opus_Utility.SeparateLoosePartsOperator,
    Opus_Utility.OBJECT_OT_copy_material_operator, Opus_Utility.SimpleOperatorReopen, Opus_Utility.AddMaterialOperator, Opus_Utility.AddMaterialOperatorSuper, Opus_Utility.AddMaterialOperatorSuperCA,
    Opus_PieMenu.CustomPieOperator, Opus_PieMenu.CustomPieMenu, Opus_PieMenu.CustomPieOperatorObject, Opus_PieMenu.OpenDialogOperator, Opus_PieMenu.CustomDialogOperator, Opus_PieMenu.OpenDialogOperatorAssignMatPre,
    Opus_PieMenu.CustomDialogOperatorAssignMatPre, Opus_PieMenu.OpenDialogOperatorMain, Opus_PieMenu.CustomDialogOperatorMain, Opus_PieMenu.OpenDialogOperatorRename, Opus_PieMenu.CustomDialogOperatorRename,
    Opus_PieMenu.OpenDialogOperatorQuickFavorites, Opus_PieMenu.CustomDialogOperatorQuickFavorites, Opus_PieMenu.CustomPieMenuFavorites, Opus_PieMenu.CustomPieFavoritesOperator, 
    Opus_PieMenu.TEXT_OT_SaveShortcut, Opus_PieMenu.OpustiToolProperties, Opus_PieMenu.RemoveWeightedNormalOperator, Opus_PieMenu.CustomPieFavoritesOperatorEdit, Opus_PieMenu.OpenDialogOperatorAutoMerge, Opus_PieMenu.CustomDialogOperatorAutoMerge,
    Opus_PieMenu.CustomDialogOperatorReadnameMB, Opus_PieMenu.OpenDialogOperatorReadnameMB, Opus_PieMenu.ReadModelsOperator, Opus_PieMenu.MY_UL_read_models_list,
    Opus_Update.RedTextMenu, Opus_Update.UpdateCheckOperator, Opus_Update.InstallAddonOperator,
    Opus_PieMenu.CUSTOM_OT_AssignMaterialOperator, Opus_PieMenu.MATERIALS_PT_ListMaterialsOperator, UptoDate.WM_OT_AlwaysSkipOperator, UptoDate.Update_missionDayZ,
    Opus_Utility.ExportActiveCollectionFBXOperator, Opus_Utility.RemoveSuffixOperator, Opus_Utility.RenameObjectsInCollection, Opus_Utility.SmartDuplicateObjectsOperator, UptoDate.WM_OT_SkipOperator, UptoDate.WM_OT_UpdateOperator,
]
#---------------------------------------------------------------------------------------------------
class MyToolProperties(bpy.types.PropertyGroup):
    my_property: bpy.props.IntProperty(name="My Property")
#----------------------------------------------------Sort object to collection DayZ
bpy.types.Scene.my_prefix = bpy.props.StringProperty(
    name="Prefix",
    default="",
    description="Prefix for Collection Names"
)
class MaterialSelectorOperator(bpy.types.Operator):
    bl_idname = "wm.material_selector_operator"
    bl_label = "Material Selector"

    def execute(self, context):
        # โค้ดลงทะเบียนของคุณที่นี่
        context.scene.selected_material = bpy.props.EnumProperty(
            items=[(mat.name, mat.name, "") for mat in bpy.data.materials],
            description="Select Material"
        )
        return {'FINISHED'}
def register():
    #-------------------------Shift Key for Update news

#----------------------------------------------------DayZ convert A3 to Dz and copy texture and rvmate
    bpy.utils.register_class(RvmatToBlender.LoadRvmatOperator)
    bpy.types.Scene.folder_path_convert = bpy.props.StringProperty(
        name="Source Folder Path",
        default="C:/",
        subtype='DIR_PATH',
    )
    bpy.types.Scene.target_folder_path = bpy.props.StringProperty(
        name="Target Folder Path",
        default="C:/",
        subtype='DIR_PATH',
    )
    if bpy.context.window_manager.windows:
        # Check if there are windows in the window manager
        main_window = bpy.context.window_manager.windows[0]

        if main_window.scene:
            # Check if the main window has a scene
            default_folder_path = "C:/" 
            save_path = os.path.join(os.path.expanduser('~'), "Documents", "saveLrvmatConvert.txt")

            if os.path.exists(save_path):
                with open(save_path, 'r') as file:
                    saved_folder_path = file.read().strip()  # อ่านข้อความจากไฟล์

                if os.path.exists(saved_folder_path):  # เช็คว่าพาธที่อ่านมาถูกต้องหรือไม่
                    default_folder_path = saved_folder_path

                bpy.context.window_manager.windows[0].scene.folder_path_convert = default_folder_path

                rvmat_folder = bpy.path.abspath(default_folder_path)
                rvmat_files = [f for f in os.listdir(rvmat_folder) if f.endswith(".rvmat")]

                bpy.types.Scene.selected_rvmat_convert = bpy.props.EnumProperty(
                    items=[(f, f, "") for f in rvmat_files],
                    description="Select .rvmat File"
                )
            else:
                print(f"Warning: Saved file '{save_path}' not found.")

#--------------------------------------Opus_Update
    bpy.types.Scene.custom_addon_red_text_enum = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    bpy.types.Scene.custom_addon_red_text_enum_index = bpy.props.IntProperty()
#------------------------------------
    bpy.utils.register_class(MaterialSelectorOperator)
    bpy.types.Scene.folder_path = bpy.props.StringProperty(
        name="Folder Path",
        default="C:/",
        subtype='DIR_PATH',
    )

    bpy.types.Scene.custom_text = bpy.props.StringProperty(
        name="Custom Text",
        default="",
        description="Enter custom text",
    )
    if bpy.context.window_manager.windows:
        # Check if there are windows in the window manager
        main_window = bpy.context.window_manager.windows[0]

        if main_window.scene:
            # Check if the main window has a scene
            default_folder_path = "C:/"
            save_path = "C:\\Users\\Public\\Documents\\saveLrvmatDZ.txt"

            if os.path.exists(save_path):
                # Read the content of the file
                with open(save_path, 'r') as file:
                    saved_text = file.read().strip()
                    
                # Check if the saved text is a valid and existing path
                if os.path.exists(saved_text):
                    default_folder_path = saved_text

                    bpy.context.window_manager.windows[0].scene.folder_path = default_folder_path

                    rvmat_folder = bpy.path.abspath(default_folder_path)
                    rvmat_files = [f for f in os.listdir(rvmat_folder) if f.endswith(".rvmat")]

                    bpy.types.Scene.selected_rvmat = bpy.props.EnumProperty(
                        items=[(f, f, "") for f in rvmat_files],
                        description="Select .rvmat File"
                    )
                else:
                    print(f"Warning: The saved path '{saved_text}' is not valid or does not exist.")
            else:
                print(f"Warning: Saved file '{save_path}' not found.")
#********************************
##----------------------------Dayz
    # Directory path
    rvmat_directory = "P:\\dz\\data\\data\\penetration"
    tga_directory = "P:\\dz\\surfaces\\data\\roadway"

    # Check if the directory exists
    if os.path.exists(rvmat_directory):
        # Define the custom property for the RVMAT list
        bpy.types.Scene.custom_rvmat_list = bpy.props.EnumProperty(
            name="RVMAT List",
            items=get_rvmat_files(rvmat_directory),
            description="List of RVMAT files in the specified directory",
        )
    else:
        bpy.types.Scene.custom_rvmat_list = bpy.props.EnumProperty(
            name="RVMAT List (Missing P drive)",
            items=[("Missing P drive", "Missing P drive", "")],
            description="Directory does not exist",
        )
    # Check if the directory exists
    if os.path.exists(tga_directory):
        # Define the custom property for the TGA list
        bpy.types.Scene.custom_tga_list = bpy.props.EnumProperty(
            name="TGA List",
            items=get_tga_files(tga_directory),
            description="List of TGA files in the specified directory",
        )
    else:
        bpy.types.Scene.custom_tga_list = bpy.props.EnumProperty(
            name="TGA List (Missing P drive)",
            items=[("Missing P drive", "Missing P drive", "")],
            description="Directory does not exist",
        )
    bpy.types.Scene.custom_text_box = bpy.props.StringProperty(
        name="Custom Text Box",
        description="Text Box with editable text",
        default="CO",
    )

    # Define the custom_new_menu_list property
    def get_rvmat_paths(self, context):
        rvmat_paths = []
        save_path = os.path.join("C:\\Users\\Public\\Downloads", "SaveRvmat.txt")
        
        if os.path.exists(save_path):
            with open(save_path, 'r') as file:
                rvmat_directory = file.read().strip()
                if os.path.isdir(rvmat_directory):
                    rvmat_files = [f for f in os.listdir(rvmat_directory) if f.endswith('.rvmat')]
                    rvmat_paths = [(f, f, "") for f in rvmat_files]

        return rvmat_paths

    bpy.types.Scene.custom_new_menu_list = bpy.props.EnumProperty(
        name="New Menu List",
        items=get_rvmat_paths,
    )

    #bpy.utils.register_class(ReadRvmatNamesAndSaveOperator)
    save_path = os.path.join("C:\\Users\\Public\\Downloads", "SaveRvmat.txt")
    if os.path.exists(save_path):
        with open(save_path, 'r') as file:
            custom_directory_path = file.read().strip()
            bpy.types.Scene.custom_directory_path = bpy.props.StringProperty(
                name="Directory Path",
                description="Enter the directory path to read .rvmat files from and save to SaveRvmat.txt",
                default=custom_directory_path,  # Set the default value here
            )
##----------------End DayZ
    #----------------TGA TO TIF
    bpy.types.Scene.bat_file_choice = bpy.props.EnumProperty(
        name="",
        items=[
            ("TGA to TIF", "TGA to TIF", ""),
            ("Delete all tif", "Delete all tif", "")
        ]
    )
    bpy.types.Scene.bat_file_text = bpy.props.StringProperty(
        name="",
        subtype='DIR_PATH'
    )
    #----------------
    bpy.types.Scene.custom_panel_input = bpy.props.StringProperty(
        name="Input Text",
        default="SM_Vigor"
    )
    #--------------
    bpy.utils.register_class(MyToolProperties)
    #---------------------------Update addons
    #bpy.types.Scene.custom_addon_red_text_enum = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    #bpy.types.Scene.custom_addon_red_text_enum_index = bpy.props.IntProperty(default=0)
    #------------read name object and check material
    bpy.types.Scene.my_read_models_list = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    bpy.types.Scene.my_read_models_list_index = bpy.props.IntProperty()
    # ------Pie Menu
    filepath = os.path.join(bpy.utils.user_resource('SCRIPTS'), 'addons', 'Opusti_Tool', 'text_data', 'ShortCut.txt')
    with open(filepath, 'r') as file:
        key_bind = file.read().strip()
        
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_menu_pie', key_bind, 'PRESS')
    kmi.properties.name = "OBJECT_MT_custom_pie_menu"
    
    ##-----------End Pie Menu
    bpy.utils.register_class(DeleteAllTransformOrientationOperator)
    #---------
    bpy.utils.register_class(MyToolOperator)
    bpy.utils.register_class(OpustiStatusProperties)
    bpy.types.Scene.opusti_status = bpy.props.PointerProperty(type=OpustiStatusProperties)
    bpy.utils.register_class( Opus_Normal.TEST_OT_test_op)
    #--------
    bpy.utils.register_class(Opus_Utility.SetActiveUVMapOperator)
    bpy.utils.register_class(Opus_Utility.RemoveUVMapOperator)
    bpy.utils.register_class(Opus_Utility.AddUVMapOperator)
    #----.001-.099
    bpy.utils.register_class(Opus_Utility.UpdateObjectNameOperator)
    #--------
    bpy.utils.register_class(ApplyTransformsOperator)
    bpy.utils.register_class(FixCopiedMaterialsOperator)
    bpy.utils.register_class(MyOperator1)
    bpy.utils.register_class(OBJECT_OT_CreateBoxMatchDimensionsRotationMoveOperator)
    bpy.utils.register_class(Opus_Utility.SelectFurthestOperator)
    bpy.utils.register_class(Opus_Utility.SelectFurthestOperatorFace)
    bpy.utils.register_class(Opus_Utility.CustomPanelOperatorMulticall)
    bpy.utils.register_class(Opus_Utility.CustomPanelOperatorMulticallFace)
    bpy.utils.register_class(Opus_Utility.RandomDeselectOperator)
    # Register the scene property
    bpy.types.Scene.create_toggle_transform_orientation = bpy.props.BoolProperty(default=False)
    #---------rename UVMap
    bpy.utils.register_class(Opus_Utility.OBJECT_OT_RenameUV)
    bpy.utils.register_class(Opus_Utility.OBJECT_OT_ResetUVNames)
    bpy.types.Scene.first_uv_name = bpy.props.StringProperty(name="First UV Name", default="UVmap0")
    bpy.types.Scene.second_uv_name = bpy.props.StringProperty(name="Second UV Name", default="UVmap1")
    #---------
    bpy.utils.register_class(Opus_Utility.OBJECT_OT_RemoveUnusedMaterials)
    bpy.utils.register_class(Opus_Utility.RemoveMaterialSlotsOperator)
    bpy.utils.register_class(Opus_Utility.ShadeSmoothOperator)
    bpy.utils.register_class(RandomDiffuseColorOperator)
    bpy.utils.register_class(Opus_ui.CustomOperatorVertexGroupbrick)
    bpy.utils.register_class(Opus_Utility.OBJECT_OT_RenameSelectedOperator)
    bpy.types.Scene.new_object_name = bpy.props.StringProperty(name="Name")
    bpy.types.Scene.suffix_text = bpy.props.StringProperty(name="Suffix")  # Property for suffix text
    ##--------Update material
    bpy.utils.register_class(CustomMaterial)
    #bpy.utils.register_class(CombinedPanel)
    bpy.utils.register_class(SaveTextDataOperator)
    bpy.types.Scene.custom_material = bpy.props.PointerProperty(type=CustomMaterial)
    bpy.types.Scene.base_folder_path = bpy.props.StringProperty(name="Base Folder Path", default=base_folder_path)
    ##----end
    ##---------------------Added personal material
    bpy.types.Scene.my_folder_location = StringProperty(
        name="",
        subtype='DIR_PATH'
    )
    bpy.utils.register_class(Opus_Utility.FolderSelectOperator)
    bpy.utils.register_class(Opus_Utility.SimpleOperator)
    bpy.utils.register_class(Opus_Utility.PopupDialogOperator)
    bpy.utils.register_class(Opus_Utility.RemoveLineOperator)
    bpy.utils.register_class(Opus_Utility.CopyTextToCollisionMatOperator)
    bpy.types.Scene.my_label_text = bpy.props.StringProperty(default="")
    ##----------------End
    ##---------------------------------Duplicate rename
    bpy.utils.register_class(Opus_Utility.CopyAndRenameOperator)
    ##-------------------------
    bpy.types.Scene.mytool_color = bpy.props.FloatVectorProperty(
                 name = "",
                 subtype = "COLOR",
                 size = 4,
                 min = 0.0,
                 max = 1.0,
                 default = (1.0,1.0,1.0,1.0))
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= MyProperties)

    for cls in classes:
        bpy.types.Scene.my_material = bpy.props.PointerProperty(type= MyMaterial)
    for cls in classes:
        bpy.types.Scene.opusti_tool = bpy.props.PointerProperty(type=Opus_PieMenu.OpustiToolProperties)
        
##-----------icon
    Opus_Utility.pcoll = bpy.utils.previews.new()

    # path to the folder where the icon is
    # the path is calculated relative to this py file inside the addon folder
    my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    # load a preview thumbnail of a file and store in the previews collection
    Opus_Utility.pcoll.load("icon_main", os.path.join(my_icons_dir, "Opusti_main.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_dayz", os.path.join(my_icons_dir, "Opusti_dayz.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_update", os.path.join(my_icons_dir, "Opusti_update.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_reload", os.path.join(my_icons_dir, "Opusti_reload.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_reopen", os.path.join(my_icons_dir, "Opusti_reopen.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_export", os.path.join(my_icons_dir, "Opusti_export.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_setting1", os.path.join(my_icons_dir, "Opusti_setting1.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_setting2", os.path.join(my_icons_dir, "Opusti_setting2.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_orient", os.path.join(my_icons_dir, "Opusti_orient.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_origins", os.path.join(my_icons_dir, "Opusti_origins.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_global", os.path.join(my_icons_dir, "Opusti_global.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_CD", os.path.join(my_icons_dir, "Opusti_CD.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_grow", os.path.join(my_icons_dir, "Opusti_grow.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_reverse", os.path.join(my_icons_dir, "Opusti_reverse.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_flip", os.path.join(my_icons_dir, "Opusti_flip.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_borders", os.path.join(my_icons_dir, "Opusti_borders.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_shell", os.path.join(my_icons_dir, "Opusti_shell.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_multi", os.path.join(my_icons_dir, "Opusti_multi.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_single", os.path.join(my_icons_dir, "Opusti_single.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_wnm", os.path.join(my_icons_dir, "Opusti_wnm.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_clearnm", os.path.join(my_icons_dir, "Opusti_clearnm.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_ca", os.path.join(my_icons_dir, "Opusti_ca.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_material1", os.path.join(my_icons_dir, "Opusti_material1.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_material", os.path.join(my_icons_dir, "Opusti_material.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_coverbox", os.path.join(my_icons_dir, "Opusti_coverbox.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_list", os.path.join(my_icons_dir, "Opusti_list.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_magic", os.path.join(my_icons_dir, "Opusti_magic.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_boxclear", os.path.join(my_icons_dir, "Opusti_boxclear.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_seam", os.path.join(my_icons_dir, "Opusti_seam.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_sharp", os.path.join(my_icons_dir, "Opusti_sharp.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_split", os.path.join(my_icons_dir, "Opusti_split.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_rvmat", os.path.join(my_icons_dir, "Opusti_rvmat.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_roadway", os.path.join(my_icons_dir, "Opusti_roadway.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_firegeo", os.path.join(my_icons_dir, "Opusti_firegeo.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_tri", os.path.join(my_icons_dir, "Opusti_tri.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_half", os.path.join(my_icons_dir, "Opusti_half.png"), 'IMAGE')
    Opus_Utility.pcoll.load("icon_mission", os.path.join(my_icons_dir, "Opusti_mission.png"), 'IMAGE')
    Opus_Utility.preview_collections["main"] = Opus_Utility.pcoll   
##------------End icon
#----------------------------Combo panel
    bpy.types.Scene.Panel_Menu = bpy.props.EnumProperty(
        items=[('STATUS', "", "Main", 'PMARKER_ACT', 0),
               ('DayZ', "", "DayZ", 'EVENT_D', 7),
               ('FINDING_ERRORS', "", "Finding Errors", 'TEMP', 2),
               ('MAIN', "", "Modifier", 'MODIFIER', 3), 
               ('SCATTER_BRICK_WOOD', "", "Scatter Bricks and Woods", 'SEQ_HISTOGRAM', 4),
               ('UV_MAPS', "", "UV Maps", 'UV', 1),
               ('VERTEX_COLORS', "", "Vertex Colors paint", 'COLOR', 5),
               ('SETTING_OR_UPDATE', "", "Setting or Update", 'PREFERENCES', 6)],
        default='STATUS')
    bpy.types.Scene.Check_Errors = bpy.props.EnumProperty(
        items=[('Mesh', "Mesh", "Check Mesh errors", 0),
               ('Materials', "Materials", "Check Materials errors", 1)],
        default='Mesh')
def unregister():
    #-------------------------------------
    ##-----------DayZ
    del bpy.types.Scene.custom_rvmat_list
    del bpy.types.Scene.custom_tga_list
    ##---------End DayZ
    #----------------TGA TO TIF
    del bpy.types.Scene.bat_file_choice
    del bpy.types.Scene.bat_file_text
    #----------------
    del bpy.types.Scene.custom_panel_input
    #--------------
    bpy.utils.unregister_class(MyToolProperties)
    # Remove the keymap entry
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps['Window']
    
    # Find the keymap item with the matching properties
    for kmi in km.keymap_items:
        if kmi.idname == 'wm.call_menu_pie' and kmi.type == 'PRESS' and kmi.properties.name == "OBJECT_MT_custom_pie_menu":
            km.keymap_items.remove(kmi)
            break
    ##-----------End Pie Menu
    bpy.utils.unregister_class(DeleteAllTransformOrientationOperator)
    #---------
    bpy.utils.unregister_class(MyToolOperator)
    bpy.utils.unregister_class(OpustiStatusProperties)
    del bpy.types.Scene.opusti_status
    bpy.utils.unregister_class(Opus_Normal.TEST_OT_test_op)
    bpy.utils.unregister_class(Opus_Utility.SetActiveUVMapOperator)
    bpy.utils.unregister_class(Opus_Utility.RemoveUVMapOperator)
    bpy.utils.unregister_class(Opus_Utility.AddUVMapOperator)
    #----.001-.099
    bpy.utils.unregister_class(Opus_Utility.UpdateObjectNameOperator)
    #--------
    bpy.utils.unregister_class(ApplyTransformsOperator)
    bpy.utils.unregister_class(FixCopiedMaterialsOperator)
    bpy.utils.unregister_class(MyOperator1)
    bpy.utils.unregister_class(OBJECT_OT_CreateBoxMatchDimensionsRotationMoveOperator)
    bpy.utils.unregister_class(Opus_Utility.SelectFurthestOperator)
    bpy.utils.unregister_class(Opus_Utility.SelectFurthestOperatorFace)
    bpy.utils.unregister_class(Opus_Utility.CustomPanelOperatorMulticall)
    bpy.utils.unregister_class(Opus_Utility.CustomPanelOperatorMulticallFace)
    bpy.utils.unregister_class(Opus_Utility.RandomDeselectOperator)
    #---------rename UVMap
    bpy.utils.unregister_class(Opus_Utility.OBJECT_OT_RenameUV)
    bpy.utils.unregister_class(Opus_Utility.OBJECT_OT_ResetUVNames)

    bpy.utils.unregister_class(Opus_Utility.OBJECT_OT_RemoveUnusedMaterials)
    bpy.utils.unregister_class(Opus_Utility.RemoveMaterialSlotsOperator)
    bpy.utils.unregister_class(Opus_Utility.ShadeSmoothOperator)
    bpy.utils.unregister_class(Opus_Utility.OBJECT_OT_RenameSelectedOperator)
    bpy.utils.unregister_class(RandomDiffuseColorOperator)
    bpy.utils.unregister_class(Opus_ui.CustomOperatorVertexGroupbrick)
    ##----end
    del bpy.types.Scene.first_uv_name
    del bpy.types.Scene.second_uv_name
    #---------
    # Unregister the scene property
    del bpy.types.Scene.create_toggle_transform_orientation
    #--------
    del bpy.types.Scene.my_tool
    for cls in classes:
        bpy.utils.unregister_class(cls)
##-----------icon
    for Opus_Utility.pcoll in Opus_Utility.preview_collections.values():
        bpy.utils.previews.remove(Opus_Utility.pcoll)

    Opus_Utility.preview_collections.clear()
##------------End icon
    ##--------Update material
    bpy.utils.unregister_class(CustomMaterial)
    bpy.utils.unregister_class(SaveTextDataOperator)
    del bpy.types.Scene.custom_material
    del bpy.types.Scene.base_folder_path
    ##----end
    ##---------------------Added personal material
    bpy.utils.unregister_class(Opus_Utility.FolderSelectOperator)
    bpy.utils.unregister_class(Opus_Utility.SimpleOperator)
    bpy.utils.unregister_class(Opus_Utility.PopupDialogOperator)
    bpy.utils.unregister_class(Opus_Utility.RemoveLineOperator)
    bpy.utils.unregister_class(Opus_Utility.CopyTextToCollisionMatOperator)
    del bpy.types.Scene.my_label_text
    ##----------------End
    ##---------------------------------Duplicate rename
    bpy.utils.unregister_class(Opus_Utility.CopyAndRenameOperator)
    #------------read name object and check material
    del bpy.types.Scene.my_read_models_list
    del bpy.types.Scene.my_read_models_list_index
    #---------------------------Update addons
    #del bpy.types.Scene.custom_addon_red_text_enum
    #del bpy.types.Scene.custom_addon_red_text_enum_index
    #------------Combo panel
    del bpy.types.Scene.Panel_Menu
    del bpy.types.Scene.Check_Errors
    #***********************
    bpy.utils.unregister_class(MaterialSelectorOperator)
    try:
        del bpy.types.Scene.selected_rvmat
    except AttributeError:
        pass
    del bpy.types.Scene.folder_path
    del bpy.types.Scene.custom_text
    #--------------------------------------Opus_Update
    del bpy.types.Scene.custom_addon_red_text_enum
    del bpy.types.Scene.custom_addon_red_text_enum_index
#----------------------------------------------------DayZ convert A3 to Dz and copy texture and rvmate
    try:
        del bpy.types.Scene.selected_rvmat_convert
    except AttributeError:
        pass
    del bpy.types.Scene.folder_path_convert
    #-------------------------------------------------
if __name__ == "__main__":
    register()
    bpy.ops.object.fix_copied_materials()
    bpy.context.area.tag_redraw()
RvmatToBlender.initialize()