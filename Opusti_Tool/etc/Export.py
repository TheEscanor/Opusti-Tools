from PySide2 import QtWidgets, QtGui
import substance_painter.ui
import substance_painter.export
import substance_painter.project
import substance_painter.textureset
import os

plugin_widgets = []
output_path = ""
texture_sizes_index = 2
texture_sizes = ["128x128", "256x256", "512x512", "1024x1024", "2048x2048", "4096x4096"]
def textureSize(size):
    if size == "128x128":
        return 7
    elif size == "256x256":
        return 8
    elif size == "512x512":
        return 9
    elif size == "1024x1024":
        return 10
    elif size == "2048x2048":
        return 11
    elif size == "4096x4096":
        return 12

def export_enfution(output_path, maps, selected_size):
    saveData(output_path)
    if not substance_painter.project.is_open():
        return

    stack = substance_painter.textureset.get_active_stack()
    material = stack.material()

    export_preset = substance_painter.resource.ResourceID(
        context="your_assets",
        name="A4"
    )
    resolution = material.get_resolution()

    # Use the provided output path or the project file path
    if output_path:
        Path = output_path
    else:
        Path = substance_painter.project.file_path()
        Path = os.path.dirname(Path) + "/"

    #project_output_directory = substance_painter.project.get_output_path()

    config = {
        "exportShaderParams": False,
        "exportPath": Path,
        "exportList": [{"rootPath": str(stack),
            "filter" : {
            "outputMaps" : [maps]
            }}],
        "exportPresets": [{"name": "default", "maps": []}],  # Specify the desired map name (e.g., "Diffuse")
        "defaultExportPreset": export_preset.url(),
        "exportParameters": [
            {
                "parameters": {"paddingAlgorithm": "infinite", "sizeLog2":textureSize(selected_size)}
            }
        ]
    }
    export_list = substance_painter.export.list_project_textures(config)
    print(export_list)
    substance_painter.export.export_project_textures(config)
    
    

def logX():
    for shelf in substance_painter.resource.Shelves.all():
        export_presets_dir = f"{shelf.path()}/export-presets"
        #print(shelf)
        if not os.path.isdir(export_presets_dir):
            continue
        for filename in os.listdir(export_presets_dir):
            if not filename.endswith(".spexp"):
                continue
            name = os.path.splitext(filename)[0]
            export_preset_id = substance_painter.resource.ResourceID(context=shelf.name(), name=name)
            export_preset = substance_painter.resource.Resource.retrieve(export_preset_id)[0]
            #print(export_preset.gui_name())
    # my_shelf = substance_painter.resource.Shelf("export") 
    # all_shelf_resources = my_shelf.resources() 
    # print(substance_painter)
    # for resource in all_shelf_resources: 
    #     print(resource.identifier().name) 
    #print("The name of the project is now: '{0}'".format(substance_painter.project.name())) 
    metadata = substance_painter.project.Metadata("PluginSaveData")
    save = ["testsavedata", 2]
    metadata.set("plugin_save_data", save)
    
    print("Save Data", metadata.get("plugin_save_data"))
    

def saveData(path):
    global size_dropdown
    metadata = substance_painter.project.Metadata("PluginSaveData")
    PluginSaveData = [path, size_dropdown.currentIndex()]
    metadata.set("plugin_save_data", PluginSaveData)
    print("Save Data", metadata.get("plugin_save_data"))

def my_callback(*args, **kwargs):
    global output_path, output_path_input, texture_sizes_index
    print(f'Callback: {substance_painter.project.file_path()}')

    metadata = substance_painter.project.Metadata("PluginSaveData")
    PluginSaveData = metadata.get("plugin_save_data")
    output_path = PluginSaveData[0]
    texture_sizes_index = PluginSaveData[1]
    print(PluginSaveData)
    output_path_input.setText(output_path)
    size_dropdown.setCurrentIndex(texture_sizes_index)
    
def saveTriggered(*args, **kwargs):
    print("S A V E")


