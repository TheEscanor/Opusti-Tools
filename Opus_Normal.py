import statistics

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class 
from . import Opus_Update
from . import Opus_Normal
from . import Opus_Utility
from . import Opus_ComboPanel
import bmesh
from mathutils import Vector, Matrix

triangle = 0
GetNum = 0
a = ""
col= ""
col_convert = ""
xx = ""
col_convert2 = ""
xx2= ""
xxDone= ""
ST = "new"
getName=""
#------------------------------------------import file
import sys
import os

PKG = PKG = __package__
#------------------------------------------End import file
class TEST_OT_test_op(bpy.types.Operator):
    bl_idname = 'test.test_op'
    bl_label = 'Test'
    
    
    action: EnumProperty(
        items=
        [
            ('R_Transfrom', 'R_Transfrom', 'R_Transfrom'),
            ('CLEARNORMAL', 'clear normal', 'clear normal'),
            ('ClearSharp', 'clear sharp', 'clear sharp'),
            ('Sharp_O', 'sharp O', 'sharp O'),
            ('ClearM', 'ClearM', 'ClearM'),
            ('P_X', 'P_X', 'P_X'),
            ('P_Y', 'P_Y', 'P_Y'),
            ('P_Z', 'P_Z', 'P_Z'),
            ('M_Dimensions', 'M_Dimensions', 'M_Dimensions'),
            ('alignToface', 'alignToface', 'alignToface'),
            ('P_cube', 'P_cube', 'P_cube'),
            ('P_cy', 'P_cy', 'P_cy'),
            ('P_Plane', 'P_Plane', 'P_Plane'),
            ('P_Circle', 'P_Circle', 'P_Circle'),
            ('originToface', 'originToface', 'originToface'),
            ('createDefault', 'createDefault', 'createDefault'),
            ('FlipFaces', 'FlipFaces', 'FlipFaces'),
            ('GetFaces', 'GetFaces', 'GetFaces'),
            ('WeightedNormal', 'WeightedNormal', 'WeightedNormal'),
            ('FaceOrientation', 'FaceOrientation', 'FaceOrientation'),
            ('SmartRepeat', 'SmartRepeat', 'SmartRepeat'),
            ('SmartRepeat25', 'SmartRepeat25', 'SmartRepeat25'),
            ('SelectedB', 'SelectedB', 'SelectedB'),
            ('COMbySelected', 'COMbySelected', 'COMbySelected'),
            ('ConUCX', 'ConUCX', 'ConUCX'),
            ('ConDe', 'ConDe', 'ConDe'),
            ('ClearSeam', 'ClearSeam', 'ClearSeam'),
            ('ClearVertexColor', 'ClearVertexColor', 'ClearVertexColor'),
            ('Coll_Add', 'Coll_Add', 'Coll_Add'),
            ('Coll_Reset', 'Coll_Reset', 'Coll_Reset'),
            ('FF_X', 'FF_X', 'FF_X'),
            ('FF_Y', 'FF_Y', 'FF_Y'),
            ('FF_Z', 'FF_Z', 'FF_Z'),
            ('Cring', 'Cring', 'Cring'),
            ('Cloop', 'Cloop', 'Cloop'),
            ('Ccd', 'Ccd', 'Ccd'),
            ('VCface', 'VCface', 'VCface'),
            ('VCvertex', 'VCvertex', 'VCvertex'),
            ('VCshow', 'VCshow', 'VCshow'),
            ('VCflat', 'VCflat', 'VCflat'),
            ('VChi', 'VChi', 'VChi'),
            ('P_all', 'P_all', 'P_all'),
            ('ImportB', 'ImportB', 'ImportB'),
            ('ImportW', 'ImportW', 'ImportW'),
            ('Decim_V2', 'Decim_V2', 'Decim_V2'),
            ('Half_LODs', 'Half_LODs', 'Half_LODs'),
        ]
    )
