import bpy
import os
import re
from bpy.types import Menu, Operator
import bpy.types
from . import Opus_Normal
from . import Opus_ui
from . import Opus_Utility
from . import Opus_Update
from . import Opus_ComboPanel
#---------------------------------------Shortcut
class TEXT_OT_SaveShortcut(bpy.types.Operator):#---- Shortcut Pie Menu
    bl_idname = "text.save_shortcut"
    bl_label = "Save Shortcut"
    bl_description = "After saving, your old key will still work. You need to reprogram the old key to not work."

    def execute(self, context):
        # Get the text from the dropdown menu
        shortcut_name = context.scene.opusti_tool.shortcut_name

        # Define the directory and file path
        version = bpy.app.version_string.split(' ')[0]  # Extract the version without additional info
        version = version.rsplit('.', 1)[0]  # Remove decimal point and trailing zeros
        directory = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Blender Foundation", "Blender", version, "scripts", "addons", "Opusti_Tool", "text_data")
        file_path = os.path.join(directory, "ShortCut.txt")

        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the shortcut name to the file
        with open(file_path, 'w') as file:
            file.write(shortcut_name)
        bpy.ops.script.reload()
        self.report({'WARNING'}, "Shortcut saved successfully! After saving, your old key will still work. You need to reprogram the old key to not work")
        bpy.ops.object.auto_reopen_panel()
        return {'FINISHED'}
class OpustiToolProperties(bpy.types.PropertyGroup):#---- Shortcut Pie Menu
    shortcut_name: bpy.props.EnumProperty(
        name="",
        items=[
            ("A", "A", "A"),
            ("B", "B", "B"),
            ("C", "C", "C"),
            ("D", "D", "D"),
            ("E", "E", "E"),
            ("F", "F", "F"),
            ("G", "G", "G"),
            ("H", "H", "H"),
            ("I", "I", "I"),
            ("J", "J", "J"),
            ("K", "K", "K"),
            ("L", "L", "L"),
            ("M", "M", "M"),
            ("N", "N", "N"),
            ("O", "O", "O"),
            ("P", "P", "P"),
            ("Q", "Q", "Q"),
            ("R", "R", "R"),
            ("S", "S", "S"),
            ("T", "T", "T"),
            ("U", "U", "U"),
            ("V", "V", "V"),
            ("W", "W", "W"),
            ("X", "X", "X"),
            ("Y", "Y", "Y"),
            ("Z", "Z", "Z"),
            ("SPACE", "Space", "Space"),
        ],
        default="SPACE"
    )

    def read_saved_shortcut_text(self):
        # Define the directory and file path
        version = bpy.app.version_string.split(' ')[0]  # Extract the version without additional info
        version = version.rsplit('.', 1)[0]  # Remove decimal point and trailing zeros
        directory = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Blender Foundation", "Blender", version, "scripts", "addons", "Opusti_Tool", "text_data")
        file_path = os.path.join(directory, "ShortCut.txt")

        # Read the text from the file
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read()

        return ""
class CustomPieMenuFavorites(bpy.types.Menu): #---------------Pie Menu Favorites
    bl_label = "Opusti Farovites"
    bl_idname = "OBJECT_MT_custom_pie_favorites"

    def draw(self, context):
        layout = self.layout
        sizeRow = 1.6
        pie = layout.menu_pie()
        # Define the number of buttons per row and the total number of buttons
        buttons_per_rowfavorites = 2
        total_buttonsfavorites = 6
        
        buttons_per_rowfavoritesEdit = 1
        total_buttonsfavoritesEdit = 4  
        # Define the icons for each button
        if bpy.context.active_object is not None:
            if context.object.mode == 'OBJECT':
                button_icons = ['KEYFRAME', 'MOD_SMOOTH', 'LIGHT_DATA', 'OUTLINER_OB_LIGHT', 'NETWORK_DRIVE', 'HAND']  # Add more icons as needed
                button_names = ['Remove Keyframe Anim', 'Auto Smooth Angle', 'lights off', 'lights on', 'Check Material','Rename Objects']  # Add more names as needed
                # Add buttons to the pie menu
                for i in range(total_buttonsfavorites):
                    if i % buttons_per_rowfavorites == 0:
                        row = pie.row(align=True)
                        row.scale_x = sizeRow -0.6
                        row.scale_y = sizeRow
                    op = row.operator("object.custom_pie_favorites", text=button_names[i], icon=button_icons[i])
                    op.button_index = i
            elif context.object.mode == 'EDIT':
                button_iconsEdit = ['ADD', 'REMOVE', 'MOD_SMOOTH', 'ERROR']  # Add more icons as needed
                button_namesEdit = ['Grow', 'Reverse', 'Auto Smooth Angle', 'Emtry']  # Add more names as needed
                # Add buttons to the pie menu
                for i in range(total_buttonsfavoritesEdit):
                    if i % buttons_per_rowfavoritesEdit == 0:
                        row = pie.row(align=True)
                        row.scale_x = sizeRow -0.6
                        row.scale_y = sizeRow
                    op = row.operator("object.custom_pie_favoritesedit", text=button_namesEdit[i], icon=button_iconsEdit[i])
                    op.button_indexedit = i
