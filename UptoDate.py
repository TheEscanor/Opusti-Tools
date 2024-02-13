import bpy
import os
import urllib.request
import zipfile
from . import Opus_ComboPanel
import datetime
# ฟังก์ชันสำหรับแสดง Popup ข้อความ
def show_message_popup(context, title, message):
    def draw(self, context):
        self.layout.label(text=message)
        self.layout.operator("wm.update_operator", text="Update")
        self.layout.operator("wm.skip_operator", text="Skip")
        self.layout.operator("wm.alwaysskip_operator", text="Always Skip")


    bpy.context.window_manager.popup_menu(draw, title=title, icon='INFO')

class WM_OT_UpdateOperator(bpy.types.Operator):
    bl_idname = "wm.update_operator"
    bl_label = "Update Operator"
    bl_description = "Click the button to update to the latest version"
    def execute(self, context):
        try:
            download_path = "C:\\Users\\Public\\Documents\\Link.txt"
            # Download the file from Google Drive
            download_url = f"https://drive.google.com/uc?id=1BtlVhZ3yWBE28eUp8l0MRb7g0-wW9_Sj"
            urllib.request.urlretrieve(download_url, download_path)
            custom_message = "Default Message"  # Initialize with a default value
            if os.path.exists(download_path):
                # Read data from Link.txt
                with open(download_path, 'r') as file:
                    line_one = file.readline().strip()
                    if '=' in line_one:
                        custom_message = line_one.split('=')[1].strip()
                        #----------download big file
                        download_url = f"https://drive.google.com/uc?id={custom_message}"

                        # Download the zip file from the link
                        download_folder = bpy.path.abspath("//")  # Get the current blend file's directory
                        download_path = os.path.join(download_folder, "Opusti_Tool.zip")
                        urllib.request.urlretrieve(download_url, download_path)

                        # Extract the contents to the specified location
                        user_directory = bpy.utils.resource_path("USER")  # Get the user directory
                        
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

                        addon_directory = os.path.join(user_directory, "scripts", "addons")
                        with zipfile.ZipFile(download_path, 'r') as zip_ref:
                            zip_ref.extractall(addon_directory)
                        os.remove(download_path)
                        bpy.ops.object.auto_reopen_panel()
            self.report({'INFO'}, custom_message)
        except Exception as e:
            self.report({'ERROR'}, f" Please check your internet connection or Try to close the DayZ tools .exe, report the issue to Sunny")
        return {'FINISHED'}
    
# Custom Operator สำหรับปุ่ม "Skip"
class WM_OT_SkipOperator(bpy.types.Operator):
    bl_idname = "wm.skip_operator"
    bl_label = "Skip Operator"
    bl_description = "skip for now"
    def execute(self, context):
        file_path = "C:\\Users\\Public\\Documents\\OpusUptoDate.txt"
        with open(file_path, 'r') as file:
            lines = file.readlines()

        lines[1] = lines[1].replace("News", "Old")
        with open(file_path, 'w') as file:
            file.writelines(lines)
        return {'FINISHED'}
class WM_OT_AlwaysSkipOperator(bpy.types.Operator):
    bl_idname = "wm.alwaysskip_operator"
    bl_label = "Skip Operator"
    bl_description = "Always skip until updating to the new version manually"
    def execute(self, context):
        file_path = "C:\\Users\\Public\\Documents\\OpusUptoDate.txt"
        if os.path.exists(file_path):
            # Read data from OpusUptoDate.txt
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 3:
                    line_one = lines[0].strip()
                    line_two = lines[1].strip()
                    line_three = lines[2].strip()

                    # Write data to Version.txt
                    user_directory = bpy.utils.resource_path("USER")  # Get the user directory
                    addon_directory = os.path.join(user_directory, "scripts", "addons", "Opusti_Tool", "text_data", "Version.txt")

                    with open(addon_directory, 'w') as version_file:
                        version_file.write(line_three)

        return {'FINISHED'}
def check_download(download_url):
    try:
        urllib.request.urlopen(download_url)
        return True
    except Exception as e:
        print(f"Unable to download file from {download_url}: {e}")
        return False

def main_download():
    download_path = "C:\\Users\\Public\\Documents\\OpusUptoDate.txt"
    download_url = f"https://drive.google.com/uc?id=1FNqLBD58ZXqVKX3einTzynFt4XoZ7Ijt"

    today = datetime.date.today()

    file_path = "C:\\Users\\Public\\Documents\\Opus_SaveAday.txt"
    if os.path.exists(file_path):
        print("---------------------------------------------Get In")
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 1:
                    line_one = lines[0].strip()
                    if str(today) == line_one:
                        print("Nothing to download")
                    else:
                        print("Will be downloaded")
                        if check_download(download_url):
                            urllib.request.urlretrieve(download_url, download_path)
                            print("File downloaded successfully.")
                        else:
                            print("Download failed. Exiting...")
                            return {'FAILED'}
                        with open(file_path, 'w') as file:
                            file.write(str(today))
        print(f"Keep Day: {line_one} Today: {today}")
        
    else:
        print("---------------------------------------------Out Side")
        # Create the file if it doesn't exist
        with open(file_path, 'w') as file:
            file.write(str(today))
    
