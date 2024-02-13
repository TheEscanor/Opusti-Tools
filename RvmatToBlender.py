import bpy
import os
import shutil
def initialize():
    # Your initialization code here
    print("RvmatToBlender addon initialized!")
class CustomAdditionalButton(bpy.types.Operator):
    bl_idname = "custom.additional_button"
    bl_label = "Your Additional Button"
    bl_description="The recommendation is similar to the 'Convert Super to Mat*' button. The difference with this button is that it's for multi-materials."
    def execute(self, context):
        # Get the selected material
        bpy.ops.object.rename_uv()
        selected_material_name = context.scene.selected_material
        selected_material = bpy.data.materials.get(selected_material_name)
        if selected_material:
            # Get the folder path from the scene properties
            folder_path = bpy.path.abspath(context.scene.folder_path)

            # Get the selected .rvmat file
            selected_rvmat = context.scene.selected_rvmat
            rvmat_file_path = os.path.join(folder_path, selected_rvmat)
            if os.path.exists(rvmat_file_path):
                with open(rvmat_file_path, 'r') as file:
                    # Read lines from the file
                    lines = file.readlines()

                    # Separate CO.tga lines based on their occurrence
                    co_lines = [line.strip() for line in lines if 'CO.tga' in line or 'co.tga' in line]
                    co_lines_mask = [line.strip() for line in lines if 'MASK.tga' in line or 'Mask.tga' in line or 'mask.tga' in line]
                    co_lines_ads = [line.strip() for line in lines if 'ADS.tga' in line or 'ads.tga' in line]
                    co_lines_mc = [line.strip() for line in lines if 'MC.tga' in line or 'mc.tga' in line]
                    # Update the texture nodes based on CO.tga lines
                    for index, co_line in enumerate(co_lines):
                        if index == 0:
                            # Replace Black node with the first CO.tga line
                            if selected_material.name == context.scene.selected_material:
                                self.update_texture_node(selected_material, 'Black', co_line)
                        elif index == 1:
                            # Replace Red node with the second CO.tga line
                            if selected_material.name == context.scene.selected_material:
                                self.update_texture_node(selected_material, 'Red', co_line)
                        elif index == 2:
                            # Replace Green node with the third CO.tga line
                            if selected_material.name == context.scene.selected_material:
                                self.update_texture_node(selected_material, 'Green', co_line)
                        elif index == 3:
                            # Replace Blue node with the fourth CO.tga line
                            if selected_material.name == context.scene.selected_material:
                                self.update_texture_node(selected_material, 'Blue', co_line)
                    for index, co_lines_mask in enumerate(co_lines_mask):
                        if index == 0:
                            # Replace Black node with the first CO.tga line
                            if selected_material.name == context.scene.selected_material:
                                self.update_texture_node(selected_material, 'Mask', co_lines_mask)
                    for index, co_lines_ads in enumerate(co_lines_ads):
                        if index == 0:
                            # Replace Black node with the first CO.tga line
                            if selected_material.name == context.scene.selected_material:
                                self.update_texture_node(selected_material, 'ADS', co_lines_ads)
                    for index, co_lines_mc in enumerate(co_lines_mc):
                        if index == 0:
                            # Replace Black node with the first CO.tga line
                            if selected_material.name == context.scene.selected_material:
                                self.update_texture_node(selected_material, 'MC', co_lines_mc)
        else:
            self.report({'WARNING'}, f"Selected material not found: {selected_material_name}")

        return {'FINISHED'}
    def update_texture_node(self, selected_material, node_name, co_line):
        # Check if the material uses nodes
        if selected_material.use_nodes:
            for node in selected_material.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.name == node_name:
                    # Get the new texture path from the CO.tga line
                    new_texture_path = co_line.replace('texture="', 'P:\\').replace('";', '')

                    # Update the texture file path of the node
                    node.image.filepath = new_texture_path

                    # Display a message in the info area
                    self.report({'INFO'}, f"Node: {node.name}, New Texture Path: {new_texture_path}")