class CustomPieFavoritesOperator(bpy.types.Operator): #-------Favorite bject Mode 
    bl_idname = "object.custom_pie_favorites"
    bl_label = "Opusti Tools"
    button_index: bpy.props.IntProperty(default=0)
    def execute(self, context):
        # Call the corresponding function based on the button index
        button_functions = [self.function1, self.function2, self.function3, self.function4, self.FV_CheckMaterial, self.F_RenameSelected]  # Add more functions as needed
        if self.button_index < len(button_functions):
            button_functions[self.button_index]()
        return {'FINISHED'}

    # Define the functions to be called by the buttons
    def function1(self):
        bpy.ops.anim.keyframe_delete_v3d()
    def function2(self):
        bpy.ops.object.shade_smooth(use_auto_smooth=True)
        bpy.ops.object.open_dialog_quickfavorites()
    def function3(self):
        bpy.context.space_data.shading.use_scene_lights = False
        bpy.context.space_data.shading.use_scene_world = False
    def function4(self):
        bpy.context.space_data.shading.use_scene_lights = True
        bpy.context.space_data.shading.use_scene_world = True
    def FV_CheckMaterial(self):
        bpy.ops.object.open_dialog_rednamemb()
        bpy.ops.myaddon.read_models_operator()
    def F_RenameSelected(self):
        bpy.ops.object.open_dialog_rename()
class CustomPieFavoritesOperatorEdit(bpy.types.Operator): #---Favorite Edit Mode 
    bl_idname = "object.custom_pie_favoritesedit"
    bl_label = "Opusti Tools"
    button_indexedit: bpy.props.IntProperty(default=0)
    def execute(self, context):
        # Call the corresponding function based on the button index
        button_functionsEdit = [self.function1, self.function2, self.function3, self.function4]  # Add more functions as needed
        if self.button_indexedit < len(button_functionsEdit):
            button_functionsEdit[self.button_indexedit]()
        return {'FINISHED'}

    # Define the functions to be called by the buttons
    def function1(self):
        bpy.ops.mesh.select_more()
    def function2(self):
        bpy.ops.mesh.select_less()
    def function3(self):
        bpy.ops.object.open_dialog_quickfavorites()
    def function4(self):
        bpy.ops.mesh.faces_shade_flat()
