import fileinput
import os
import sys
import time
import winreg, win32security, win32api
import platform
import shutil
from lxml import etree as et

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox

parser = et.XMLParser(remove_blank_text=True)

if platform.system() == "Windows":
    winpath = os.getenv('APPDATA') + "\\FreeCAD\\"
    #filename = os.path.dirname(os.path.abspath(__file__)) + "\\" + "test.txt"
    usercfg = winpath + "link.user.cfg"
    output = winpath + "link.user.cfg"
if platform.system() == "Linux":
    linpath = os.getenv('HOME') + "\\.FreeCAD\\"
    usercfg = linpath + "link.user.cfg"
    output = linpath + "link.user.cfg"
if platform.system() == "Darwin":
    macpath = os.path.expanduser('~/Library/Preferences')
    usercfg = macpath + "link.user.cfg"
    output = macpath + "link.user.cfg"

app_dir = os.path.dirname(os.path.abspath(__file__))
xml_dir = app_dir + "\\xml\\"

PersistentToolbar = xml_dir + "PersistentToolbar.xml"
DockWindows = xml_dir + "DockWindows.xml"
Editor = xml_dir + "Editor.xml"
TreeViewPrefs = xml_dir + "TreeViewPrefs.xml"

# Parse link.user.cfg as xml
usercfg_tree = et.parse(usercfg, parser)
usercfg_root = usercfg_tree.getroot()

# Parse PersistentToolbar.xml
PersistentToolbar_tree = et.parse(PersistentToolbar, parser)
PersistentToolbar_root = PersistentToolbar_tree.getroot()

# Parse DockWindows.xml
DockWindows_tree = et.parse(DockWindows, parser)
DockWindows_root = DockWindows_tree.getroot()

# Parse Editor.xml
Editor_tree = et.parse(Editor, parser)
Editor_root = Editor_tree.getroot()

# Parse TreeViewPrefs.xml
TreeViewPrefs_tree = et.parse(TreeViewPrefs, parser)
TreeViewPrefs_root = TreeViewPrefs_tree.getroot()