class CustomSaveFolderPath(bpy.types.Operator):
    bl_idname = "custom.save_folder_path"
    bl_label = "Save folder_path"
    bl_description="Update ans Save Path, then Rvmat and Material will be update as well if the path it's correct"
    def execute(self, context):
        # Get the folder path from the scene properties
        folder_path = bpy.path.abspath(context.scene.folder_path)

        # Check if the folder path exists and is a directory
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Save folder_path to a file
            save_path = "C:\\Users\\Public\\Documents\\saveLrvmatDZ.txt"
            with open(save_path, 'w') as file:
                file.write(folder_path)

            self.report({'INFO'}, f"folder_path saved to {save_path}")

            # Update the list of .rvmat files in the folder
            update_rvmat_files(context)
        else:
            self.report({'ERROR'}, f" Invalid folder path: {folder_path}")

        return {'FINISHED'}
def update_rvmat_files(context):
    # รับเส้นทางของโฟลเดอร์ .rvmat จากฉากปัจจุบันใน Blender
    rvmat_folder = bpy.path.abspath(context.scene.folder_path)
    
    # ดึงรายการไฟล์ทั้งหมดในโฟลเดอร์ที่ระบุ
    rvmat_files = [f for f in os.listdir(rvmat_folder) if f.endswith(".rvmat")]

    # อัปเดต EnumProperty สำหรับ selected_rvmat
    bpy.types.Scene.selected_rvmat = bpy.props.EnumProperty(
        items=[(f, f, "") for f in rvmat_files],
        description="Select .rvmat File"
    )

    # อัปเดต EnumProperty สำหรับ selected_material
    bpy.types.Scene.selected_material = bpy.props.EnumProperty(
        items=[(mat.name, mat.name, "") for mat in bpy.data.materials],
        description="Select Material"
    )
#---------------------------------------------------------------------------------------------------------------CHeck texture Rvmat 
class CustomDisplayRvmatContent(bpy.types.Operator):
    bl_idname = "custom.display_rvmat_content"
    bl_label = "Display .rvmat Content"
    bl_description="Check all texture from the Rvmat selected on the list"
    def execute(self, context):
        # Get the folder path from the scene properties
        folder_path = bpy.path.abspath(context.scene.folder_path)

        # Check if folder path is valid
        if not os.path.exists(folder_path):
            self.report({'WARNING'}, "Folder path does not exist.")
            return {'CANCELLED'}

        # Get the selected .rvmat file
        selected_rvmat = context.scene.selected_rvmat

        # Check if selected_rvmat is not empty
        if not selected_rvmat:
            self.report({'WARNING'}, "No .rvmat file selected.")
            return {'CANCELLED'}
        rvmat_file_path = os.path.join(folder_path, selected_rvmat)

        if os.path.exists(rvmat_file_path):
            with open(rvmat_file_path, 'r') as file:
                # Read lines from the file
                lines = file.readlines()

                # Filter lines containing specific keywords
                keyword_lines = [line.strip() for line in lines if any(keyword in line for keyword in ['CO.tga', 'co.tga', 'MASK.tga', 'Mask.tga', 'mask.tga', 'ADS.tga', 'ads.tga', 'MC.tga', 'AS.tga', 'as.tga', 'MC.tga', 'mc.tga'])]

                # Join the filtered lines and display the result
                filtered_content = '\n'.join(keyword_lines)
                self.report({'INFO'}, f"Selected .rvmat Content:\n{filtered_content}")
                
        else:
            self.report({'WARNING'}, "Selected .rvmat file not found.")

        return {'FINISHED'}

class CustomLoadRvmat(bpy.types.Operator):
    bl_idname = "custom.load_rvmat"
    bl_label = "Load .rvmat File"

    def execute(self, context):
        # Get the selected material
        selected_material_name = context.scene.selected_material
        selected_material = bpy.data.materials.get(selected_material_name)

        if selected_material:
            self.report({'INFO'}, f"Selected Material: {selected_material_name}")

        # Get the selected .rvmat file
        selected_rvmat = context.scene.selected_rvmat
        rvmat_file_path = bpy.path.abspath(selected_rvmat)

        if os.path.exists(rvmat_file_path):
            self.report({'INFO'}, f"Selected .rvmat File: {selected_rvmat}")

            # Display the selected .rvmat file text in the info area
            bpy.context.window_manager.popup_menu(
                lambda self, context: self.layout.label(text=f"Selected .rvmat: {selected_rvmat}"),
                title="Info",
                icon='INFO'
            )

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Choose .rvmat file")