##-----------------------------------------------------------------------------------------End Favorite Pie Menu
class CustomPieMenu(bpy.types.Menu): #-------------------Main Pie Menu
    bl_label = "Opusti Tools"
    bl_idname = "OBJECT_MT_custom_pie_menu"

    def draw(self, context):
        layout = self.layout
        # Create the pie menu layout
        pie = layout.menu_pie()
        # Size of buttons
        sizeRow = 1.6
        # Define the number of buttons per row and the total number of buttons
        Object_buttons_per_row = 2
        Object_total_buttons = 16  # Adjust the number of buttons as needed
        
        buttons_per_row = 3
        total_buttons = 19  # Adjust the number of buttons as needed
        # Define the icons for each button
        if bpy.context.active_object is not None:
            if bpy.context.object.mode == 'OBJECT' and bpy.context.area.type != 'IMAGE_EDITOR':
                Object_button_icons = [
                    'PREFERENCES', 'PREFERENCES', 'BRUSH_DATA', 'MOD_NORMALEDIT', 'ORIENTATION_GLOBAL', 'CUBE', 'MESH_CUBE',
                    'OUTLINER_OB_LIGHTPROBE', 'MODIFIER', 'CON_KINEMATIC', 'SYSTEM', 'HAND', 'HAND', 'HAND', 'MATERIAL', 'SOLO_ON'
                ]
                Object_button_names = [
                    'Reset All Transforms', 'Reset | Origin to Center', 'Clear Normals', 'Weighted Normal', 'Global',
                    'Wireframe toggle', 'Wireframe all', 'Face Orientation', 'Fix copied materials', 'Custom Origins',
                    'Smart Apply', 'Manual UBXs', 'Assign Material/Preset', 'COM/Optimize/Duplicate', 'Assigned materials from scene',
                    'Quick Favorites'
                ]
                # Add buttons to the pie menu
                for i in range(Object_total_buttons):
                    if i % Object_buttons_per_row == 0:
                        row = pie.row(align=True)
                        row.scale_x = sizeRow -0.6
                        row.scale_y = sizeRow 
                    opt = row.operator("object.custom_pie_operator_object", text=Object_button_names[i], icon=Object_button_icons[i])
                    opt.button_indexobject = i
            elif context.object.mode == 'EDIT'and context.area.type != 'IMAGE_EDITOR':
                button_icons = [
                    'MATCUBE', 'META_CUBE', 'SHADING_WIRE', 'SHADING_SOLID', 'COLLAPSEMENU', 'PAUSE', 'ALIGN_CENTER', 'OUTLINER_DATA_VOLUME', 'ORIENTATION_GLOBAL', 'NORMALS_FACE', 
                    'MOD_BEVEL', 'LIBRARY_DATA_BROKEN', 'AUTOMERGE_ON', 'MOD_UVPROJECT', 'INDIRECT_ONLY_ON', 'AXIS_SIDE', 'AXIS_FRONT', 'AXIS_TOP', 'SOLO_ON'
                ]
                button_names = [
                    'Mark Sharp', 'Clear Sharp', 'Mark Seam', 'Clear Seam', 'Rings', 'Loops', 'Checker Deselect', 'Borders', 'Global', 'Get Face/Edge', 'Unbevel', 'Splite', 'Auto Merge', 
                    'Correct UVs', 'Flip Faces', 'X', 'Y', 'Z', 'Quick Favorites'
                ]
                # Add buttons to the pie menu
                for i in range(total_buttons):
                    if i % buttons_per_row == 0:
                        row = pie.row(align=True)
                        row.scale_x = sizeRow -0.6
                        row.scale_y = sizeRow
                    op = row.operator("object.custom_pie_operator", text=button_names[i], icon=button_icons[i])
                    op.button_index = i          
