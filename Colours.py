
import os
import sys
import fileinput

filename = os.path.dirname(os.path.abspath(__file__)) + "/" + "link.user.cfg"

with fileinput.FileInput(filename, inplace=True, backup='.bak_colours') as file:
    for line in file:
    # EDITOR #
        #bookmark
        if line.strip().startswith("<FCUInt Name=\"Bookmark\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"16776960\"/>" + "\n"
        
        #breakpoint
        if line.strip().startswith("<FCUInt Name=\"Breakpoint\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"4278190080\"/>" + "\n"
        
        #Comment
        if line.strip().startswith("<FCUInt Name=\"Comment\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"1936945920\"/>" + "\n"
        
        #Block comment
        if line.strip().startswith("<FCUInt Name=\"Block comment\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"1936945920\"/>" + "\n"
        
        #Number
        if line.strip().startswith("<FCUInt Name=\"Number\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"4294967040\"/>" + "\n"
        
        #String
        if line.strip().startswith("<FCUInt Name=\"String\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"1000781312\"/>" + "\n"

        #Character
        if line.strip().startswith("<FCUInt Name=\"Character\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"4278190080\"/>" + "\n"
        
        #Class name
        if line.strip().startswith("<FCUInt Name=\"Class name\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"1321840640\"/>" + "\n"
        
        #Define name
        if line.strip().startswith("<FCUInt Name=\"Define name\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"3703857920\"/>" + "\n"
        
        #Operator
        if line.strip().startswith("<FCUInt Name=\"Block comment\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"4294967040\"/>" + "\n"
        
        #Python output
        if line.strip().startswith("<FCUInt Name=\"Python output\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"2863311360\"/>" + "\n"
        
        #Python error
        if line.strip().startswith("<FCUInt Name=\"Python error\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"4252787200\"/>" + "\n"                
        
        #Current line highlight
        if line.strip().startswith("<FCUInt Name=\"Current line highlight\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"707406336\"/>" + "\n"     

    # MAIN WINDOW #
        #Current line highlight
        if line.strip().startswith("<FCText Name=\"StyleSheet\""):
            num = line.find('Name')
            line = line[:num] + "Name=\"StyleSheet\">ProDark-Sidebar.qss</FCText>" + "\n"  

        #OverlayActiveStyleSheet
        if line.strip().startswith("<FCText Name=\"OverlayActiveStyleSheet\""):
            num = line.find('Name')
            line = line[:num] + "Name=\"OverlayActiveStyleSheet\">Dark-Outline.qss</FCText>" + "\n"

        #MenuStyleSheet
        if line.strip().startswith("<FCText Name=\"MenuStyleSheet\""):
            num = line.find('Name')
            line = line[:num] + "Name=\"MenuStyleSheet\">Default.qss</FCText>" + "\n"
        
        #Size of toolbar Icons
        if line.strip().startswith("<FCInt Name=\"ToolbarIconSize\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"24\"/>" + "\n"

        #Treeview icon size
        if line.strip().startswith("<FCInt Name=\"IconSize\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"20\"/>" + "\n"
        
        #Treeview item spacing
        if line.strip().startswith("<FCInt Name=\"ItemSpacing\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"4\"/>" + "\n"

    # VIEWPORT #
        #Simple ON (colour, instead of gradient background)
        if line.strip().startswith("<FCBool Name=\"Simple\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"1\"/>" + "\n"

        #Gradient to OFF
        if line.strip().startswith("<FCBool Name=\"Gradient\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"0\"/>" + "\n"
        
        #Gradient to OFF
        if line.strip().startswith("<FCUInt Name=\"BackgroundColor\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"926365695\"/>" + "\n"

    # SKETCHER #
        #Default Edge Colour
        if line.strip().startswith("<FCUInt Name=\"SketchEdgeColor\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"911964415\"/>" + "\n"  

        #Default Vertex Colour
        if line.strip().startswith("<FCText Name=\"SketchVertexColor\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"2521630207\"/>" + "\n"  

        #Making Line Colour
        if line.strip().startswith("<FCText Name=\"CreateLineColor\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"2189591295\"/>" + "\n"  
        
        #Edit Edge Colour
        if line.strip().startswith("<FCInt Name=\"EditedEdgeColor\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"4040472831\"/>" + "\n"  

        #Edit Vertex Colour
        if line.strip().startswith("<FCInt Name=\"EditedVertexColor\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"4034923007\"/>" + "\n"  
        
        #Invalid Sketch Colour
        if line.strip().startswith("<FCInt Name=\"InvalidSketchColor\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"4278190335\"/>" + "\n"  

        #Dimensional Constraint Colour
        if line.strip().startswith("<FCInt Name=\"ItemSpacing\""):
            num = line.find('Value')
            line = line[:num] + "Value=\"255\"/>" + "\n"  

        sys.stdout.write(line)