class CustomCheckTextureNodes(bpy.types.Operator):
    bl_idname = "custom.check_texture_nodes"
    bl_label = "Check Texture Nodes"
    bl_description="Before pressing this button, you should create a material from the button named 'Super or CA' and change the name to anything you like. Then, after that, press the button 'Update and Save path.' Next, select the Rvmat you want to import and choose 'Mat*' to select the material you just created to receive values from the Rvmat. Then, you can press 'Convert Super/CA to Mat*'."
    def execute(self, context):
        # Get the selected material
        bpy.ops.object.rename_uv()
        selected_material_name = context.scene.selected_material
        selected_material = bpy.data.materials.get(selected_material_name)

        if selected_material:
            # Get the folder path from the scene properties
            folder_path = bpy.path.abspath(context.scene.folder_path)

            # Get the selected .rvmat file
            selected_rvmat = context.scene.selected_rvmat
            rvmat_file_path = os.path.join(folder_path, selected_rvmat)
            
            if os.path.exists(rvmat_file_path):
                with open(rvmat_file_path, 'r') as file:
                    # Read lines from the file
                    lines = file.readlines()

                    # Separate CO.tga lines based on their occurrence
                    co_lines_mask = [line.strip() for line in lines if 'MASK.tga' in line or 'Mask.tga' in line or 'mask.tga' in line]
                    co_lines_ads = [line.strip() for line in lines if 'ADS.tga' in line or 'ads.tga' in line]
                    co_lines_ad = [line.strip() for line in lines if 'AS.tga' in line or 'as.tga' in line]
                    co_lines_mc = [line.strip() for line in lines if 'MC.tga' in line or 'mc.tga' in line]

                    for index, co_lines_mask in enumerate(co_lines_mask):
                        if index == 0:
                            # Replace Black node with the first CO.tga line
                            self.update_texture_node(selected_material, 'Mask', co_lines_mask)
                    for index, co_lines_ads in enumerate(co_lines_ads):
                        if index == 0:
                            # Replace Black node with the first CO.tga line
                            self.update_texture_node(selected_material, 'ADS', co_lines_ads)
                    for index, co_lines_ad in enumerate(co_lines_ad):
                        if index == 0:
                            # Replace Black node with the first CO.tga line
                            self.update_texture_node(selected_material, 'ADS', co_lines_ad)
                    for index, co_lines_mc in enumerate(co_lines_mc):
                        if index == 0:
                            # Replace Black node with the first CO.tga line
                            self.update_texture_node(selected_material, 'MC', co_lines_mc)
                            
            if os.path.exists(rvmat_file_path):
                with open(rvmat_file_path, 'r') as file:
                    # Read lines from the file
                    lines = file.readlines()

                    # Filter lines containing specific keywords
                    keyword_lines = [line.strip() for line in lines if any(keyword in line for keyword in ['CO.tga', 'co.tga', 'MASK.tga', 'Mask.tga', 'mask.tga', 'ADS.tga', 'ads.tga', 'MC.tga', 'AS.tga', 'as.tga', 'MC.tga', 'mc.tga'])]

                    # Join the filtered lines and display the result
                    filtered_content = '\n'.join(keyword_lines)

                    # Check material nodes for all texture nodes
                    message = f"Material: {selected_material_name}"
                    if selected_material.use_nodes:
                        for node in selected_material.node_tree.nodes:
                            if node.type == 'TEX_IMAGE':
                                # Display node name and original texture file path
                                original_texture_path = node.image.filepath if node.image else "N/A"
                                message += f"\nNode: {node.name}, Original Texture Path: {original_texture_path}"
                                # Update the texture file path if a valid keyword is found
                                if  node.name == 'Black':
                                    new_texture_path = context.scene.custom_text
                                    node.image.filepath = new_texture_path
                                    message += f"\nNode: {node.name}, New Texture Path: {new_texture_path}"
                    self.report({'INFO'}, message)
            else:
                self.report({'WARNING'}, "Selected .rvmat file not found.")
        else:
            self.report({'WARNING'}, f"Selected material not found: {selected_material_name}")

        return {'FINISHED'}
    def update_texture_node(self, selected_material, node_name, co_line):
        # Check if the material uses nodes
        if selected_material.use_nodes:
            for node in selected_material.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.name == node_name:
                    # Get the new texture path from the CO.tga line
                    new_texture_path = co_line.replace('texture="', 'P:\\').replace('";', '')

                    # Update the texture file path of the node
                    node.image.filepath = new_texture_path

                    # Display a message in the info area
                    self.report({'INFO'}, f"Node: {node.name}, New Texture Path: {new_texture_path}")