#---------------------------------------------------------------------------------------------------Normal function
    def execute(self, context):
        if self.action == 'CLEARNORMAL':
            self.clear_normal(context=context)
        elif self.action == 'ClearSharp':
            self.ClearSharp(context=context)
        elif self.action == 'Sharp_O':
            self.Sharp_O(context=context)
        elif self.action == 'ClearM':
            self.ClearM(context=context)
        elif self.action == 'P_X':
            self.P_X(context=context)
        elif self.action == 'P_Y':
            self.P_Y(context=context)
        elif self.action == 'P_Z':
            self.P_Z(context=context)
        elif self.action == 'M_Dimensions':
            self.M_Dimensions(context=context)
        elif self.action == 'R_Transfrom':
            self.R_Transfrom(context=context)
        elif self.action == 'alignToface':
            self.alignToface(context=context)
        elif self.action == 'P_cube':
            self.P_cube(context=context)
        elif self.action == 'P_cy':
            self.P_cy(context=context)
        elif self.action == 'P_Plane':
            self.P_Plane(context=context)
        elif self.action == 'P_Circle':
            self.P_Circle(context=context)
        elif self.action == 'originToface':
            self.originToface(context=context)
        elif self.action == 'createDefault':
            self.createDefault(context=context)
        elif self.action == 'FlipFaces':
            self.FlipFaces(context=context)
        elif self.action == 'GetFaces':
            self.GetFaces(context=context)
        elif self.action == 'WeightedNormal':
            self.WeightedNormal(context=context)
        elif self.action == 'FaceOrientation':
            self.FaceOrientation(context=context)
        elif self.action == 'SmartRepeat':
            self.SmartRepeat(context=context)
        elif self.action == 'SmartRepeat25':
            self.SmartRepeat25(context=context)
        elif self.action == 'SelectedB':
            self.SelectedB(context=context)
        elif self.action == 'COMbySelected':
            self.COMbySelected(context=context)
        elif self.action == 'ConUCX':
            self.ConUCX(context=context)
        elif self.action == 'ConDe':
            self.ConDe(context=context)
        elif self.action == 'ClearSeam':
            self.ClearSeam(context=context)
        elif self.action == 'ClearVertexColor':
            self.ClearVertexColor(context=context)
        elif self.action == 'Coll_Add':
            self.Coll_Add(context=context)
        elif self.action == 'Coll_Reset':
            self.Coll_Reset(context=context)
        elif self.action == 'FF_X':
            self.FF_X(context=context)
        elif self.action == 'FF_Y':
            self.FF_Y(context=context)
        elif self.action == 'FF_Z':
            self.FF_Z(context=context)
        elif self.action == 'Cring':
            self.Cring(context=context)
        elif self.action == 'Cloop':
            self.Cloop(context=context)
        elif self.action == 'Ccd':
            self.Ccd(context=context)
        elif self.action == 'VCface':
            self.VCface(context=context)
        elif self.action == 'VCvertex':
            self.VCvertex(context=context)
        elif self.action == 'VCshow':
            self.VCshow(context=context)
        elif self.action == 'VCflat':
            self.VCflat(context=context)
        elif self.action == 'VChi':
            self.VChi(context=context)
        elif self.action == 'P_all':
            self.P_all(context=context)
        elif self.action == 'ImportB':
            self.ImportB(context=context)
        elif self.action == 'ImportW':
            self.ImportW(context=context)
        elif self.action == 'Decim_V2':
            self.Decim_V2(context=context)
        elif self.action == 'Half_LODs':
            self.Half_LODs(context=context)
        return {'FINISHED'}