class CustomPieOperatorObject(bpy.types.Operator):#------Main for Object Mode 
    bl_idname = "object.custom_pie_operator_object"
    bl_label = "Opusti Tools"

    button_indexobject: bpy.props.IntProperty(default=0)
    def execute(self, context):
        # Call the corresponding function based on the button index
        button_functionsObject = [
            self.function1, self.function2, self.function3, self.WeightedNormal, self.F_Global, self.F_Wireframe_toggle, self.F_Wireframe, self.F_face_orientation, 
            self.F_fix_copied_materials, self.F_CustomOrigin, self.F_AutoGenBoxes, self.F_GenUBXs, self.F_AssingMaterail, self.F_Main, self.F_AssignedMfromScene, self.F_quickfavorites
        ]  # Add more functions as needed
        if self.button_indexobject < len(button_functionsObject):
            button_functionsObject[self.button_indexobject]()
        return {'FINISHED'}

    # Define the functions to be called by the buttons
    def function1(self):
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.transforms_to_deltas(mode='ALL')
        bpy.ops.object.visual_transform_apply()
        bpy.ops.object.convert(target='MESH')
    def function2(self):
        bpy.ops.object.apply_transforms()
    def function3(self):
        selection = bpy.context.selected_objects
        for o in selection:
             try:
                 bpy.context.view_layer.objects.active = o
                 bpy.ops.mesh.customdata_custom_splitnormals_clear()
             except:
                 print("Object has no custom split normals: " + o.name + ", skipping")
    def WeightedNormal(self):#4
        bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
        bpy.context.object.modifiers["WeightedNormal"].keep_sharp = True
    def F_Global(self):
        bpy.ops.my_operator.button1()
    def F_Wireframe_toggle(self):
        bpy.ops.view3d.wireframe_toggle()
    def F_Wireframe(self):
        bpy.ops.view3d.wireframe_toggles()
    def F_face_orientation(self):
        bpy.ops.wm.toggle_face_orientation()
    def F_fix_copied_materials(self):
        bpy.ops.object.fix_copied_materials()
    def F_CustomOrigin(self):
        if bpy.context.scene.tool_settings.use_transform_data_origin == True:
            bpy.context.scene.tool_settings.use_transform_data_origin = False
        elif bpy.context.scene.tool_settings.use_transform_data_origin == False:
            bpy.context.scene.tool_settings.use_transform_data_origin = True
    def F_AutoGenBoxes(self):
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            # Apply all modifiers
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.convert(target='MESH')
    def F_GenUBXs(self):
        bpy.ops.object.open_dialog_operator()
    def F_AssingMaterail(self):
        bpy.ops.object.open_dialog_assignmaterial()
    def F_Main(self):
        bpy.ops.object.open_dialog_main()
    def F_AssignedMfromScene(self):
        bpy.ops.custom.custom_materailfromsence('INVOKE_DEFAULT')
    def F_quickfavorites(self):
        bpy.ops.wm.call_menu_pie(name="OBJECT_MT_custom_pie_favorites")