#---------------------------------------------------------------------------------------------------------------For Convert Rvmat from A3 to DayZ and Copy .tga file as well
class CopyAndConvertOperator(bpy.types.Operator):
    bl_idname = "custom.copy_and_convert"
    bl_label = "Copy and Convert"
    bl_description = "This button will copy the currently selected Rvmat and all textures inside of the Rvmat, then paste them to a new location"
    
    def execute(self, context):
        # Check if selected_rvmat is not None and not an empty string
        if context.scene.selected_rvmat_convert:
            # Get the source folder path and selected .rvmat file
            source_folder_path = bpy.path.abspath(context.scene.folder_path_convert)
            selected_rvmat = context.scene.selected_rvmat_convert
            rvmat_file_path = os.path.join(source_folder_path, selected_rvmat)

            # Get the target folder path
            target_folder_path = bpy.path.abspath(context.scene.target_folder_path)
            if not os.path.exists(target_folder_path):
                self.report({'WARNING'}, "Folder path to place the filese does not exist.")
                return {'CANCELLED'}
            # Construct the target .mat file path by replacing the extension
            target_mat_file_path = os.path.join(target_folder_path, os.path.splitext(selected_rvmat)[0] + ".rvmat")

            # Check if the source .rvmat file exists
            if os.path.exists(rvmat_file_path):
                # Copy the .rvmat file to the target folder
                shutil.copy(rvmat_file_path, target_mat_file_path)
                self.report({'INFO'}, f"Conversion successful. Copied {selected_rvmat} to {target_mat_file_path}")
                
                # Read the content of the created .mat file
                self.read_mat_file(target_mat_file_path, context)

                # Modify the copied .rvmat file to replace the paths
                self.modify_rvmat_file(target_mat_file_path, source_folder_path, target_folder_path)
                
                self.report({'INFO'}, "Conversion and Copying completed successfully.")
            else:
                self.report({'ERROR'}, f"Source .rvmat file not found: {rvmat_file_path}")

        else:
            self.report({'WARNING'}, "No Rvmat file selected. Please select an Rvmat file.")
        
        return {'FINISHED'}
    def read_mat_file(self, mat_file_path, context):
        # Check if the selected .mat file exists
        target_folder_path = bpy.path.abspath(context.scene.target_folder_path)
        
        if os.path.exists(mat_file_path):
            # Read the content of the .mat file
            with open(mat_file_path, 'r') as file:
                # Filter lines containing ".tga" but not containing "env_land_co.tga"
                tga_lines = [line.strip() for line in file.readlines() if '.tga' in line and 'env_land_co.tga' not in line and 'default_vehicle_ti_ca.tga' not in line]
            if tga_lines:
                processed_lines = []
                for line in tga_lines:
                    # Remove "texture=" from the beginning and everything after ";
                    processed_line = line.replace('texture="', 'P:\\').split('";')[0]
                    processed_lines.append(processed_line)
                    #----Copy .tga file
                    shutil.copy(processed_line, target_folder_path)
                    #self.report({'INFO'}, f"Copy from {processed_lines} (To) {target_folder_path}")
                processed_content = '\n'.join(processed_lines)
                #self.report({'INFO'}, f"Processed Content of {mat_file_path} (Lines with .tga):\n{processed_content}")
                self.report({'INFO'}, f"Texture list for convert:\n{processed_content}")
                # Copy files to the target folder
            else:
                self.report({'INFO'}, f"{mat_file_path} does not contain lines with '.tga' excluding 'env_land_co.tga'.")

        else:
            self.report({'ERROR'}, f"Selected .mat file not found: {mat_file_path}")

    def modify_rvmat_file(self, rvmat_file_path, old_source_path, new_target_path):
        # Read the content of the copied .rvmat file
        with open(rvmat_file_path, 'r') as file:
            rvmat_content = file.readlines()

        # Modify the paths in the content
        modified_content = []
        for line in rvmat_content:
            # Check if the line contains specific path
            if '.tga' in line and 'env_land_co.tga' not in line:
                # Extract the path within "texture=" and ";
                texture_path = line.split('texture="')[1].split('";')[0]

                # Replace the old source path with the new target path
                modified_path = os.path.join(new_target_path, os.path.basename(texture_path))
                modified_path = modified_path.replace('P:\\', '')

                # Replace the path in the line and append to modified content
                modified_line = f'\ttexture="{modified_path}";\n'
                modified_content.append(modified_line)
                #self.report({'INFO'}, f"TTTT:\n{modified_path}")
                self.report({'INFO'}, f"{modified_path}")
            elif 'A3\Data_f\env_land_co.tga' in line or 'A3\Data_f\env_land_co.paa' in line or 'A3\data_F\env_land_co.tga' in line or 'A3\data_F\env_land_co.paa' in line:
                modified_line = line.replace('A3\Data_f\env_land_co.tga', 'dz\data\data\env_land_co.tga')
                modified_line = modified_line.replace('A3\Data_f\env_land_co.paa', 'dz\data\data\env_land_co.paa')
                modified_line = modified_line.replace('A3\data_F\env_land_co.tga', 'dz\data\data\env_land_co.tga')
                modified_line = modified_line.replace('A3\data_F\env_land_co.paa', 'dz\data\data\env_land_co.paa')
                modified_content.append(modified_line)
                #self.report({'INFO'}, f"TTTT:\n{modified_line}")
            else:
                # Keep the line unchanged
                modified_content.append(line)

        # Write the modified content back to the .rvmat file
        with open(rvmat_file_path, 'w') as file:
            file.writelines(modified_content)