class MyLayout(Widget):

    ui = False
    console = False
    sketcher = False
    count = 0
    regcount = 0
    error = False
    completed = False

    def check_include_ui(self, state):
        if state:
            self.ui = not False
            self.reset_button()
            self.error = False
            self.completed = False
        else:
            self.ui = False

    def check_include_console(self, state):
        if state:
            self.console = not False
            self.reset_button()
            self.error = False
            self.completed = False
        else:
            self.console = False
    
    def check_include_sketcher(self, state):
        if state:
            self.sketcher = not False
            self.reset_button()  
            self.error = False
            self.completed = False
        else:
            self.sketcher = False

    def reset_checkbox(self):
        for child in reversed(self.ids.check1.children):
            if isinstance(child, CheckBox):
                child.active = False 
        for child in reversed(self.ids.check2.children):
            if isinstance(child, CheckBox):
                child.active = False 
        for child in reversed(self.ids.check3.children):
            if isinstance(child, CheckBox):
                child.active = False 

    def pressed(self, state):
        print(self.ui, self.console, self.sketcher)
        self.count = self.count+1
        self.regcount = self.regcount+1
        print(self.count)

        if self.ui == False and self.console == False and self.sketcher == False:
            self.ids.main.text = "Empty Selection"
            self.ids.main.background_color = (1,0,0,1)
            self.error = True
        
        if not self.error:
            if os.path.isfile(winpath + f'link.user.cfg_backup{self.count}'):
                self.count +=1
                shutil.copy(usercfg, winpath + f'link.user.cfg_backup{self.count}')
            else:
                shutil.copy(usercfg, winpath + f'link.user.cfg_backup{self.count}')
        
        if self.completed == True:
            App.get_running_app().stop()

        if self.ui == True:
            
            if platform.system() == "Windows":
            # Backup HKEY_CURRENT_USER\SOFTWARE\FreeCAD\FreeCAD\Qt5.12\ Just in case
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\FreeCAD\\FreeCAD\\Qt5.12") as handle:
                        # Ask for Elevated Permissions 
                        win32security.AdjustTokenPrivileges(win32security.OpenProcessToken(win32api.GetCurrentProcess(), 40), 0, [(win32security.LookupPrivilegeValue(None, 'SeBackupPrivilege'), 2)])
                        # Backup binary registry file to AppData\FreeCAD\ folder. To restore backup, run regedit and File -> Import, select "Registry Hive Files" in the dropdown and select the 'regbackup' file
                        if os.path.isfile(winpath + f"regbackup{self.regcount}"):
                            self.regcount +=1
                            winreg.SaveKey(handle, winpath + f"regbackup_512{self.regcount}")
                        else:
                            winreg.SaveKey(handle, winpath + f"regbackup_512{self.regcount}")    
                    # Deleting redundant registry keys (made redundant by Persistent Toolbars, which writes the layout in the .cfg file)
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\FreeCAD\\FreeCAD\\Qt5.12")
                except:
                    pass
                try: 
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\FreeCAD\\FreeCAD\\Qt5.15") as handle2:
                        # Ask for Elevated Permissions 
                        win32security.AdjustTokenPrivileges(win32security.OpenProcessToken(win32api.GetCurrentProcess(), 40), 0, [(win32security.LookupPrivilegeValue(None, 'SeBackupPrivilege'), 2)])
                        # Backup binary registry file to AppData\FreeCAD\ folder. To restore backup, run regedit and File -> Import, select "Registry Hive Files" in the dropdown and select the 'regbackup' file
                        if os.path.isfile(winpath + f"regbackup{self.regcount}"):
                            self.regcount +=1
                            winreg.SaveKey(handle2, winpath + f"regbackup_515{self.regcount}")
                        else:
                            winreg.SaveKey(handle2, winpath + f"regbackup_515{self.regcount}")    
                    # Deleting redundant registry keys (made redundant by Persistent Toolbars, which writes the layout in the .cfg file)
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\FreeCAD\\FreeCAD\\Qt5.15")
                except:
                    pass

            # Delete everything in PersistentToolbar in link.user.cfg
            for users in usercfg_root.findall('.//*[@Name=\"PersistentToolbars\"]/*[@Name=\"User\"]'):
                for x in users.findall('./*'):
                    users.remove(x)
            
            # Copy over the setup from PersistentToolbar.xml
            PersistentToolbar_tag = PersistentToolbar_tree.findall('./')
            for x in PersistentToolbar_tag:
                usercfg_tree.find('.//*[@Name=\"PersistentToolbars\"]/*[@Name=\"User\"]').append(x)

            # Set Theme To ProDark-Sidebar
            elm = usercfg_root.find('.//*[@Name=\"Preferences\"]*[@Name=\"MainWindow\"]')
            # Check whether ToolbarStyle element has children. If true, change it to IconText, if false, add a child
            elmcount = usercfg_root.findall('.//*[@Name=\"Preferences\"]*[@Name=\"MainWindow\"]*[@Name=\"StyleSheet\"]')
            if not elmcount:
                elm.append(et.fromstring("<FCText Name=\"StyleSheet\">ProDark-Sidebar.qss</FCText>"))
            else:
                usercfg_root.find('.//*[@Name=\"Preferences\"]*[@Name=\"MainWindow\"]*[@Name=\"StyleSheet\"]').text = "ProDark-Sidebar.qss"

            # Set ToolbarStyle to IconText
            elm = usercfg_root.find('.//*[@Name=\"ToolbarStyle\"]')
            # Check whether ToolbarStyle element has children. If true, change it to IconText, if false, add a child
            elmcount = usercfg_root.findall('.//*[@Name=\"ToolbarStyle\"]/')
            if not elmcount:
                elm.append(et.fromstring("<FCText Name=\"Style\">IconText</FCText>"))
            else:
                usercfg_root.find('.//*[@Name=\"ToolbarStyle\"]/').text = "IconText"
            
            # Docking
            elm = usercfg_root.find('.//*[@Name=\"Preferences\"]*[@Name=\"DockWindows\"]*[@Name=\"ComboView\"]')
            # Check whether Toolbars element has children. If empty, add a line, else, just change the value. Repeat.
            elmcount = usercfg_root.findall('.//*[@Name=\"Preferences\"]*[@Name=\"DockWindows\"]*[@Name=\"ComboView\"]/')
            if not elmcount:
                elm.append(et.fromstring("<FCBool Name=\"Enabled\" Value=\"0\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"Preferences\"]*[@Name=\"DockWindows\"]*[@Name=\"ComboView\"]*[@Name=\"Enabled\"]').attrib['Value'] = "0"

            usercfg_root.find('.//*[@Name=\"DockWindows\"]*[@Name=\"TreeView\"]*[@Name=\"Enabled\"]').attrib['Value'] = "1"
            usercfg_root.find('.//*[@Name=\"DockWindows\"]*[@Name=\"PropertyView\"]*[@Name=\"Enabled\"]').attrib['Value'] = "1"

            # Set Toolbars
            elm = usercfg_root.find('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]')
            # Check whether Toolbars element has children. If empty, add a line, else, just change the value. Repeat.
            elmcount = usercfg_root.findall('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"File\"]')
            if not elmcount:
                elm.append(et.fromstring("<FCBool Name=\"File\" Value=\"0\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"File\"]').attrib['Value'] = "0"

            elmcount = usercfg_root.findall('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"Workbench\"]')
            if not elmcount:
                elm.append(et.fromstring("<FCBool Name=\"Workbench\" Value=\"1\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"Workbench\"]').attrib['Value'] = "1"

            elmcount = usercfg_root.findall('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"Macro\"]')
            if not elmcount:
                elm.append(et.fromstring("<FCBool Name=\"Macro\" Value=\"0\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"Macro\"]').attrib['Value'] = "0"

            elmcount = usercfg_root.findall('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"View\"]')
            if not elmcount:
                elm.append(et.fromstring("<FCBool Name=\"View\" Value=\"0\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"View\"]').attrib['Value'] = "0"

            elmcount = usercfg_root.findall('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"Structure\"]')
            if not elmcount:
                elm.append(et.fromstring("<FCBool Name=\"Structure\" Value=\"0\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"Structure\"]').attrib['Value'] = "0"

            elmcount = usercfg_root.findall('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"Navigation\"]')
            if not elmcount:
                elm.append(et.fromstring("<FCBool Name=\"Navigation\" Value=\"0\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"MainWindow\"]*[@Name=\"Toolbars\"]*[@Name=\"Navigation\"]').attrib['Value'] = "0"

            # LINKSTAGE3 UI #
            elm = usercfg_root.find('.//*[@Name=\"Preferences\"]*[@Name=\"MainWindow\"]')
            elmcount = usercfg_root.findall('.//*[@Name=\"Preferences\"]*[@Name=\"MainWindow\"]*[@Name=\"OverlayActiveStyleSheet\"]')
            if not elmcount:
                elm.append(et.fromstring("<FCText Name=\"OverlayActiveStyleSheet\">Dark-Outline.qss</FCText>"))
            else:
                usercfg_root.find('.//*[@Name=\"MainWindow\"]*[@Name=\"OverlayActiveStyleSheet\"]').text = "Dark-Outline.qss"

            # Delete everything in DockWindows in link.user.cfg
            for dock in usercfg_root.findall('.//*[@Name=\"BaseApp\"]*[@Name=\"MainWindow\"]*[@Name=\"DockWindows\"]'):
                for x in dock.findall('./*'):
                    dock.remove(x)
            
            # Copy over the setup from DockWindows.xml
            DockWindows_tag = DockWindows_tree.findall('./')
            for x in DockWindows_tag:
                usercfg_tree.find('.//*[@Name=\"BaseApp\"]*[@Name=\"MainWindow\"]*[@Name=\"DockWindows\"]').append(x)

            # TREEVIEW #
            # Delete everything in Preferences/TreeView in link.user.cfg
            for tvsets in usercfg_root.findall('.//*[@Name=\"Preferences\"]*[@Name=\"TreeView\"]'):
                for x in tvsets.findall('./*'):
                    tvsets.remove(x)

            # Copy over the setup from TreeViewPrefs.xml
            TreeViewPrefs_tag = TreeViewPrefs_tree.findall('./')
            for x in TreeViewPrefs_tag:
                usercfg_tree.find('.//*[@Name=\"Preferences\"]*[@Name=\"TreeView\"]').append(x)

            # VIEWPORT #
            # Simple ON (solid colour instead of gradient in the background)
            elm = usercfg_root.find('.//*[@Name=\"Preferences\"]*[@Name=\"View\"]')
            
            simplebg = usercfg_root.findall('.//*[@Name=\"View\"]*[@Name=\"Simple\"]')
            if not simplebg:
                elm.append(et.fromstring("<FCBool Name=\"Simple\" Value=\"1\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"View\"]*[@Name=\"Simple\"]').attrib['Value'] = "1"

            # Gradient To OFF
            gradient = usercfg_root.findall('.//*[@Name=\"View\"]*[@Name=\"Gradient\"]')
            if not gradient:
                elm.append(et.fromstring("<FCBool Name=\"Gradient\" Value=\"0\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"View\"]*[@Name=\"Gradient\"]').attrib['Value'] = "0"

            # Background Colour
            bgcol = usercfg_root.findall('.//*[@Name=\"View\"]*[@Name=\"BackgroundColor\"]')
            if not bgcol:
                elm.append(et.fromstring("<FCUInt Name=\"BackgroundColor\" Value=\"926365695\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"View\"]*[@Name=\"BackgroundColor\"]').attrib['Value'] = "926365695"

            # SELECTION #            
            highlight_col = usercfg_root.findall('.//*[@Name=\"Preferences\"]*[@Name=\"View\"]*[@Name=\"HighlightColor\"]')
            if not highlight_col:
                elm.append(et.fromstring("<FCUInt Name=\"HighlightColor\" Value=\"12306687\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"Preferences\"]*[@Name=\"View\"]*[@Name=\"HighlightColor\"]').attrib['Value'] = "12306687"

            highlight_col = usercfg_root.findall('.//*[@Name=\"Preferences\"]*[@Name=\"View\"]*[@Name=\"SelectionColor\"]')
            if not highlight_col:
                elm.append(et.fromstring("<FCUInt Name=\"SelectionColor\" Value=\"3197895423\"/>"))
            else:
                usercfg_root.find('.//*[@Name=\"Preferences\"]*[@Name=\"View\"]*[@Name=\"SelectionColor\"]').attrib['Value'] = "3197895423"

            # WRITE link.user.cfg #
            et.ElementTree(usercfg_root).write(output, pretty_print=True, encoding='utf-8', xml_declaration=True)

        if self.console == True:
            # SETTING EDITOR COLOURS #
            # Delete everything in Editor in link.user.cfg
            for edcols in usercfg_root.findall('.//*[@Name=\"Preferences\"]*[@Name=\"Editor\"]'):
                for editor in edcols.findall('./*'):
                    edcols.remove(editor)

            # Copy over the setup from Editor.xml
            Editor_tag = Editor_tree.findall('./')
            for x in Editor_tag:
                destination = usercfg_tree.find('.//*[@Name=\"Preferences\"]*[@Name=\"Editor\"]')
                destination.append(x)

            # WRITE link.user.cfg
            et.ElementTree(usercfg_root).write(output, pretty_print=True, encoding='utf-8', xml_declaration=True)

        if self.sketcher == True:
            # SKETCHER #
            sktchr = usercfg_root.find('.//*[@Name=\"Preferences\"]*[@Name=\"View\"]')
            # SketchEdgeColour
            sketchedge = usercfg_root.findall('.//*[@Name=\"View\"]*[@Name=\"SketchEdgeColor\"]')
            if not sketchedge:
                sktchr.append(et.fromstring("<FCUInt Name=\"SketchEdgeColor\" Value=\"911964415\"/>"))
            else:
                value = usercfg_root.find('.//*[@Name=\"View\"]*[@Name=\"SketchEdgeColor\"]')
                value.attrib['Value'] = "911964415"
    
            # Vertex Colour
            vertexcol = usercfg_root.findall('.//*[@Name=\"View\"]*[@Name=\"SketchVertexColor\"]')
            if not vertexcol:
                sktchr.append(et.fromstring("<FCUInt Name=\"SketchVertexColor\" Value=\"2521630207\"/>"))
            else:
                value = usercfg_root.find('.//*[@Name=\"View\"]*[@Name=\"SketchVertexColor\"]')
                value.attrib['Value'] = "2521630207"
    
            # Making Line Colour
            linecol = usercfg_root.findall('.//*[@Name=\"View\"]*[@Name=\"CreateLineColor\"]')
            if not linecol:
                sktchr.append(et.fromstring("<FCUInt Name=\"CreateLineColor\" Value=\"2189591295\"/>"))
            else:
                value = usercfg_root.find('.//*[@Name=\"View\"]*[@Name=\"CreateLineColor\"]')
                value.attrib['Value'] = "2189591295"
    
            # Edit Edge Colour
            edsketchedge = usercfg_root.findall('.//*[@Name=\"View\"]*[@Name=\"EditedEdgeColor\"]')
            if not edsketchedge:
                sktchr.append(et.fromstring("<FCUInt Name=\"EditedEdgeColor\" Value=\"4040472831\"/>"))
            else:
                value = usercfg_root.find('.//*[@Name=\"View\"]*[@Name=\"EditedEdgeColor\"]')
                value.attrib['Value'] = "4040472831"
    
            # Edit Vertex Colour
            edvertexcol = usercfg_root.findall('.//*[@Name=\"View\"]*[@Name=\"EditedVertexColor\"]')
            if not edvertexcol:
                sktchr.append(et.fromstring("<FCUInt Name=\"EditedVertexColor\" Value=\"4034923007\"/>"))
            else:
                value = usercfg_root.find('.//*[@Name=\"View\"]*[@Name=\"EditedVertexColor\"]')
                value.attrib['Value'] = "4034923007"
    
            # Invalid Sketch Colour
            sketcherror = usercfg_root.findall('.//*[@Name=\"View\"]*[@Name=\"InvalidSketchColor\"]')
            if not sketcherror:
                sktchr.append(et.fromstring("<FCUInt Name=\"InvalidSketchColor\" Value=\"4278190335\"/>"))
            else:
                value = usercfg_root.find('.//*[@Name=\"View\"]*[@Name=\"InvalidSketchColor\"]')
                value.attrib['Value'] = "4278190335"
    
            # Dimension Colour
            dim = usercfg_root.findall('.//*[@Name=\"View\"]*[@Name=\"ConstrainedDimColor\"]')
            if not dim:
                sktchr.append(et.fromstring("<FCUInt Name=\"ConstrainedDimColor\" Value=\"255\"/>"))
            else:
                value = usercfg_root.find('.//*[@Name=\"View\"]*[@Name=\"ConstrainedDimColor\"]')
                value.attrib['Value'] = "255"

            # WRITE link.user.cfg
            et.ElementTree(usercfg_root).write(output, pretty_print=True, encoding='utf-8', xml_declaration=True)
        
        # Reset all checkboxes to prevent accidental double-clicks.
        self.reset_checkbox()

    # Once above progress is complete, turn button green and use it to close the application.
    def check(self):
        if self.error == False:
            self.completed = True
            self.ids.main.text = "Done. Click To Exit"
            self.ids.main.background_color = (0,1,0,1)

    def reset_button(self):
        self.ids.main.text = "Apply"
        self.ids.main.background_color = (1,1,1,1)

class FreeCAD4K(App):
    def build(self):
        self.icon = app_dir + "\\Images\\icon.png"
        Window.size = (400, 1235)
        self.title = 'FreeCAD Linkstage3 4K UI'
        return MyLayout()

if __name__ == '__main__':
    FreeCAD4K().run()