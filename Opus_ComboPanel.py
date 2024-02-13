import os
import urllib.request
import zipfile
from . import Opus_Normal
from . import Opus_ui
from . import Opus_Utility
from . import UptoDate
import bpy
from bpy.types import Panel
buttonY=1.1
buttonX=5.0

class OBJECT_OT_my_operatorCorrectUV(bpy.types.Operator):
    bl_idname = "object.my_operator"
    bl_label = "Toggle Correct Face Attributes"

    def execute(self, context):
        # Toggle the value of use_transform_correct_face_attributes
        scene = bpy.context.scene
        scene.tool_settings.use_transform_correct_face_attributes = not scene.tool_settings.use_transform_correct_face_attributes
        
        # Display a message to inform the user about the current state
        if scene.tool_settings.use_transform_correct_face_attributes:
            self.report({'INFO'}, "Toggle ON: Correct Face Attributes")
        else:
            self.report({'INFO'}, "Toggle OFF: Correct Face Attributes")
            
        return {'FINISHED'}
class MyButtonOperator(bpy.types.Operator):
    bl_idname = "wm.my_button_operator"
    bl_label = "My Button"
    bl_description=" Custom origin of the models"

    def execute(self, context):
        # Toggle the "use_transform_data_origin" property
        scene = context.scene
        scene.tool_settings.use_transform_data_origin = not scene.tool_settings.use_transform_data_origin

        # Call your custom function here if needed
        my_button_function(self, context)
        return {'FINISHED'}
def my_button_function(self, context):
    print("Button clicked!")
