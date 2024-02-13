import bpy
import os
import urllib.request
import zipfile
from . import Opus_Normal
from . import Opus_ui
from . import Opus_Utility
from . import Opus_ComboPanel

class UpdateCheckOperator(bpy.types.Operator):
    bl_idname = "wm.update_check_operator"
    bl_label = "Update Check Operator"
    bl_description="Check the latest update from the cloud"
    def execute(self, context):
        # Check internet connection
        try:
            urllib.request.urlopen("http://google.com", timeout=1)
        except urllib.error.URLError:
            self.report({'ERROR'}, "Unable to check for updates. Please check your internet connection or report the issue to Sunny.")
            return {'CANCELLED'}
        
        # Define the file paths
        download_path = "C:\\Users\\Public\\Documents\\Link.txt"

        # Download the file from Google Drive
        download_url = "https://drive.google.com/uc?id=1uQ3XihKR7Ee3Seh9CmITp5K5QS6IsVah"
        urllib.request.urlretrieve(download_url, download_path)

        # Print a message to the console
        print(f"File downloaded and saved to {download_path}")

        # Read the content of the file
        with open(download_path, 'r') as file:
            file_content = file.readlines()

        # Add the content to the custom enum property
        bpy.context.scene.custom_addon_red_text_enum.clear()
        
        for i, line in enumerate(file_content):
            new_item = bpy.context.scene.custom_addon_red_text_enum.add()
            new_item.name = f"Line {i+1}"
            new_item['text'] = line.strip()

        bpy.context.scene.custom_addon_red_text_enum_index = 0

        return {'FINISHED'}

class InstallAddonOperator(bpy.types.Operator):
    bl_idname = "wm.install_addon_operator"
    bl_label = "Install Addon Operator"
    bl_description = "Download the selected version from the list"
    def execute(self, context):
        try:
            # Get the selected item
            selected_item = bpy.context.scene.custom_addon_red_text_enum[bpy.context.scene.custom_addon_red_text_enum_index]

            # Get the text content after '='
            download_link = selected_item['text'].split('=')[1].strip()
            download_url = f"https://drive.google.com/uc?id={download_link}"

            # Download the zip file from the link
            download_folder = bpy.path.abspath("//")  # Get the current blend file's directory
            download_path = os.path.join(download_folder, "Opusti_Tool.zip")
            urllib.request.urlretrieve(download_url, download_path)

            # Extract the contents to the specified location
            user_directory = bpy.utils.resource_path("USER")  # Get the user directory
            addon_directory = os.path.join(user_directory, "scripts", "addons")

            directory_icons = os.path.join(user_directory, "scripts", "addons", "Opusti_Tool", "icons")
            if os.path.exists(directory_icons):
                        # หากโฟลเดอร์มีไฟล์ภายใน
                for filename in os.listdir(directory_icons):
                    file_path = os.path.join(directory_icons, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            print(f"ลบไฟล์ '{filename}' เรียบร้อยแล้ว")
                    except Exception as e:
                        print(f"เกิดข้อผิดพลาดในการลบ '{filename}': {e}")
            else:
                print(f"โฟลเดอร์ '{directory_icons}' ไม่มีอยู่")

            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(addon_directory)

            # Print a message to the console
            self.report({'INFO'}, f"Downloaded and extracted to {addon_directory}")

            # Delete the downloaded zip file
            os.remove(download_path)
            bpy.ops.object.auto_reopen_panel()
        except Exception as e:
            self.report({'ERROR'}, f" Please check your internet connection or Try to close the DayZ tools .exe, report the issue to Sunny")
        return {'FINISHED'}

class RedTextMenu(bpy.types.UIList):
    bl_idname = "TEXT_UL_red_text_list"
    bl_label = "Red Text List"
    bl_description="Check"
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Display only the text content up to the '=' symbol
        display_text = item['text'].split('=')[0].strip()
        layout.label(text=display_text, translate=False)