#---------------------------------------------------------------------------------------------------Normal
    @staticmethod
    def Half_LODs(context):
        s = bpy.context.scene.statistics(bpy.context.view_layer)
        tris = int(s.split("Tris:")[1].split(' ')[0].replace(',', '')) 
        converted_num_1 = f'{"{:,}".format(int(tris*0.5))}'
        triangle = converted_num_1
        def oops(self, context):
            self.layout.label(text="LOD1 : "+triangle)
        bpy.context.window_manager.popup_menu(oops, title="Result", icon='SCRIPT')
        return {'FINISHED'}
    @staticmethod
    def Decim_V2(context):
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].decimate_type = 'DISSOLVE'
        bpy.context.object.modifiers["Decimate"].angle_limit = 3.14159
        bpy.context.object.modifiers["Decimate"].delimit = {'UV'}
        return {'FINISHED'}
    @staticmethod
    def ImportW(context):
        # path to library.blend
        libraryPath = bpy.utils.user_resource('SCRIPTS', path="addons") + "\\" + PKG + "\\data\\library.blend"

        if not bpy.data.node_groups.get("Wood_scatter_KS"):
            with bpy.data.libraries.load(libraryPath,link=True) as (data_from, data_to):
                data_to.node_groups = ["Wood_scatter_KS"]
        # Get a reference to the selected object
        selected_object = bpy.context.object

        # Create a new Geometry Nodes modifier
        modifier = selected_object.modifiers.new(name="Geometry Nodes", type='NODES')

        # Get a reference to the existing node tree
        existing_node_tree = bpy.data.node_groups["Wood_scatter_KS"]

        # Set the node tree for the modifier
        modifier.node_group = existing_node_tree

        # Optionally, you can set other properties of the modifier
        # modifier.some_property = value

        # Update the scene to apply the changes
        bpy.context.view_layer.update()
        return {'FINISHED'}
    @staticmethod
    def ImportB(context):
        # path to library.blend
        libraryPath = bpy.utils.user_resource('SCRIPTS', path="addons") + "\\" + PKG + "\\data\\library.blend"
        if not bpy.data.node_groups.get("Bricks_scatter_KS"):
            with bpy.data.libraries.load(libraryPath,link=True) as (data_from, data_to):
                data_to.node_groups = ["Bricks_scatter_KS"]
        # Get a reference to the selected object
        selected_object = bpy.context.object

        # Create a new Geometry Nodes modifier
        modifier = selected_object.modifiers.new(name="Geometry Nodes", type='NODES')

        # Get a reference to the existing node tree
        existing_node_tree = bpy.data.node_groups["Bricks_scatter_KS"]

        # Set the node tree for the modifier
        modifier.node_group = existing_node_tree

        # Optionally, you can set other properties of the modifier
        # modifier.some_property = value

        # Update the scene to apply the changes
        bpy.context.view_layer.update()
        return {'FINISHED'}
    @staticmethod
    def clear_normal(context):
        selection = bpy.context.selected_objects
        for o in selection:
             try:
                 bpy.context.view_layer.objects.active = o
                 bpy.ops.mesh.customdata_custom_splitnormals_clear()
             except:
                 print("Object has no custom split normals: " + o.name + ", skipping")
                 
        return {'FINISHED'}

    @staticmethod
    def ClearSharp(context):
        bpy.ops.mesh.mark_sharp(clear=True)
        return {'FINISHED'}
    @staticmethod
    def Sharp_O(context):
        #bpy.ops.mesh.mark_sharp(clear=True)
        bpy.ops.mesh.mark_sharp()
        return {'FINISHED'}
    @staticmethod
    def ClearM(context):
        bpy.ops.object.remove_unused_materials()
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
        
    @staticmethod
    def P_X(context):
        bpy.ops.transform.resize(value=(0, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        return {'FINISHED'}
    @staticmethod
    def P_Y(context):
        bpy.ops.transform.resize(value=(1, 0, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        return {'FINISHED'}
    @staticmethod
    def P_Z(context):
        bpy.ops.transform.resize(value=(1, 1, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        return {'FINISHED'}
    @staticmethod
    def M_Dimensions(context):

        active = bpy.context.active_object
        selected = bpy.context.selected_objects

        for obj in selected:
            obj.dimensions = active.dimensions
        return {'FINISHED'}

    @staticmethod
    def R_Transfrom(context):

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.transforms_to_deltas(mode='ALL')
        bpy.ops.object.visual_transform_apply()
        bpy.ops.object.convert(target='MESH')
        return {'FINISHED'}
    @staticmethod
    def alignToface(context):
        context = bpy.context
        scene = context.scene
        cursor = scene.cursor
        ob = context.edit_object
        mw = ob.matrix_world

        me = ob.data
        bm = bmesh.from_edit_mesh(me)

        f = bm.select_history.active
        o = mw @ f.calc_center_median()
        f.normal_update()
        norm = (o + mw @ f.normal) - o

        q = norm.to_track_quat('Z', 'Y')

        M = q.to_matrix().to_4x4()
        M.translation = o
        cursor.matrix = M # does not work!! bummer

        cursor.location = o
        if cursor.rotation_mode == 'QUATERNION':
            cursor.rotation_quaternion = q
        elif cursor.rotation_mode == 'AXIS_ANGLE':
            cursor.rotation_axis_angle = q.to_axis_angle()
        else:
            cursor.rotation_euler = q.to_euler(cursor.rotation_mode)
        return {'FINISHED'}
        
    @staticmethod
    def P_cube(context):
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='CURSOR', scale=(1, 1, 1))

        return {'FINISHED'}
    @staticmethod
    def COMbySelected(context):
        #-----------get name collectin and removed usless word
        getName=""
        newDone = "neww"
        a=bpy.context.view_layer.active_layer_collection.collection
        #col = bpy.data.collections.get(a.name)
        col = bpy.data.collections.get(a.name)
        col_convert=f'{col}'
        xx = col_convert.split(')')[0]
        col_convert2=f'{xx}'
        xx2 = col_convert2.split('(')[1]
        xxDone = f'{xx2}'
        ST = col_convert2.split('"')[1]
        GetNameOfCollection = (('COM_')+(ST))
        #bpy.ops.wm.console_toggle()
        #print(ST)
        #--------------------------------------------
        #bpy.ops.object.editmode_toggle()
        #bpy.ops.mesh.select_all(action='SELECT')
        #bpy.ops.view3d.snap_cursor_to_selected()
        #bpy.ops.object.editmode_toggle()
        bpy.ops.object.apply_transforms()
        bpy.ops.view3d.snap_cursor_to_selected()
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='CURSOR',rotation=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = (GetNameOfCollection)

        return {'FINISHED'}
    @staticmethod
    def P_cy(context):
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, align='CURSOR', scale=(1, 1, 1))
        return {'FINISHED'}

    @staticmethod
    def P_Plane(context):
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='CURSOR', scale=(1, 1, 1))
        return {'FINISHED'}
    @staticmethod
    def P_Circle(context):
        bpy.ops.mesh.primitive_circle_add(radius=1, enter_editmode=False, align='CURSOR', scale=(1, 1, 1))
        return {'FINISHED'}
    @staticmethod
    def originToface(context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}
    @staticmethod
    def createDefault(context):
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = 0.5
        return {'FINISHED'}
    @staticmethod
    def FlipFaces(context):
        bpy.ops.mesh.flip_normals()
        return {'FINISHED'}
    @staticmethod
    def GetFaces(context):
        bpy.ops.mesh.set_normals_from_faces()
        return {'FINISHED'}
    @staticmethod
    def WeightedNormal(context):
        bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
        bpy.context.object.modifiers["WeightedNormal"].keep_sharp = True
        return {'FINISHED'}
    @staticmethod
    def FaceOrientation(context):
        if context.space_data.overlay.show_face_orientation == False:
            bpy.context.space_data.overlay.show_face_orientation = True
        elif context.space_data.overlay.show_face_orientation == True:
            bpy.context.space_data.overlay.show_face_orientation = False
        return {'FINISHED'}
    @staticmethod
    def SmartRepeat(context): #--------------------------------------------------SmartRepeat
        s = bpy.context.scene.statistics(bpy.context.view_layer)
        tris = int(s.split("Tris:")[1].split(' ')[0].replace(',', '')) 
               
        def oops(self, context):
            converted_num_0 = f'{"{:,}".format(int(tris))}'
            converted_num_1 = f'{"{:,}".format(int(tris*0.5))}'
            converted_num_2 = f'{"{:,}".format(int(tris/2/2))}'
            converted_num_3 = f'{"{:,}".format(int(tris/2/2/2))}'
            converted_num_4 = f'{"{:,}".format(int(tris/2/2/2/2))}'
            converted_num_5 = f'{"{:,}".format(int(tris/2/2/2/2/2))}'
            converted_num_6 = f'{"{:,}".format(int(tris/2/2/2/2/2/2))}'
            # print type of converted_num
            print(type(converted_num_1))
            
            self.layout.label(text="LOD0 : "+converted_num_0)
            self.layout.label(text="LOD1 : "+converted_num_1)
            self.layout.label(text="LOD2 : "+converted_num_2)
            self.layout.label(text="LOD3 : "+converted_num_3)
            self.layout.label(text="LOD4 : "+converted_num_4)
            self.layout.label(text="LOD5 : "+converted_num_5)
            self.layout.label(text="LOD6 : "+converted_num_6)

        bpy.context.window_manager.popup_menu(oops, title="Result", icon='SCRIPT')
        return {'FINISHED'}
    @staticmethod
    def SmartRepeat25(context): #--------------------------------------------------SmartRepeat
        ss = bpy.context.scene.statistics(bpy.context.view_layer)
        tris = int(ss.split("Tris:")[1].split(' ')[0].replace(',', '')) 
        
        def oops(self, context):
            converted_num_0 = f'{"{:,}".format(int(tris))}'
            converted_num_1 = f'{"{:,}".format(int(tris*0.25))}'
            converted_num_2 = f'{"{:,}".format(int(tris*0.0625))}'
            converted_num_3 = f'{"{:,}".format(int(tris*0.015625))}'
            
            
            self.layout.label(text="LOD0 : "+converted_num_0)
            self.layout.label(text="LOD1 : "+converted_num_1)
            self.layout.label(text="LOD2 : "+converted_num_2)
            self.layout.label(text="LOD3 : "+converted_num_3)
        bpy.context.window_manager.popup_menu(oops, title="Result", icon='SCRIPT')
               
        return {'FINISHED'}
    @staticmethod
    def SelectedB(context):
        bpy.ops.mesh.region_to_loop()

        return {'FINISHED'}
    @staticmethod
    def ClearSeam(context):
        bpy.ops.mesh.mark_seam(clear=True)

        return {'FINISHED'}
    @staticmethod
    def Coll_Add(context):
        newDone = "neww"
        a=bpy.context.view_layer.active_layer_collection.collection
        #col = bpy.data.collections.get(a.name)
        col = bpy.data.collections.get(a.name)
        col_convert=f'{col}'
        xx = col_convert.split(')')[0]
        col_convert2=f'{xx}'
        xx2 = col_convert2.split('(')[1]
        xxDone = f'{xx2}'

        for collection in bpy.data.collections:
            #ST = collection.name
            ST = (('"')+(collection.name)+('"'))
            if ST == xxDone:
                #------------------------------------
                getST=ST.replace('"', '')
                
                Coll_0 = ["_Coll", "_LOD0", "_LOD1", "_LOD2", "_LOD3", "_LOD4", "_LOD5", "_LOD6", "_LOD7"]
                for x in Coll_0: 
                    #if x == "Coll_0":
                    getX = f'{x}'
                    collection = bpy.context.blend_data.collections.new(name=getST+getX)
                    bpy.context.collection.children.link(collection)

        def oops(self, context):
            converted_num_0 = f'{xxDone}'
            self.layout.label(text=" = "+converted_num_0)

        bpy.context.window_manager.popup_menu(oops, title="Add", icon='SCRIPT')
        return {'FINISHED'}
    @staticmethod
    def Coll_Reset(context):
        def oops(self, context):
            converted_num_0 = f'{GetNum}'
            self.layout.label(text="GetNum = "+converted_num_0)

        bpy.context.window_manager.popup_menu(oops, title="Reset", icon='SCRIPT')
        return {'FINISHED'}
    @staticmethod
    def ClearVertexColor(context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.editmode_toggle()
        bpy.ops.paint.vertex_paint_toggle()
        bpy.data.brushes["Draw"].color = (1, 1, 1)
        bpy.data.brushes["Draw"].color = (1, 1, 1)
        bpy.context.object.data.use_paint_mask_vertex = True
        bpy.ops.paint.vertex_color_set()
        bpy.ops.paint.vertex_paint_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}
    @staticmethod
    def ConDe(context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.convex_hull()
        bpy.ops.object.editmode_toggle()
        
        return {'FINISHED'}
    @staticmethod
    def ConUCX(context):  
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = 0.1

        return {'FINISHED'}
    @staticmethod
    def FF_X(context):
        bpy.ops.transform.resize(value=(-1, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        return {'FINISHED'}
    @staticmethod
    def FF_Y(context):
        bpy.ops.transform.resize(value=(1, -1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        return {'FINISHED'}
    @staticmethod
    def FF_Z(context):
        bpy.ops.transform.resize(value=(1, 1, -1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        return {'FINISHED'}
    @staticmethod
    def Cring(context):
        bpy.ops.mesh.loop_multi_select(ring=True)
        return {'FINISHED'}
    @staticmethod
    def Cloop(context):
        bpy.ops.mesh.loop_multi_select(ring=False)
        return {'FINISHED'}
    @staticmethod
    def Ccd(context):
        bpy.ops.mesh.select_nth()
        return {'FINISHED'}
    @staticmethod
    def VCface(context):
        clr = context.scene.mytool_color
        bpy.ops.object.editmode_toggle()
        bpy.ops.paint.vertex_paint_toggle()
        bpy.context.object.data.use_paint_mask = True
        bpy.data.brushes["Draw"].color = (clr[0], clr[1], clr[2])
        bpy.ops.paint.vertex_color_set()
        bpy.ops.paint.vertex_paint_toggle()
        bpy.ops.object.editmode_toggle()
        def oops(self, context):
            converted_num_0 = "Faces"
            self.layout.label(text="Fill "+converted_num_0)

        bpy.context.window_manager.popup_menu(oops, title="Vertex Color", icon='SCRIPT')
        return {'FINISHED'}
    @staticmethod
    def VCvertex(context):
        clr = context.scene.mytool_color
        bpy.ops.object.editmode_toggle()
        bpy.ops.paint.vertex_paint_toggle()
        bpy.context.object.data.use_paint_mask_vertex = True
        bpy.data.brushes["Draw"].color = (clr[0], clr[1], clr[2])
        bpy.ops.paint.vertex_color_set()
        bpy.ops.paint.vertex_paint_toggle()
        bpy.ops.object.editmode_toggle()
        def oops(self, context):
            converted_num_0 = "Vertex"
            self.layout.label(text="Fill "+converted_num_0)

        bpy.context.window_manager.popup_menu(oops, title="Vertex Color", icon='SCRIPT')
        return {'FINISHED'}
    @staticmethod
    def VCshow(context):
        for area in bpy.context.screen.areas: 
                if area.type == 'VIEW_3D':
                    space = area.spaces.active
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'SOLID'
                        bpy.context.space_data.shading.light = 'STUDIO'
                        bpy.context.space_data.shading.color_type = 'VERTEX'
        def oops(self, context):
            converted_num_0 = "On"
            self.layout.label(text="Color "+converted_num_0)

        bpy.context.window_manager.popup_menu(oops, title="Vertex Color", icon='SCRIPT')
        return {'FINISHED'}
    @staticmethod
    def VCflat(context):
        for area in bpy.context.screen.areas: 
                if area.type == 'VIEW_3D':
                    space = area.spaces.active
                    if space.type == 'VIEW_3D':
                        print("test")
                        #space.shading.type = 'FLAT'
                        bpy.context.space_data.shading.light = 'FLAT'
        def oops(self, context):
            converted_num_0 = "On"
            self.layout.label(text="FLAT "+converted_num_0)

        bpy.context.window_manager.popup_menu(oops, title="Vertex Color", icon='SCRIPT')
        return {'FINISHED'}
    @staticmethod
    def VChi(context):
        for area in bpy.context.screen.areas: 
                if area.type == 'VIEW_3D':
                    space = area.spaces.active
                    if space.type == 'VIEW_3D':
                        bpy.context.space_data.shading.light = 'STUDIO'
                        bpy.context.space_data.shading.color_type = 'MATERIAL'
        def oops(self, context):
            converted_num_1 = "Off"
            self.layout.label(text="Color "+converted_num_1)

        bpy.context.window_manager.popup_menu(oops, title="Vertex Color", icon='SCRIPT')
        return {'FINISHED'}
    @staticmethod
    def P_all(context):
        bpy.ops.transform.resize(value=(0, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.resize(value=(1, 0, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.resize(value=(1, 1, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        return {'FINISHED'}