class Status(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_status"
    bl_label = "Status"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Combo Panel'

    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def draw_header(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Opusti Status", icon='PMARKER_ACT')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_tool = scene.opusti_status
        selected = context.selected_objects
        layout.enabled = getattr(context.active_object, "type", "") == "MESH" and context.active_object in selected

        iconReload = Opus_Utility.pcoll["icon_reload"]
        icontri = Opus_Utility.pcoll["icon_tri"]
        iconhalf = Opus_Utility.pcoll["icon_half"]

        box = layout.box()
        row = box.row()
        iconReopen = Opus_Utility.pcoll["icon_reopen"]
        row.operator("object.auto_reopen_panel", text="Reopen blender", icon_value=iconReopen.icon_id)
        row = box.row()
        iconlist = Opus_Utility.pcoll["icon_list"]
        try:
            row.label(text=bpy.context.object["usage"], icon_value=iconlist.icon_id)
        except:
            row.label(text="None", icon_value=iconlist.icon_id)

        row = box.row()
        row.label(text="Tri : {}".format(bpy.context.scene.my_label_text0), icon_value=icontri.icon_id)
        row = box.row()
        row.label(text="Result : {}".format(bpy.context.scene.my_label_text1), icon_value=iconhalf.icon_id)
        
        # Add text box for My Number property
        row = box.row(align=True)
        col10 = row.column(align=True)
        col10.prop(my_tool, "my_number")
        col10 = row.column(align=True)
        
        col10.scale_x=0.85
        col10.operator("object.my_tool_operator", text="Reload", icon_value=iconReload.icon_id)
        
        #row = layout.row()
        row = layout.row(align=True)
        row.scale_x = 0.5
        row.operator("view3d.wireframe_toggle", text="", icon="CUBE")
        row.scale_x = 0.5
        row.operator("view3d.wireframe_toggles", text="", icon="MESH_CUBE")
        ## Orientation
        space_data = context.space_data
        row.scale_x = 0.5
        row.prop(space_data.overlay, "show_face_orientation", text="", toggle=True, icon="OUTLINER_OB_LIGHTPROBE")
        ## UVs
        col = row.column(align=True)
        col.scale_x = 0.7  # Move the "Custom Origins" button by 0.5 (half of the available space)
        col.prop(scene.tool_settings, "use_transform_correct_face_attributes", text="", icon='OUTLINER_OB_LIGHT', toggle=True)
        col = row.column(align=True)
        col.scale_x = 0.3
        col.operator("object.my_operator", text="Correct UVs")
        # Threshold distance
        #box = layout.box()
        row = layout.row()
        row.prop(scene.tool_settings, "double_threshold", text="")
        # Auto Merge toggle
        row.prop(scene.tool_settings, "use_mesh_automerge", text="")
        # Get the operator's toggle property
        toggle_property = scene.create_toggle_transform_orientation
        # Create the checkbox to toggle the operator
        
        #box = layout.box()
        #row = box.row()
        row = layout.row(align=True)
        col5 = row.column(align=True)
        if bpy.context.active_object is not None:
            if context.object.mode == "EDIT":
                # Add the operator button
                iconorient = Opus_Utility.pcoll["icon_orient"]
                operator_props = col5.operator("object.create_toggle_transform_orientation", text="GetOrient", icon_value=iconorient.icon_id)
                col5 = row.column(align=True)
                UptoDate.main_function() #Check laste update from cloud
            iconglobal = Opus_Utility.pcoll["icon_global"]
            operator_props = col5.operator("my_operator.button1", text="Global", icon_value=iconglobal.icon_id)
            #operator_props.toggle_property = toggle_property
        if bpy.context.active_object is not None:
            if context.object and context.object.mode == "OBJECT":
                col5.operator("object.apply_transforms", text="Reset | Origin to Center")
                col5.operator('test.test_op', text='Reset All Transfrom').action = 'R_Transfrom'
                text = bpy.props.StringProperty(name="Enter Text", default="")
        row = layout.row(align=True)
        # Add the custom button using the provided code
        col1 = row.column(align=True)
        col1.scale_x = 0.5  # Move the "Custom Origins" button by 0.5 (half of the available space)
        iconorigins = Opus_Utility.pcoll["icon_origins"]
        col1.prop(scene.tool_settings, "use_transform_data_origin", text="", icon_value=iconorigins.icon_id, toggle=True)

        # Add the custom operator button
        #row = layout.row(align=True)
        col1= row.column(align=True)
        col1.scale_x = 8  # Move the "My Button" by 1.0 (full available space)
        col1.operator("wm.my_button_operator", text="Custom Origins")
        #col1.prop(scene.tool_settings, "use_transform_data_origin", text="Custom Origins", toggle=True)
        #row = box.row()
        if bpy.context.active_object is not None:
            if context.object and context.object.mode == "OBJECT":
                iconcoverbox = Opus_Utility.pcoll["icon_coverbox"]
                iconmagic = Opus_Utility.pcoll["icon_magic"]
                row = layout.row(align=True)
                col1 = row.column(align=True)
                col1.operator("object.custom_panel_operator", text="OrienVertex")
                col1.operator("object.operator_loops_create_boxes_vertex", text="Coll.Vertex")
                col1.operator("object.operator_loops_create_boxes_generate", text="Generate", icon_value=iconmagic.icon_id)
                col1 = row.column(align=True)
                col1.operator("object.custom_panel_operatorface", text="OrienFace")
                col1.operator("object.operator_loops_create_boxes", text="Coll.Face")
                col1.operator("object.create_cube", text="Create Box", icon_value=iconcoverbox.icon_id)
            ##---------------------------------------------------------------From Edit mode modifiy
            #box = layout.box()
            row = layout.row(align=True)
            col9 = row.column(align=True)
            iconorwnm = Opus_Utility.pcoll["icon_wnm"]
            iconclearnm = Opus_Utility.pcoll["icon_clearnm"]
            col9.operator('test.test_op', text='ClearNormals', icon_value=iconclearnm.icon_id).action = 'CLEARNORMAL'
            col9.operator('test.test_op', text='WeightedNormal', icon_value=iconorwnm.icon_id).action = 'WeightedNormal'
            obj = context.active_object

            if obj is not None:
                row = layout.row(align=True)
                col6 = row.column(align=True)
                col6.scale_x = 0.9
                col6.prop(obj.data, "auto_smooth_angle", text="Smooth Angle")

                col6 = row.column(align=True)
                col6.prop(obj.data, "use_auto_smooth", text="")
            else:
                layout.label(text="No active object selected")
            #row = layout.row()
            #row.operator('test.test_op', text='Face Orientation', icon = 'OUTLINER_OB_LIGHTPROBE').action = 'FaceOrientation'
            row = layout.row(align=True)
            col3 = row.column(align=True)
            col3.operator('test.test_op', text='X', icon= 'AXIS_SIDE').action = 'P_X'
            col3 = row.column(align=True)
            col3.operator('test.test_op', text='Y', icon= 'AXIS_FRONT').action = 'P_Y'
            col3 = row.column(align=True)
            col3.operator('test.test_op', text='Z', icon= 'AXIS_TOP').action = 'P_Z'
            col3 = row.column(align=True)
            col3.operator('test.test_op', text='A', icon= 'FULLSCREEN_EXIT').action = 'P_all'
            #layout.label(text='Calculate LODs', icon='SCRIPT')
            #row = layout.row()
            #row.operator('test.test_op', text='50%', icon = 'KEYFRAME_HLT').action = 'SmartRepeat'
            #row.operator('test.test_op', text='25%', icon = 'KEYFRAME_HLT').action = 'SmartRepeat25'
            iconseam = Opus_Utility.pcoll["icon_seam"]
            iconsharp = Opus_Utility.pcoll["icon_sharp"]
            iconboxclear = Opus_Utility.pcoll["icon_boxclear"]
            iconsplit = Opus_Utility.pcoll["icon_split"]
        if bpy.context.active_object is not None:
            if context.object.mode == "EDIT":
                box = layout.box()
                row = box.row()
                row.operator("mira.unbevel", text="Unbevel", icon="DRIVER_ROTATIONAL_DIFFERENCE")	
                row = box.row(align=True)
                col7 = row.column(align=True)
                iconshell = Opus_Utility.pcoll["icon_shell"]
                col7.operator("mesh.solidify", text='Shell', icon_value=iconshell.icon_id)
                col7.operator('test.test_op', text='Sharp', icon_value=iconsharp.icon_id).action = 'Sharp_O'
                col7.operator('mesh.mark_seam', text='Seam', icon_value=iconseam.icon_id)
                icongrow = Opus_Utility.pcoll["icon_grow"]
                col7.operator('mesh.select_more', text='Grow', icon_value=icongrow.icon_id)
                col7.operator('mesh.split', text='split', icon_value=iconsplit.icon_id)
                col7 = row.column(align=True)
                iconborders = Opus_Utility.pcoll["icon_borders"]
                col7.operator('test.test_op', text='Borders', icon_value=iconborders.icon_id).action = 'SelectedB'
                col7.operator('test.test_op', text='clear Sharp', icon_value=iconboxclear.icon_id).action = 'ClearSharp'
                col7.operator('test.test_op', text='clear Seam', icon_value=iconboxclear.icon_id).action = 'ClearSeam'
                iconreverse = Opus_Utility.pcoll["icon_reverse"]
                col7.operator('mesh.select_less', text='Reverse', icon_value=iconreverse.icon_id)   
                iconflip = Opus_Utility.pcoll["icon_flip"]
                col7.operator('test.test_op', text='Flip Faces', icon_value=iconflip.icon_id).action = 'FlipFaces'
                row = box.row(align=True)
                col8 = row.column(align=True)
                col8.operator('test.test_op', text='Ring', icon = 'COLLAPSEMENU').action = 'Cring'
                col8 = row.column(align=True)
                col8.operator('test.test_op', text='Loop', icon = 'REMOVE').action = 'Cloop'
                col8 = row.column(align=True)
                iconCD = Opus_Utility.pcoll["icon_CD"]
                col8.operator('test.test_op', text='CD', icon_value=iconCD.icon_id).action = 'Ccd'

        #-------------------------------------------Collision Preset    
        #layout.label(text=" Collision", icon='CUBE')
        if bpy.context.active_object is not None:
            if context.object and context.object.mode == "OBJECT":
                #box=layout.box()
                scene = context.scene
                mytool = scene.my_tool
                box = layout.box()
                row = box.row(align=True)
                col1 = row.column(align=True)
                iconlist = Opus_Utility.pcoll["icon_list"]
                col1.prop(mytool, "my_enum",icon_value=iconlist.icon_id, text='')
                col1.operator("addonname.myop_operator", icon='ADD')
                #-------------------------------------------Material Preset           
                mymaterial = scene.my_material
                row = box.row(align=True)
                col1 = row.column(align=True)
                col1.scale_x = 0.17
                col1.operator("object.read_meta_file", text=" ", icon="ADD")
                col1.operator("object.popup_dialog", text=" ", icon="REMOVE")
                col1 = row.column(align=True)
                iconmaterial1 = Opus_Utility.pcoll["icon_material1"]
                col1.prop(mymaterial, "my_enum_M",icon_value=iconmaterial1.icon_id, text='')
                col1.operator("material.myop_operator",icon = 'ADD')
                #row = layout.row()
                row = box.row(align=True)
                col01 = row.column(align=True)
                iconmaterial = Opus_Utility.pcoll["icon_material"]
                col01.operator("custom.custom_materailfromsence", text="Assign Mat* scene to", icon_value=iconmaterial.icon_id)
##---------------rename
        row = layout.row(align=True)
        col4 = row.column(align=True)
        col4.prop(context.scene, "new_object_name", text='')  # Use the scene property directly
        #row = box.row()
        col4.prop(context.scene, "suffix_text", text='')  # New textbox for suffix text
        #row = box.row()
        col4.operator("object.rename_selected", text='Rename and Add a Suffix')

class UVMaps(bpy.types.Panel):#---------------UV Maps
    bl_idname = "VIEW3D_PT_uv_maps"
    bl_label = "UV Maps"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Combo Panel'
    #def draw(self, context):
     #   layout = self.layout
      #  layout.label(text="UV Maps panel content goes here")
    def draw_header(self, context):
        layout = self.layout
        #row = layout.row()
        row.label(text="UV Maps", icon='UV')
    def draw(self, context):
        layout = self.layout
        obj = context.object
        #----------rename UV
        box = layout.box()
        row = box.row()
        row.prop(context.scene, "first_uv_name")
        row = box.row()
        row.prop(context.scene, "second_uv_name")
        row = box.row()
        iconReload = Opus_Utility.pcoll["icon_reload"]
        row.operator("object.rename_uv", text="Rename All", icon_value=iconReload.icon_id)
        row.operator("object.reset_uv_names", text="Reset Names",icon="RECOVER_LAST")
        #-----------end
        layout.label(text='UV maps')
        selected = context.selected_objects
        layout.enabled = getattr(context.active_object, "type", "") == "MESH" and context.active_object in selected
        if obj is not None and obj.type == 'MESH':
            uvmaps = obj.data.uv_layers

            for uvmap in uvmaps:
                box = layout.box()
                row = box.row(align=True)
                row.prop(uvmap, "name", text="")
                row.operator("object.uvmap_set_active", text="", icon="RESTRICT_RENDER_OFF").uvmap_name = uvmap.name
                row.operator("object.uvmap_remove", text="", icon="REMOVE").uvmap_name = uvmap.name

            row = layout.row()
            row.operator("object.uvmap_add", text="Add a new UV", icon="ADD")

def filter_objects_by_suffix(context): ##---------------Finding Errors
    filtered_objects = []

    # Iterate through all objects in the scene
    for obj in bpy.context.scene.objects:
        # Extract the suffix from the object's name
        name_parts = obj.name.split('.')
        if len(name_parts) > 1:
            suffix = name_parts[-1]
            # Check if the suffix is in the range of ".001" to ".099"
            if suffix.startswith("00") or suffix.startswith("0"):
                try:
                    suffix_num = int(suffix)
                    if suffix_num >= 1 and suffix_num <= 99:
                        filtered_objects.append(obj)

                except ValueError:
                    pass

    return filtered_objects
class SelectObjectOperator(bpy.types.Operator):##-------Finding Errors
    bl_idname = "object.select_object"
    bl_label = "Select Object"

    object_name: bpy.props.StringProperty()

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        obj = bpy.context.scene.objects.get(self.object_name)
        if obj:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        return {'FINISHED'}
class FindingErrors(bpy.types.Panel):##-----------------Finding Errors
    bl_idname = "VIEW3D_PT_finding_errors"
    bl_label = "Finding Errors"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Combo Panel'
    def draw_header(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Finding errors", icon='TEMP')
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('object.open_dialog_rednamemb', text='Check Materials', icon = 'NETWORK_DRIVE')
class FindingErrorsMesh(bpy.types.Panel):##-----------------Finding Errors
    bl_idname = "VIEW3D_PT_finding_errorsmesh"
    bl_label = "Finding Errors"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Combo Panel'
    def draw(self, context):
        layout = self.layout
        # Add the text box for the active object's name
        active_object = context.view_layer.objects.active
        if active_object:
            row = layout.row(align=True)
            row.prop(active_object, "name", text="", icon="OUTLINER_OB_MESH")
        filtered_objects = filter_objects_by_suffix(context)
        for obj in filtered_objects:
            row = layout.row(align=True)
            row.label(text=obj.name)
            row.operator("object.select_object", text="", icon="PIVOT_ACTIVE").object_name = obj.name
class FindingErrorsMaterail(bpy.types.Panel):##-----------------Finding Errors
    bl_idname = "VIEW3D_PT_finding_errorsmaterial"
    bl_label = "Finding Errors"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Combo Panel'
    def draw_header(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Finding errors", icon='TEMP')
    def draw(self, context):
        layout = self.layout
#----------------End rename
        row = layout.row()
        operator_props = row.operator("object.fix_copied_materials", text="Fix Material suffixes", icon='MODIFIER')
        suffixes = [".{:03d}".format(i) for i in range(1, 100)]
        for material in bpy.data.materials:
            for suffix in suffixes:
                if material.name.endswith(suffix):
                    row = layout.row()
                    row.prop(material, "name", text="", icon="SHADING_TEXTURE")
#-------------icon
class Main(bpy.types.Panel): #-------------------------Main
    bl_idname = "VIEW3D_PT_main"
    bl_label = "Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Combo Panel'
    #def draw(self, context):
     #   layout = self.layout
      #  layout.label(text="Main panel content goes here")
    def draw_header(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Main", icon='PMARKER')
    def invoke(self, context, event):
        wn=context.window_manager
        return wn.invoke_props_dialog(self)

    def draw(self, context):
        #layout = self.layout
        #scene = context.scene#--
        #obj = context.object
        #selected = context.selected_objects
        #layout.enabled = getattr(context.active_object, "type", "") == "MESH" and context.active_object in selected
        layout = self.layout
        scene = context.scene
        collection = bpy.context.collection  # Get the currently selected collection
        selected = context.selected_objects
        # Check if the active object is in the desired collection and it's a mesh
        enable_button = collection and getattr(context.active_object, "type", "") == "MESH" and context.active_object in selected

        # Add a new button without any functionality
        if enable_button: #click model
            #row = layout.row()
            if bpy.context.active_object is not None:
                if context.object and context.object.mode == "OBJECT":
                    #row = layout.row()
                    #row.operator('test.test_op', text='Reset Transfrom', icon = 'TRASH').action = 'R_Transfrom'
                    #box = layout.box()
                    row = layout.row(align=True)
                    col1 = row.column(align=True)
                    col1.operator('test.test_op', text='LOD Default', icon = 'DUPLICATE').action = 'createDefault'
                    col1.operator('test.test_op', text='convexHull', icon = 'MESH_ICOSPHERE').action = 'ConDe'
                    col1.operator("object.smart_duplicate_objects", text="Smart Copy", icon='DUPLICATE')
                    #col1.operator("object.copy_rename", text="Duplicate")
                    col1 = row.column(align=True)
                    col1.operator('test.test_op', text='COM selected', icon = 'OUTLINER_DATA_EMPTY').action = 'COMbySelected'
                    col1.operator('test.test_op', text='Optimize', icon = 'MOD_DECIM').action = 'ConUCX'
                    col1.operator('test.test_op', text='OptimizeV2', icon = 'MOD_DECIM').action = 'Decim_V2'

                    row = layout.row()
                    row.operator('test.test_op', text='Create Collections LODs', icon = 'NODE_COMPOSITING').action = 'Coll_Add'

                    box = layout.box()
                    row = box.row(align=True)
                    #row = layout.row(align=True)
                    col01 = row.column(align=True)  
                    try:
                        col01.label(text=bpy.context.object["fbx_type"], icon="FILE_VOLUME")
                    except:
                        col01.label(text="None", icon="FILE_VOLUME")
                    col01.prop(scene, "custom_panel_input", text='')
                    row = layout.row(align=True)
                    col01.operator("object.copy_empty_sm_vigor", text="Add empty for Vigor", icon='ADD')
        else: #click collection
            row = layout.row()

            if bpy.context.active_object is not None:
                if context.object and context.object.mode == "OBJECT":

                    row = layout.row()
                    row.operator('test.test_op', text='Create Collections LODs', icon = 'NODE_COMPOSITING').action = 'Coll_Add'


class CopyEmptySMvigor(bpy.types.Operator):
    bl_idname = "object.copy_empty_sm_vigor"
    bl_label = "Copy Empty SM_Vigor"

    def execute(self, context):
        scene = context.scene
        input_text = scene.custom_panel_input

        if not input_text:
            input_text = 'SM_Vigor'

        # Specify the path to the source file
        source_file_path = os.path.join(
            bpy.utils.user_resource('SCRIPTS'),
            "addons",
            "Opusti_Tool",
            "data",
            "library.blend"
        )
        
        # Load the source file
        with bpy.data.libraries.load(source_file_path) as (data_from, data_to):
            # Ensure 'SM_Vigro' exists in the source file
            if 'SM_Vigro' in data_from.objects:
                # Copy the 'SM_Vigro' object
                data_to.objects = ['SM_Vigro']
        
        # Paste the copied object to the current scene
        for obj in data_to.objects:
            if obj is not None:
                # Rename the object to the input text
                obj.name = input_text
                scene.collection.objects.link(obj)
        
        scene.custom_panel_input = input_text  # Update the text box value
        
        return {'FINISHED'}
##-------------------------------------------------------------------- brick scatter and wood scatter
def assign_selected_vertices_to_group():##-------------------------- brick scatter and wood scatter
    obj = bpy.context.edit_object
    bpy.ops.object.vertex_group_assign()
def remove_selected_vertices_from_group():##-------------------------- brick scatter and wood scatter
    obj = bpy.context.edit_object
    bpy.ops.object.vertex_group_remove_from()
def delete_all_vertex_groups():##-------------------------- brick scatter and wood scatter
    obj = bpy.context.edit_object
    bpy.ops.object.vertex_group_remove(all=True)
def add_vertex_groups(names):##-------------------------- brick scatter and wood scatter
    obj = bpy.context.edit_object
    for name in names:
        obj.vertex_groups.new(name=name)
def has_geometry_nodes_modifier(obj): ##-------------------------- brick scatter and wood scatter
    """Check if the object has a Geometry Nodes modifier"""
    for modifier in obj.modifiers:
        if modifier.type == 'NODES':
            return True
    return False
class ScatterBrickWood(bpy.types.Panel):##-------------------------- brick scatter and wood scatter
    bl_idname = "VIEW3D_PT_scatter_brick_wood"
    bl_label = "Scatter BrickWood"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Combo Panel'
    #def draw(self, context):
     #   layout = self.layout
      #  layout.label(text="Scatter BrickWood panel content goes here")
    def draw_header(self, context):
        layout = self.layout
        #row = layout.row()
        row.label(text="Scatter_Brick&Wood", icon='PMARKER_SEL')
    def draw(self, context):
        layout = self.layout
        selected = context.selected_objects
        layout.enabled = getattr(context.active_object, "type", "") == "MESH" and context.active_object in selected
        if bpy.context.active_object is not None:
            if context.object and context.object.mode == "OBJECT":
                box = layout.box()
                row = box.row()
                row.operator('test.test_op', text='Add Wood', icon='SEQ_HISTOGRAM').action = 'ImportW'
                row = box.row()
                obj = context.object
                # Check if the first UV map is already named "UVmap01"
                if obj.data.uv_layers and obj.data.uv_layers[0].name == "UVmap01":
                    row.operator("object.remove_material_slots", text="Done")
                else:
                    row.operator("object.remove_material_slots", text="Convert to Mesh")
        if bpy.context.active_object is not None:            
            if context.object.mode == "EDIT":
                #print ("Int")
                box = layout.box()
                row = box.row()
                obj = context.active_object
                if has_geometry_nodes_modifier(obj):
                    box.label(text="Object has Geometry Nodes")
                else:
                    box.operator('test.test_op', text='Add Bricks', icon='ALIGN_FLUSH').action = 'ImportB'

                obj = bpy.context.edit_object
                if obj:
                    vertex_groups = obj.vertex_groups

                    for group in vertex_groups:
                        row = box.row()
                        row.label(text=group.name)

                        # Assign button
                        assign_op = row.operator("object.assign_vertex_group", text="", icon="ADD")
                        assign_op.group_index = group.index

                    # Delete all vertex groups button
                    if obj and obj.type == 'MESH' and obj.vertex_groups:
                        box.operator("object.delete_all_vertex_groups", text="Delete All Vertex Groups")
                    else:
                        box.label(text="No Vertex Groups")
                    # Add vertex groups button
                        box.operator("object.add_vertex_groups", text="Add Vertex Groups")
class OBJECT_OT_AssignVertexGroup(bpy.types.Operator):##-------------------------- brick scatter and wood scatter
    bl_idname = "object.assign_vertex_group"
    bl_label = "Assign Vertex Group"
    group_index: bpy.props.IntProperty()
    def execute(self, context):
        remove_selected_vertices_from_group()
        obj = bpy.context.edit_object
        obj.vertex_groups.active_index = self.group_index
        assign_selected_vertices_to_group()
        return {'FINISHED'}
class OBJECT_OT_RemoveVertexGroup(bpy.types.Operator):##-------------------------- brick scatter and wood scatter
    bl_idname = "object.remove_vertex_group"
    bl_label = "Remove Vertex Group"
    group_index: bpy.props.IntProperty()

    def execute(self, context):
        obj = bpy.context.edit_object
        obj.vertex_groups.active_index = self.group_index
        remove_selected_vertices_from_group()
        return {'FINISHED'}
class OBJECT_OT_DeleteAllVertexGroups(bpy.types.Operator):##-------------------------- brick scatter and wood scatter
    bl_idname = "object.delete_all_vertex_groups"
    bl_label = "Delete All Vertex Groups"

    def execute(self, context):
        delete_all_vertex_groups()
        return {'FINISHED'}
class OBJECT_OT_AddVertexGroups(bpy.types.Operator):##-------------------------- brick scatter and wood scatter
    bl_idname = "object.add_vertex_groups"
    bl_label = "Add Vertex Groups"
    names: bpy.props.StringProperty(default="Vertical,Horizontal,SingleX,SingleY,Random 90,Random 45")
    def execute(self, context):
        names = self.names.split(",")
        add_vertex_groups(names)
        bpy.ops.object.custom_operatorvertexgroupbrick()
        return {'FINISHED'}
##---------------------------------------------------------------------brick scatter and wood scatter
class VertexColors(bpy.types.Panel): ##--------------Vertex Colors
    bl_idname = "VIEW3D_PT_vertex_colors"
    bl_label = "Vertex Colors"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Combo Panel'

    def draw_header(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Vertex colors", icon='COLOR')

    def invoke(self, context, event):
        wn = context.window_manager
        return wn.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        selected = context.selected_objects
        layout.enabled = getattr(context.active_object, "type", "") == "MESH" and context.active_object in selected
        scene = context.scene
        obj = context.object
        
        row = layout.row(align=True)
        col = row.column(align=True)
        col.operator('test.test_op', text='Show', icon='PROP_ON').action = 'VCshow'
        col = row.column(align=True)
        col.operator('test.test_op', text='Flat').action = 'VCflat'
        col = row.column(align=True)
        col.operator('test.test_op', text='Hide', icon='PROP_CON').action = 'VChi'
        
        if bpy.context.active_object is not None:
            if context.object.mode == "EDIT":
                #print("Int")
                row = layout.row()
                row.prop(context.scene, "mytool_color")
                
                row = layout.row()
                row.operator(SimpleOperator.bl_idname)
                
                row = layout.row(align=True)
                col1 = row.column(align=True)
                col1.operator('test.test_op', text='+ Faces', icon='OBJECT_DATAMODE').action = 'VCface'
                col1 = row.column(align=True)
                col1.operator('test.test_op', text='+ Vertices', icon='EDITMODE_HLT').action = 'VCvertex'
            else:  
                row = layout.row()
                row.operator('test.test_op', text='Clear', icon='GPBRUSH_ERASE_STROKE').action = 'ClearVertexColor'
class SimpleOperator(bpy.types.Operator): ##---------Vertex Colors
    bl_idname = "object.simple_operator"
    bl_label = "Simple Operator"
    def execute(self, context):
        # Add your operator's functionality here
        return {'FINISHED'}

class SettingOrUpdate(bpy.types.Panel): ##-----------Setting or Update
    bl_idname = "VIEW3D_PT_setting_or_update"
    bl_label = "Setting or Update"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Combo Panel'

    def draw_header(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Setting", icon="FILE_SCRIPT")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        opusti_tool = scene.opusti_tool
        #-------------------------Update addons
        row = layout.row(align=True)
        col1 = row.column(align=True)
        iconReload = Opus_Utility.pcoll["icon_reload"]
        col1.operator("wm.update_check_operator", text="Check for Updates", icon_value=iconReload.icon_id)
        col1.scale_y = 0.9
        col1.scale_x = 1
        text_list = col1.template_list("TEXT_UL_red_text_list", "", bpy.context.scene, "custom_addon_red_text_enum", bpy.context.scene, "custom_addon_red_text_enum_index")
        iconDownload = Opus_Utility.pcoll["icon_update"]
        col1.operator("wm.install_addon_operator", text="Download and Install", icon_value=iconDownload.icon_id)
        iconReopen = Opus_Utility.pcoll["icon_reopen"]
        col1.operator("object.auto_reopen_panel", text="Reopen Blender", icon_value=iconReopen.icon_id)
        
        # Check if the list has items
        if text_list:
            # Get the selected item
            selected_item = bpy.context.scene.custom_addon_red_text_enum[bpy.context.scene.custom_addon_red_text_enum_index]
            
            # Display the selected item's text content up to the '=' symbol
            display_text = selected_item['text'].split('=')[0].strip()
            layout.label(text=f"Selected Text: {display_text}")
        #-------------Add Exporter preset for substance painter
        box = layout.box()
        row = box.row(align=True)
        ExPainter = row.column(align=True)
        ExPainter.label(text="Exporter for substance painter")
        iconSetting2 = Opus_Utility.pcoll["icon_setting2"]
        ExPainter.operator("wm.copy_file_preset_export_painter_operator", text="Install Exporter", icon_value=iconSetting2.icon_id)
        #--------------------------------------
        box = layout.box()
        row = box.row(align=True)
        col2 = row.column(align=True)
        col2.label(text="Shortcut for Pie Menu")
        col2.prop(opusti_tool, "shortcut_name", icon='KEYINGSET')
        col2.operator("text.save_shortcut", text="Save Shortcut", icon="KEY_HLT")
        # Display the saved shortcut text
        saved_shortcut_text = opusti_tool.read_saved_shortcut_text()
        col2.label(text="Currently Shortcut : "+saved_shortcut_text)
        
        # Add text input for the base folder path
        box = layout.box()
        row = box.row(align=True)
        col3 = row.column(align=True)
        col3.prop(context.scene, "base_folder_path", text="")
        col3.operator("text_data.save_operator", text="Update Material from Enfusion")

        box = layout.box()
        row = box.row(align=True)
        col4 = row.column(align=True)
        col4.label(text="last Import: " + context.scene.my_label_text.split('_')[0])
        col4.operator("object.read_meta_file", text="Add personal material", icon="ADD")
        iconSetting1 = Opus_Utility.pcoll["icon_setting1"]
        col4.operator("object.popup_dialog", text="list & Remove", icon_value=iconSetting1.icon_id)
        col4.operator("object.copy_text_to_collision_mat", text="Restore from backup")
class DayZ(bpy.types.Panel):#---------------UV Maps
    bl_idname = "VIEW3D_PT_DayZ"
    bl_label = "DayZ"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Combo Panel'
    #def draw(self, context):
     #   layout = self.layout
      #  layout.label(text="UV Maps panel content goes here")
    def draw_header(self, context):
        layout = self.layout
        row = layout.row()
        #row.label(text="UV Maps", icon='UV')
        icon = Opus_Utility.pcoll["icon_dayz"]
        row.label(text="DayZ", icon_value=icon.icon_id)

    def draw(self, context):
        #layout = self.layout
        #scene = context.scene#--
        #obj = context.object
        #selected = context.selected_objects
        #layout.enabled = getattr(context.active_object, "type", "") == "MESH" and context.active_object in selected
        layout = self.layout
        scene = context.scene
        collection = bpy.context.collection  # Get the currently selected collection
        selected = context.selected_objects
        # Check if the active object is in the desired collection and it's a mesh
        enable_button = collection and getattr(context.active_object, "type", "") == "MESH" and context.active_object in selected

        # Add a new button without any functionality
        if enable_button: #click model
            #row = layout.row()
            if bpy.context.active_object is not None:
                if context.object and context.object.mode == "OBJECT":
                    box = layout.box()
                    row = box.row(align=True)
                    colBat = row.column(align=True) 
                    colBat.label(text="DayZ Tools( ͡° ͜ʖ ͡°)")

                    iconmulti = Opus_Utility.pcoll["icon_multi"]
                    iconsingle = Opus_Utility.pcoll["icon_single"]
                    iconca = Opus_Utility.pcoll["icon_ca"]
                    iconrvmat = Opus_Utility.pcoll["icon_rvmat"]
                    iconmaterial1 = Opus_Utility.pcoll["icon_material1"]
                    iconroadway = Opus_Utility.pcoll["icon_roadway"]
                    iconfiregeo = Opus_Utility.pcoll["icon_firegeo"]
                    iconmision = Opus_Utility.pcoll["icon_mission"]

                    #colBat.operator("wm.run_exe_tools_dayz", text='DayZ Tool EXE', icon='GHOST_ENABLED')
                    icon = Opus_Utility.pcoll["icon_dayz"]
                    colBat.operator("wm.run_exe_tools_dayz", text='DayZ Tool EXE', icon_value=icon.icon_id)
                    row = box.row(align=True)
                    colBat.operator("dayz.update_mission", text='Update mission map', icon_value=iconmision.icon_id)
                    # Add a dropdown menu to the panel for .rvmat files
                    row = box.row(align=True)
                    colBatt = row.column(align=True) 
                    colBatt.prop(context.scene, "custom_rvmat_list", text='', icon_value=iconfiregeo.icon_id)
                    # Add a button to create and assign the .rvmat material
                    colBatt.operator("custom.create_assign_material", text='Assign FireGeometry', icon='ADD')

                    row = box.row(align=True)
                    colBat1 = row.column(align=True) 
                    # Add a dropdown menu to the panel for .tga files
                    colBat1.prop(context.scene, "custom_tga_list", text='', icon_value=iconroadway.icon_id)
                    # Add a button to create and assign the .tga material
                    colBat1.operator("custom.create_assign_tga_material", text='Assign Roadway', icon='ADD')

                    box = layout.box()
                    row = box.row(align=True)
                    row.label(text="Path CO.tga file or Emtry")
                    row = box.row(align=True)
                    colBat3 = row.column(align=True)
                    colBat3.prop(context.scene, "custom_text_box", text='')
                    colBat3 = row.column(align=True)
                    colBat3.scale_x=0.15
                    colBat3.operator("custom.select_tga", text="...")

                    row = box.row(align=True)
                    colBat2 = row.column(align=True) 
                    # Add a TextBox for entering a directory path
                    colBat2.label(text="Path of your Rvmat")
                    colBat2.prop(context.scene, "custom_directory_path", text='')

                    # Add a button to read .rvmat file names and save to SaveRvmat.txt
                    iconUpload = Opus_Utility.pcoll["icon_update"]
                    colBat2.operator("custom.read_rvmat_names_and_save", text='Save Path', icon_value=iconUpload.icon_id)

                    # Add a dropdown menu for New_menu_list
                    colBat2.prop(context.scene, "custom_new_menu_list", text="", icon_value=iconmaterial1.icon_id)
                    #colBat2.label(text="Path for CO if you need")

                    #row = box.row(align=True)
                    #colBat2 = row.column(align=True)
                    colBat2.operator("custom.create_assign_material_from_dropdown", text='Assign Rvmat', icon='ADD')

                    box = layout.box()
                    row = box.row(align=True)
                    colBat5 = row.column(align=True)
                    colBat5.operator("custom.delete_material_slots", text='Clear Slots')
                    colBat5.operator("object.clear_normal_pro", text='Clear NM Pro')
                    colBat5 = row.column(align=True)
                    colBat5.operator("object.fix_copied_materials", text='Del Useless')
                    colBat5.operator("object.get_sharp_pro", text='Get Sharp Pro')

                    row = box.row(align=True)
                    #imDzSmooth = row.column(align=True)
                    obj = context.active_object
                    if obj is not None:
                        imDzSmooth = row.column(align=True)
                        imDzSmooth.scale_x = 1.5
                        imDzSmooth.prop(obj.data, "auto_smooth_angle", text="Smooth")
                        imDzSmooth = row.column(align=True)
                        imDzSmooth.prop(obj.data, "use_auto_smooth", text="")
                    else:
                        layout.label(text="No active object selected")
                    #------------------------------------------------------------------Rvmat to material
                    box = layout.box()
                    row = box.row(align=True)
                    imDz = row.column(align=True) 
                    imDz.label(text="Convert Rvmat to Material")

                    row = box.row(align=True)
                    colBat6 = row.column(align=True) 
                    colBat6.operator("object.add_dayz_materialsuper", text='Super', icon_value=iconsingle.icon_id)
                    colBat6 = row.column(align=True) 
                    #colBat6.scale_x=0.4
                    colBat6.operator("object.add_dayz_materialsuperca", text='CA', icon_value=iconca.icon_id)
                    colBat6 = row.column(align=True) 
                    colBat6.operator("object.add_dayz_material", text='Multi', icon_value=iconmulti.icon_id)
                    # Add a textbox for entering the folder path
                    imDz.label(text="Folder Path Rvmat")
                    imDz.row(align=True)
                    imDz.prop(context.scene, "folder_path", text="")
                    iconReload = Opus_Utility.pcoll["icon_reload"]
                    imDz.operator("custom.save_folder_path", text="Update and Save Path", icon_value=iconReload.icon_id)
                    
                    row = box.row(align=True)
                    imDz1 = row.column(align=True) 
                    imDz1.scale_x=0.2
                    imDz1.label(text="Rvmat")
                    imDz1.label(text="Mat*")
                    imDz1 = row.column(align=True)
                    imDz1.prop(context.scene, "selected_rvmat", text="", icon_value=iconrvmat.icon_id)
                    imDz1.prop(context.scene, "selected_material", text="", icon_value=iconmaterial1.icon_id)

                    selected_material = context.scene.selected_rvmat
                    if selected_material:
                        row = box.row(align=True)
                        imDz2 = row.column(align=True)
                        imDz2.label(text="Location CO for super rvmat")
                        imDz2.prop(context.scene, "custom_text", text="")

                        imDz2.operator("custom.check_texture_nodes", text="Convert Super/CA to Mat", icon_value=iconsingle.icon_id)
                        imDz2.operator("custom.additional_button", text="Convert Multi to Mat", icon_value=iconmulti.icon_id)
                        row = box.row(align=True)
                        imDz3 = row.column(align=True)
                        imDz3.operator("custom.display_rvmat_content", text="Check text Rvmat")
                    #------------------------------------------------------------------Convert A3 to Dz and Copy file .tga and .Rvmat
                    box = layout.box()
                    row = box.row(align=True)
                    rvmat_conversion_column = row.column(align=True)
                    rvmat_conversion_column.label(text="Convert A3 to Dz")

                    # Add a textbox for entering the folder path
                    rvmat_conversion_column.label(text="Folder Path Rvmat")
                    rvmat_conversion_column.row(align=True)
                    rvmat_conversion_column.prop(context.scene, "folder_path_convert", text="")
                    rvmat_conversion_column.operator("custom.save_folder_pathconvert", text="Update and Save Path", icon_value=iconReload.icon_id)

                    row = box.row(align=True)
                    rvmat_info_column = row.column(align=True)
                    rvmat_info_column.prop(context.scene, "selected_rvmat_convert", text="", icon_value=iconrvmat.icon_id)

                    selected_material_convert = context.scene.selected_rvmat_convert
                    if selected_material_convert:
                        row = box.row(align=True)
                        rvmat_conversion = row.column(align=True)
                        rvmat_conversion.label(text="Folder Path to place filese")
                        rvmat_conversion.row(align=True)
                        rvmat_conversion.prop(context.scene, "target_folder_path", text="")
                        
                        row = box.row(align=True)
                        CopyAndConvert = row.column(align=True)
                        CopyAndConvert.operator("custom.copy_and_convert", text="Convert & Copy", icon='CON_TRACKTO')
                    
        else: #click collection
            row = layout.row()
            if bpy.context.active_object is not None:
                if context.object and context.object.mode == "OBJECT":
                    box = layout.box()
                    row = box.row(align=True)
                    colBat = row.column(align=True) 
                    colBat.label(text="DayZ Custom Only  ( ͡° ͜ʖ ͡°)")

                    iconDz = Opus_Utility.pcoll["icon_dayz"]
                    colBat.operator("wm.run_exe_tools_dayz", text='DayZ Tool EXE', icon_value=iconDz.icon_id)
                    # Add a button to the panel to export the active collection as FBX
                    row = box.row(align=True)
                    colBat1 = row.column(align=True)
                    iconDzExport = Opus_Utility.pcoll["icon_export"]
                    colBat1.operator("export.active_collection_fbx", text='Export FBX for DayZ', icon_value=iconDzExport.icon_id)
                    colBat1.label(text="Example Collection name")
                    colBat1.label(text="   --Name_LOD__0")
                    colBat1.label(text="   --Name_LODGeometry")
                    colBat1.label(text="   --Name_LODView_Geometry")
                    colBat1.label(text="   --Name_LODFire_Geometry")
                    colBat1.label(text="   --Name_LODRoadWay")
                    colBat1.label(text="   --Name_LODMemory")
                    row = box.row(align=True)
                    colBat2 = row.column(align=True)
                    colBat2.operator("myaddon.rename_objects_in_collection", text='Add Suffix to Objects inside', icon='TRACKING_FORWARDS_SINGLE')  # Add this line
                    colBat2.operator("myaddon.remove_suffix_operator", text='Remove Suffix from Objects inside', icon='TRACKING_CLEAR_BACKWARDS')  # Add this line

                    row = box.row(align=True)
                    colBat3 = row.column(align=True)
                    colBat3.prop(context.scene, "my_prefix", text="Name :")
                    colBat3.operator("object.organize_objects", text='Sort Objects', icon='RENDERLAYERS')   
        if bpy.context.active_object is not None:
            if context.object.mode == "EDIT":
                row = layout.row(align=True)
                row.scale_x = 0.5
                row.operator("view3d.wireframe_toggle", text="", icon="CUBE")
                row.scale_x = 0.5
                row.operator("view3d.wireframe_toggles", text="", icon="MESH_CUBE")
                ## Orientation
                space_data = context.space_data
                row.scale_x = 0.5
                row.prop(space_data.overlay, "show_face_orientation", text="", toggle=True, icon="OUTLINER_OB_LIGHTPROBE")
                ## UVs
                col = row.column(align=True)
                col.scale_x = 0.7  # Move the "Custom Origins" button by 0.5 (half of the available space)
                col.prop(scene.tool_settings, "use_transform_correct_face_attributes", text="", icon='OUTLINER_OB_LIGHT', toggle=True)
                col = row.column(align=True)
                col.scale_x = 0.3
                col.operator("object.my_operator", text="Correct UVs")
                # Threshold distance
                #box = layout.box()
                row = layout.row()
                row.prop(scene.tool_settings, "double_threshold", text="")
                # Auto Merge toggle
                row.prop(scene.tool_settings, "use_mesh_automerge", text="")
                # Get the operator's toggle property
                toggle_property = scene.create_toggle_transform_orientation

                row = layout.row(align=True)
                col5 = row.column(align=True)
                if bpy.context.active_object is not None:
                    if context.object.mode == "EDIT":
                        # Add the operator button
                        iconorient = Opus_Utility.pcoll["icon_orient"]
                        operator_props = col5.operator("object.create_toggle_transform_orientation", text="GetOrient", icon_value=iconorient.icon_id)
                        col5 = row.column(align=True)
                    iconglobal = Opus_Utility.pcoll["icon_global"]
                    operator_props = col5.operator("my_operator.button1", text="Global", icon_value=iconglobal.icon_id)
                row = layout.row(align=True)
                # Add the custom button using the provided code
                col1 = row.column(align=True)
                col1.scale_x = 0.5  # Move the "Custom Origins" button by 0.5 (half of the available space)
                col1.prop(scene.tool_settings, "use_transform_data_origin", text="", icon='OUTLINER_OB_LIGHT', toggle=True)

                # Add the custom operator button
                #row = layout.row(align=True)
                col1= row.column(align=True)
                col1.scale_x = 8  # Move the "My Button" by 1.0 (full available space)
                col1.operator("wm.my_button_operator", text="Custom Origins")

                iconseam = Opus_Utility.pcoll["icon_seam"]
                iconsharp = Opus_Utility.pcoll["icon_sharp"]
                iconboxclear = Opus_Utility.pcoll["icon_boxclear"]
                iconsplit = Opus_Utility.pcoll["icon_split"]

                box = layout.box()
                row = box.row()
                row.operator("mira.unbevel", text="Unbevel", icon="DRIVER_ROTATIONAL_DIFFERENCE")	
                row = box.row(align=True)
                col7 = row.column(align=True)
                iconshell = Opus_Utility.pcoll["icon_shell"]
                col7.operator("mesh.solidify", text='Shell', icon_value=iconshell.icon_id)
                col7.operator('test.test_op', text='Sharp', icon_value=iconsharp.icon_id).action = 'Sharp_O'
                col7.operator('mesh.mark_seam', text='Seam', icon_value=iconseam.icon_id)
                icongrow = Opus_Utility.pcoll["icon_grow"]
                col7.operator('mesh.select_more', text='Grow', icon_value=icongrow.icon_id)
                col7.operator('mesh.split', text='split', icon_value=iconsplit.icon_id)
                col7 = row.column(align=True)
                iconborders = Opus_Utility.pcoll["icon_borders"]
                col7.operator('test.test_op', text='Borders', icon_value=iconborders.icon_id).action = 'SelectedB'
                col7.operator('test.test_op', text='Clear Sharp', icon_value=iconboxclear.icon_id).action = 'ClearSharp'
                col7.operator('test.test_op', text='Clear Seam', icon_value=iconboxclear.icon_id).action = 'ClearSeam'
                iconreverse = Opus_Utility.pcoll["icon_reverse"]
                col7.operator('mesh.select_less', text='Reverse', icon_value=iconreverse.icon_id)   
                iconflip = Opus_Utility.pcoll["icon_flip"]
                col7.operator('test.test_op', text='Flip Faces', icon_value=iconflip.icon_id).action = 'FlipFaces'
                row = box.row(align=True)
                col8 = row.column(align=True)
                col8.operator('test.test_op', text='Ring', icon = 'COLLAPSEMENU').action = 'Cring'
                col8 = row.column(align=True)
                col8.operator('test.test_op', text='Loop', icon = 'REMOVE').action = 'Cloop'
                col8 = row.column(align=True)
                iconCD = Opus_Utility.pcoll["icon_CD"]
                col8.operator('test.test_op', text='CD', icon_value=iconCD.icon_id).action = 'Ccd'

class ComboPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_combo_panel"
    bl_label = ""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Opusti Tool'
    def draw_header(self, context):
        layout = self.layout
        row = layout.row()
        #row.label(text="Opusti Tools By Sunny", icon='KEYTYPE_EXTREME_VEC')
        icon = Opus_Utility.pcoll["icon_main"]
        row.label(text="Oputi Tools(by Sunny)", icon_value=icon.icon_id)
    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(context.scene, "Panel_Menu", expand=True)

        if context.scene.Panel_Menu == 'STATUS':
            layout.use_property_split = True
            layout.use_property_decorate = False
            #layout.label(text="Combo Panel with Status:")
            layout.separator()
            layout.scale_y = buttonY  # Adjust the size of the panel items
            layout.scale_x = buttonX  # Adjust the size of the panel items
            Status.draw(self, context)

        elif context.scene.Panel_Menu == 'UV_MAPS':
            layout.use_property_split = True
            layout.use_property_decorate = False
            #layout.label(text="UV Maps")
            layout.separator()
            layout.scale_y = buttonY  # Adjust the size of the panel items
            layout.scale_x = buttonX  # Adjust the size of the panel items
            UVMaps.draw(self, context)

        elif context.scene.Panel_Menu == 'FINDING_ERRORS':
            layout.use_property_split = True
            layout.use_property_decorate = False
            layout.label(text="Finding Errors")
            layout.separator()
            layout.scale_y = buttonY  # Adjust the size of the panel items
            layout.scale_x = buttonX  # Adjust the size of the panel items
            FindingErrors.draw(self, context)
            
            row = layout.row(align=True)
            row.prop(context.scene, "Check_Errors", expand=True)
            if context.scene.Check_Errors == 'Mesh':##---------------Finding Errors
                layout.use_property_split = True
                layout.use_property_decorate = False
                layout.separator()
                layout.scale_y = buttonY  # Adjust the size of the panel items
                layout.scale_x = buttonX  # Adjust the size of the panel items
                FindingErrorsMesh.draw(self, context)

            elif context.scene.Check_Errors == 'Materials':##---------------Finding Errors
                layout.use_property_split = True
                layout.use_property_decorate = False
                layout.separator()
                layout.scale_y = buttonY  # Adjust the size of the panel items
                layout.scale_x = buttonX  # Adjust the size of the panel items
                FindingErrorsMaterail.draw(self, context)

        elif context.scene.Panel_Menu == 'MAIN':
            layout.use_property_split = True
            layout.use_property_decorate = False
            #layout.label(text="Combo Panel with Main:")
            layout.separator()
            layout.scale_y = buttonY  # Adjust the size of the panel items
            layout.scale_x = buttonX  # Adjust the size of the panel items
            Main.draw(self, context)

        elif context.scene.Panel_Menu == 'SCATTER_BRICK_WOOD':
            layout.use_property_split = True
            layout.use_property_decorate = False
            layout.label(text="Scatter Woods and Bricks")
            layout.separator()
            layout.scale_y = buttonY  # Adjust the size of the panel items
            layout.scale_x = buttonX  # Adjust the size of the panel items
            ScatterBrickWood.draw(self, context)

        elif context.scene.Panel_Menu == 'VERTEX_COLORS':
            layout.use_property_split = True
            layout.use_property_decorate = False
            layout.label(text="Paint Vertex Colors")
            layout.separator()
            layout.scale_y = buttonY  # Adjust the size of the panel items
            layout.scale_x = buttonX  # Adjust the size of the panel items
            VertexColors.draw(self, context)

        elif context.scene.Panel_Menu == 'SETTING_OR_UPDATE':
            layout.use_property_split = True
            layout.use_property_decorate = False
            layout.label(text="Setting and Update addon")
            layout.separator()
            layout.scale_y = buttonY  # Adjust the size of the panel items
            layout.scale_x = buttonX  # Adjust the size of the panel items
            SettingOrUpdate.draw(self, context)
        if context.scene.Panel_Menu == 'DayZ':
            layout.use_property_split = True
            layout.use_property_decorate = False
            layout.separator()
            layout.scale_y = buttonY  # Adjust the size of the panel items
            layout.scale_x = buttonX  # Adjust the size of the panel items
            DayZ.draw(self, context)