def start_plugin():
    dev_label = QtWidgets.QLabel("Enfusion")
    dev_label2 = QtWidgets.QLabel("DayZ")
    plugin_widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    plugin_widget.setLayout(layout)
    plugin_widget.setWindowTitle("Export") 
    
    substance_painter.event.DISPATCHER.connect(substance_painter.event.ProjectOpened, my_callback)
    #substance_painter.event.DISPATCHER.connect(substance_painter.event.ProjectSaved, saveTriggered)
    # Create a dropdown for selecting the texture size
    global size_dropdown
    size_label = QtWidgets.QLabel("Texture Size:")
    size_dropdown = QtWidgets.QComboBox()
    size_dropdown.addItems(texture_sizes)
    
    #size_dropdown.activated.conext(saveData(size_dropdown.currentIndex()))
    
    global output_path_input
    output_path_input = QtWidgets.QLineEdit()
    output_path_input.setPlaceholderText("Output Path")
    output_path_input.setText(output_path)
    output_path_input.textChanged.connect(lambda text = output_path_input.text(): saveData(text))
    

    row_layout1 = QtWidgets.QHBoxLayout()
    row_layout2 = QtWidgets.QHBoxLayout()
    row_layout3 = QtWidgets.QHBoxLayout()
    row_layout4 = QtWidgets.QHBoxLayout()
    row_layout5 = QtWidgets.QHBoxLayout()
    row_layout6 = QtWidgets.QHBoxLayout()
    row_layout7 = QtWidgets.QHBoxLayout()

    bt_export_mask = QtWidgets.QPushButton("Global Mask")
    bt_export_vfx = QtWidgets.QPushButton("VFX")
    bt_export_mcr = QtWidgets.QPushButton("MCR")
    bt_export_bcr = QtWidgets.QPushButton("BCR")
    bt_export_nmo = QtWidgets.QPushButton("NMO")

    bt_export_co = QtWidgets.QPushButton("CO")
    bt_export_nohq = QtWidgets.QPushButton("NOHQ")
    bt_export_smdi = QtWidgets.QPushButton("SMDI")
    bt_export_mc = QtWidgets.QPushButton("MC")
    bt_export_MASK = QtWidgets.QPushButton("MASK")
    bt_export_ADS = QtWidgets.QPushButton("ADS")
    bt_export_AS = QtWidgets.QPushButton("AS")
    bt_logX = QtWidgets.QPushButton("LogX")

    bt_export_mask.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_GLOBAL_MASK", size_dropdown.currentText()))
    bt_export_vfx.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_VFX", size_dropdown.currentText()))
    bt_export_mcr.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_MCR", size_dropdown.currentText()))
    bt_export_bcr.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_BCR", size_dropdown.currentText()))
    bt_export_nmo.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_NMO", size_dropdown.currentText()))

    bt_export_co.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_CO", size_dropdown.currentText()))
    bt_export_nohq.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_NOHQ", size_dropdown.currentText()))
    bt_export_smdi.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_SMDI", size_dropdown.currentText()))
    bt_export_mc.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_MC", size_dropdown.currentText()))
    bt_export_MASK.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_MASK", size_dropdown.currentText()))
    bt_export_ADS.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_ADS", size_dropdown.currentText()))
    bt_export_AS.clicked.connect(lambda: export_enfution(output_path_input.text(), "$textureSet_AS", size_dropdown.currentText()))

    bt_logX.hide()
    layout.addWidget(output_path_input)
    row_layout7.addWidget(size_label)
    row_layout7.addWidget(size_dropdown)
    
    row_layout1.addWidget(dev_label)
    row_layout1.addWidget(bt_export_bcr)
    row_layout1.addWidget(bt_export_nmo)
    row_layout2.addWidget(bt_export_mask)
    row_layout2.addWidget(bt_export_vfx)
    row_layout2.addWidget(bt_export_mcr)
    row_layout3.addWidget(dev_label2)
    row_layout3.addWidget(bt_export_co)
    row_layout3.addWidget(bt_export_nohq)
    row_layout4.addWidget(bt_export_smdi)
    row_layout4.addWidget(bt_export_mc)
    row_layout4.addWidget(bt_export_MASK)
    row_layout5.addWidget(bt_export_ADS)
    row_layout5.addWidget(bt_export_AS)
    
    layout.addWidget(bt_logX)
    layout.addLayout(row_layout7)
    layout.addLayout(row_layout1)
    layout.addLayout(row_layout2)
    layout.addLayout(row_layout3)
    layout.addLayout(row_layout4)
    layout.addLayout(row_layout5)
    layout.addLayout(row_layout6)
    
    substance_painter.ui.add_dock_widget(plugin_widget)
    plugin_widgets.append(plugin_widget)
def close_plugin():
    # Remove all widgets that have been added to the UI
    for widget in plugin_widgets:
        substance_painter.ui.delete_ui_element(widget)
    plugin_widgets.clear()

if __name__ == "__main__":
    start_plugin()