class CustomPieOperator(bpy.types.Operator):#------------Main for Edit Mode
    bl_idname = "object.custom_pie_operator"
    bl_label = "Opusti Tools"

    button_index: bpy.props.IntProperty(default=0)
    def execute(self, context):
        # Call the corresponding function based on the button index
        button_functions = [
            self.function1, self.function2, self.function3, self.function4, self.F_Rings, self.F_Loops, self.F_CheckerDeselect, self.F_Borders, self.F_Global, self.F_Orientation, self.F_Unbevel,
            self.F_Split, self.F_Reverse, self.F_Grow, self.F_FlipFaces, self.P_X, self.P_Y, self.P_Z, self.F_quickfavorites
        ]
        if self.button_index < len(button_functions):
            button_functions[self.button_index]()
        return {'FINISHED'}

    # Define the functions to be called by the buttons
    def function1(self):
        bpy.ops.mesh.mark_sharp()
    def function2(self):
        bpy.ops.mesh.mark_sharp(clear=True)
    def function3(self):
        bpy.ops.mesh.mark_seam(clear=False)
    def function4(self):
        bpy.ops.mesh.mark_seam(clear=True)
    def F_Rings(self):
        bpy.ops.mesh.loop_multi_select(ring=True)
    def F_Loops(self):
        bpy.ops.mesh.loop_multi_select(ring=False)
    def F_CheckerDeselect(self):
        bpy.ops.mesh.select_nth()
    def F_Borders(self):#8
        bpy.ops.mesh.region_to_loop()
    def F_Global(self):
        bpy.ops.my_operator.button1()
    def F_Orientation(self):
        bpy.ops.object.create_toggle_transform_orientation()
    def F_Unbevel(self):
        bpy.ops.mira.unbevel()
    def F_Grow(self): #-------UVs preserv
        bpy.context.scene.tool_settings.use_transform_correct_face_attributes = not bpy.context.scene.tool_settings.use_transform_correct_face_attributes
    def F_Reverse(self): #-----AutoMerge
        bpy.ops.object.open_dialog_automerge()
    def F_Split(self):
        bpy.ops.mesh.split()
    def F_FlipFaces(self):
        bpy.ops.mesh.flip_normals()
    def P_X(self):
        bpy.ops.transform.resize(value=(0, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        return {'FINISHED'}
    def P_Y(self):
        bpy.ops.transform.resize(value=(1, 0, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        return {'FINISHED'}
    def P_Z(self):
        bpy.ops.transform.resize(value=(1, 1, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        return {'FINISHED'}
    def F_quickfavorites(self):
        bpy.ops.wm.call_menu_pie(name="OBJECT_MT_custom_pie_favorites")
class OpenDialogOperator(bpy.types.Operator):#---------------Dialog for Gen UBXs
    bl_idname = "object.open_dialog_operator"
    bl_label = "Open Dialog"

    def execute(self, context):
        # Open the custom dialog
        bpy.ops.object.custom_dialog_operator('INVOKE_DEFAULT')

        return {'FINISHED'}
class CustomDialogOperator(bpy.types.Operator):#-------------Dialog for Gen UBXs
    bl_idname = "object.custom_dialog_operator"
    bl_label = "Manual create UBXs"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_tool = scene.my_tool
        tool_settings = scene.tool_settings
        #toggle_property = scene.create_toggle_transform_orientation
        
        box = layout.box()
        row = box.row()
        box.prop(scene.tool_settings, "use_transform_data_origin", text="Custom Origins", toggle=True)
        row.operator("object.custom_panel_operator", text="OrienVertex")
        row.operator("object.custom_panel_operatorface", text="OrienFace")
        row = box.row()
        row.operator("object.operator_loops_create_boxes_vertex", text="Coll.Vertex")
        row.operator("object.operator_loops_create_boxes", text="Coll.Face")
        row.operator("object.operator_loops_create_boxes_generate", text="", icon="SHADERFX")
        row = box.row()
        row.operator("object.create_cube", text="Create a box by selection", icon="META_CUBE")
class OpenDialogOperatorAssignMatPre(bpy.types.Operator):#-----Dialog for Assign material and Preset
    bl_idname = "object.open_dialog_assignmaterial"
    bl_label = "Open Dialog"

    def execute(self, context):
        # Open the custom dialog
        bpy.ops.object.custom_dialog_assignmaterial('INVOKE_DEFAULT')

        return {'FINISHED'}
class CustomDialogOperatorAssignMatPre(bpy.types.Operator):#---Dialog for Assign material and Preset
    bl_idname = "object.custom_dialog_assignmaterial"
    bl_label = "Manual Assign material/preset"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        box=layout.box()
        scene = context.scene
        mytool = scene.my_tool
        box.prop(mytool, "my_enum",icon='FILE_VOLUME')
        box.operator("addonname.myop_operator",icon = 'ADD')
                #-------------------------------------------Material Preset           
        mymaterial = scene.my_material
        box.prop(mymaterial, "my_enum_M",icon='SHADING_RENDERED')
        box.operator("material.myop_operator",icon = 'ADD')
class OpenDialogOperatorMain(bpy.types.Operator):#-------------Dialog for COM/Optimize/Duplicate Pro
    bl_idname = "object.open_dialog_main"
    bl_label = "Open Dialog"

    def execute(self, context):
        # Open the custom dialog
        bpy.ops.object.custom_dialog_main('INVOKE_DEFAULT')

        return {'FINISHED'}
class CustomDialogOperatorMain(bpy.types.Operator):#-----------Dialog for COM/Optimize/Duplicate Pro
    bl_idname = "object.custom_dialog_main"
    bl_label = "COM/Optimize/Duplicate Pro"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        row = layout.row()
        row.operator('test.test_op', text='LOD Default', icon = 'DUPLICATE').action = 'createDefault'
        row.operator('test.test_op', text='COM selected', icon = 'OUTLINER_DATA_EMPTY').action = 'COMbySelected'
        row = layout.row()
        row.operator('test.test_op', text='convexHull', icon = 'MESH_ICOSPHERE').action = 'ConDe'
        row.operator('test.test_op', text='Optimize', icon = 'MOD_DECIM').action = 'ConUCX'
        row = layout.row()
        row.operator("object.copy_rename", text="Duplicate_LODs")
        row.operator('test.test_op', text='OptimizeV2', icon = 'MOD_DECIM').action = 'Decim_V2'
        row = layout.row()
        row.operator('test.test_op', text='Create Collections LODs', icon = 'NODE_COMPOSITING').action = 'Coll_Add'
class OpenDialogOperatorAutoMerge(bpy.types.Operator):#--------Dialog for AutoMerge
    bl_idname = "object.open_dialog_automerge"
    bl_label = "Open Dialog"

    def execute(self, context):
        # Open the custom dialog
        bpy.ops.object.custom_dialog_automerge('INVOKE_DEFAULT')

        return {'FINISHED'}
class CustomDialogOperatorAutoMerge(bpy.types.Operator):#------Dialog for AutoMerge
    bl_idname = "object.custom_dialog_automerge"
    bl_label = "Auto Merge"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_tool = scene.my_tool
        tool_settings = scene.tool_settings
        #toggle_property = scene.create_toggle_transform_orientation
        
        box = layout.box()
        row = box.row()
        row.prop(scene.tool_settings, "double_threshold", text="Threshold Distance")
        # Auto Merge toggle
        row.prop(scene.tool_settings, "use_mesh_automerge", text="AutoMerge")
class OpenDialogOperatorRename(bpy.types.Operator):#----------Dialog for Rename
    bl_idname = "object.open_dialog_rename"
    bl_label = "Open Dialog"

    def execute(self, context):
        # Open the custom dialog
        bpy.ops.object.custom_dialog_rename('INVOKE_DEFAULT')

        return {'FINISHED'}
class CustomDialogOperatorRename(bpy.types.Operator):#--------Dialog for Rename
    bl_idname = "object.custom_dialog_rename"
    bl_label = "Rename Selection"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box = layout.box()
        row = box.row()
        row.prop(context.scene, "new_object_name")  # Use the scene property directly
        row = box.row()
        row.prop(context.scene, "suffix_text")  # New textbox for suffix text
        row = box.row()
        row.operator("object.rename_selected")
class MATERIALS_PT_ListMaterialsOperator(bpy.types.Operator):#----------Dialog for Assigned materials from existing ones in the scene
    bl_idname = "custom.custom_materailfromsence"
    bl_label = "Click material what you want to assign to selected models"
    bl_description="Select and assign existing materials in the scene to all remaining models."
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout

        # Get all the materials in the scene
        materials = bpy.data.materials

        # Display a list of clickable materials in the popup dialog
        for material in materials:
            layout.operator("custom.assign_material_operator", text=material.name).material_name = material.name
class CUSTOM_OT_AssignMaterialOperator(bpy.types.Operator):#------------Dialog for Assigned materials from existing ones in the scene
    bl_idname = "custom.assign_material_operator"
    bl_label = "Assign Material"

    material_name: bpy.props.StringProperty()

    def execute(self, context):
        material = bpy.data.materials.get(self.material_name)
        if material:
            selected_objects = bpy.context.selected_objects
            for obj in selected_objects:
                if obj.type == 'MESH':
                    obj.data.materials.clear()
                    obj.data.materials.append(material)
        return {'FINISHED'}
#----------------------------------------------------------------------------------------------Dialog Quick Favorites
class OpenDialogOperatorQuickFavorites(bpy.types.Operator): #---
    bl_idname = "object.open_dialog_quickfavorites"
    bl_label = "Open Dialog"

    def execute(self, context):
        bpy.ops.object.custom_dialog_quickfavorites('INVOKE_DEFAULT')
        return {'FINISHED'}
class CustomDialogOperatorQuickFavorites(bpy.types.Operator):
    bl_idname = "object.custom_dialog_quickfavorites"
    bl_label = "Auto Smooth"

    def execute(self, context):
        return {'FINISHED'}
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box = layout.box()
        obj = context.object
        row = box.row()
        row.prop(obj.data, "use_auto_smooth", text="")
        row.prop(obj.data, "auto_smooth_angle", text="Auto Smooth Angle")
        row = box.row()
        row.operator('test.test_op', text='ClearNormals', icon = 'MOD_PHYSICS').action = 'CLEARNORMAL'
        row = box.row()
        row.operator('test.test_op', text='WeightedNormal', icon = 'NORMALS_VERTEX_FACE').action = 'WeightedNormal'
        row = box.row()
        row.operator("object.remove_weighted_normal", icon='TRASH')
class RemoveWeightedNormalOperator(bpy.types.Operator):
    bl_idname = "object.remove_weighted_normal"
    bl_label = "Remove WeightedNormal"
    
    def execute(self, context):
        # Get the selected objects
        selected_objects = bpy.context.selected_objects
        
        # Iterate over selected objects
        for obj in selected_objects:
            # Iterate over object modifiers
            for modifier in obj.modifiers:
                if modifier.type == 'WEIGHTED_NORMAL':
                    # Remove the "WeightedNormal" modifier
                    obj.modifiers.remove(modifier)
        
        return {'FINISHED'}
class OpenDialogOperatorReadnameMB(bpy.types.Operator): #---read name object and check material
    bl_idname = "object.open_dialog_rednamemb"
    bl_label = "Open Dialog"
    bl_description="Check all models in this project to see which ones have assigned materials."
    def execute(self, context):
        bpy.ops.object.custom_dialog_rednamemb('INVOKE_DEFAULT')
        return {'FINISHED'}
class CustomDialogOperatorReadnameMB(bpy.types.Operator):#--read name object and check material
    bl_idname = "object.custom_dialog_rednamemb"
    bl_label = "check name ojbects/material"

    def execute(self, context):
        return {'FINISHED'}
    def invoke(self, context, event):
        # Adjust the width of the dialog by changing the value below (in pixels)
        return context.window_manager.invoke_props_dialog(self, width=800)
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Add operators
        row = layout.row()
        row.operator("myaddon.read_models_operator", text="Update")
        # Add text block to display the result
        row = layout.row()
        row.template_list("MY_UL_read_models_list", "", scene, "my_read_models_list", scene, "my_read_models_list_index")
class ReadModelsOperator(bpy.types.Operator):#--------------read name object and check material
    bl_idname = "myaddon.read_models_operator"
    bl_label = "Read Models"

    def execute(self, context):
        view_layer = context.view_layer

        # Clear the list before updating it
        context.scene.my_read_models_list.clear()

        for layer_col in get_all_children(view_layer.layer_collection):
            if not layer_col.exclude:
                entry = context.scene.my_read_models_list.add()
                entry.name = f"————◈ {layer_col.name}"#--------------Text of Collection
                for obj in layer_col.collection.objects:
                    if obj.material_slots:
                        for material_slot in obj.material_slots:
                            if material_slot.material:
                                if "usage" in obj:
                                    usage = obj["usage"]
                                else:
                                    usage = "No usage info"
                                entry = context.scene.my_read_models_list.add()
                                entry.name = f" ～{obj.name} ▚▚ Material :  {material_slot.material.name}   ▚▚ {usage}"
                    else:
                        if "usage" in obj:
                            usage = obj["usage"]
                        else:
                            usage = "No usage info"
                        entry = context.scene.my_read_models_list.add()
                        entry.name = f" ❎ {obj.name}  ▚▚ No Material Assigned   ▚▚ {usage}"

        return {'FINISHED'}
class MY_UL_read_models_list(bpy.types.UIList):#------------read name object and check material
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        # Display the collection name and object/material information in the list
        if item.name.startswith("Collection"):
            layout.label(text=item.name, icon='OBJECT_DATAMODE')
        else:
            layout.label(text=item.name)
    def invoke(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'DOUBLE_CLICK':
            # Handle double-click event here
            if context.object:
                obj_name = context.object.name
                for item in context.scene.my_read_models_list:
                    if item.name.startswith("Mesh") and obj_name in item.name:
                        context.scene.my_read_models_list_index = context.scene.my_read_models_list.find(item.name)
                        break

        return {'PASS_THROUGH'}
def get_all_children(col):#---------------------------------read name object and check material
    yield col
    for child in col.children:
        yield from get_all_children(child)
def count_materials(collection):#---------------------------read name object and check material
    materials = set()
    for obj in collection.collection.objects:
        if obj.material_slots:
            for material_slot in obj.material_slots:
                if material_slot.material:
                    materials.add(material_slot.material.name)
    return len(materials)
#-------------------------------------------------------------------------------------------------Quick Favorites