#def main_download():
#    download_path = "C:\\Users\\Public\\Documents\\OpusUptoDate.txt"
#    download_url = f"https://drive.google.com/uc?id=1FNqLBD58ZXqVKX3einTzynFt4XoZ7Ijt"
#    urllib.request.urlretrieve(download_url, download_path)
#    return {'FINISHED'}
def main_function():
    # ตรวจสอบว่ามี Object ที่ถูกเลือกหรือไม่
    if bpy.context.selected_objects:
        file_path = "C:\\Users\\Public\\Documents\\OpusUptoDate.txt"
        if os.path.exists(file_path):
            # Read data from OpusUptoDate.txt
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 3:
                    line_one = lines[0].strip()
                    line_two = lines[1].strip()
                    line_three = lines[2].strip()

                    # Read data from Version.txt
                    user_directory = bpy.utils.resource_path("USER")  # Get the user directory
                    addon_directory = os.path.join(user_directory, "scripts", "addons", "Opusti_Tool", "text_data", "Version.txt")

                    with open(addon_directory, 'r') as version_file:
                        version_lines = version_file.readlines()
                        # Compare line_three with an appropriate line from version_lines
                        if line_three == version_lines[0].strip():
                            custom_message = f"ข้อวามตรงกัน version:{version_lines}, UptoDate: {line_three}"
                        else:
                            custom_message = "อัพเดทเวอร์ชั่นใหม่ล่าสุด"
                            second_line = lines[1].strip() if len(lines) > 1 else ""
                            if "News" in second_line:
                                # เปลี่ยนคำว่า "News" เป็น "Old" ในบรรทัดที่ 2
                                if len(lines) > 1:
                                    #lines[1] = lines[1].replace("News", "Old")

                                    # เขียนข้อมูลที่ถูกแก้ไขลงในไฟล์
                                    with open(file_path, 'w') as file:
                                        file.writelines(lines)

                                    # แยกข้อความที่มีเครื่องหมาย "=" และแสดง Popup ข้อความ
                                    for line in lines:
                                        if "=" in line:
                                            key, value = map(str.strip, line.split("="))
                                            if key.lower() == "show":
                                                message_content = value
                                                show_message_popup(bpy.context, "News! Update from Opusti Tool", message_content)

                                else:
                                    # ถ้าไม่มีข้อมูลในไฟล์
                                    show_message_popup(bpy.context, "เกิดข้อผิดพลาด", "ไฟล์ไม่มีข้อมูล")
        else:
            # ถ้าไม่พบไฟล์
            show_message_popup(bpy.context, "เกิดข้อผิดพลาด", "ไม่พบไฟล์ที่ระบุ")
#---------------------------------------------------------------------------------------------------Update mission for DayZ
class Update_missionDayZ(bpy.types.Operator):
    bl_idname = "dayz.update_mission"
    bl_label = "Update mission map"
    bl_description = "Update the mission map from the cloud. If you have already downloaded it, please check for the last mission on the DayZ tool"
    def execute(self, context):
        download_url = "https://drive.google.com/uc?export=download&id=1xgql9pmFraXftKHfGYRP6j6BHpa93PLF"
        download_path = os.path.join(os.environ['USERPROFILE'], "Documents", "DayZ", "missions", "Sunny.SampleMap", "init.c")
        download_pathfloder = os.path.join(os.environ['USERPROFILE'], "Documents", "DayZ", "missions", "Sunny.SampleMap")
        
        if os.path.exists(download_pathfloder):
            try:
                urllib.request.urlretrieve(download_url, download_path)
                self.report({'INFO'}, "Mission map updated successfully!")
            except Exception as e:
                self.report({'ERROR'}, f"Failed to update mission map: {e}")
        else:
            os.makedirs(download_pathfloder)
            self.report({'ERROR'}, f"Ext")
            if os.path.exists(download_pathfloder):
                try:
                    urllib.request.urlretrieve(download_url, download_path)
                    self.report({'INFO'}, "Mission map updated successfully!")
                except Exception as e:
                    self.report({'ERROR'}, f"Failed to update mission map: {e}")  
        return {'FINISHED'}