class LoadRvmatOperator(bpy.types.Operator):
    bl_idname = "custom.load_rvmat"
    bl_label = "Load .rvmat File"

    def execute(self, context):
        # Get the selected .rvmat file
        selected_rvmat = context.scene.selected_rvmat_convert
        rvmat_file_path = bpy.path.abspath(selected_rvmat)

        if os.path.exists(rvmat_file_path):
            self.report({'INFO'}, f"Selected .rvmat File: {selected_rvmat}")

            # Display the selected .rvmat file text in the info area
            bpy.context.window_manager.popup_menu(
                lambda self, context: self.layout.label(text=f"Selected .rvmat: {selected_rvmat}"),
                title="Info",
                icon='INFO'
            )

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Choose .rvmat file")


class SaveFolderPathOperator(bpy.types.Operator):
    bl_idname = "custom.save_folder_pathconvert"
    bl_label = "Save folder_path"
    bl_description = "Update and Save Path, then Rvmat list will be update if the path is correct"

    def execute(self, context):
        # Get the folder path from the scene properties
        folder_path = bpy.path.abspath(context.scene.folder_path_convert)

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            save_path = os.path.join(os.path.expanduser('~'), "Documents", "saveLrvmatConvert.txt")
            with open(save_path, 'w') as file:
                file.write(folder_path)

            self.report({'INFO'}, f"folder_path saved to {save_path}")

            # Update the list of .rvmat files in the folder
            update_rvmat_files_convert(context)
        else:
            self.report({'ERROR'}, f"Invalid folder path: {folder_path}")

        return {'FINISHED'}


def update_rvmat_files_convert(context):
    # Get the path of the folder containing .rvmat files from the current scene in Blender
    rvmat_folder = bpy.path.abspath(context.scene.folder_path_convert)

    # Get a list of all files in the specified folder
    rvmat_files = [f for f in os.listdir(rvmat_folder) if f.endswith(".rvmat")]

    # Update EnumProperty for selected_rvmat
    bpy.types.Scene.selected_rvmat_convert = bpy.props.EnumProperty(
        items=[(f, f, "") for f in rvmat_files],
        description="Select .rvmat File"
    )