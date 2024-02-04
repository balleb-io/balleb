from os import system
from os import path

def makeVivadoProject(projectName='myProject',fpgaPart="xc7z020clg484-1"):
    command = "vivado -mode tcl -source "+path.join(path.dirname(__file__),'db/vivadoScript.tcl')+" -tclargs "+fpgaPart
    print("Executing the following command:", command)
    system(command)
    f=open("zynet.tcl","a")
    f.write("\nset_property source_mgmt_mode All [current_project]")
    f.write("\nexit") #Vivado doesn't add exit command to the end of the script
    f.close()
    command = "vivado -mode tcl -source zynet.tcl -tclargs --project_name "+projectName
    print("Executing the following command:", command)
    system(command)

def makeIP(projectName='myProject'):
    command = "vivado -mode tcl -source " + path.join(path.dirname(__file__),'db/makeIP.tcl') + " -tclargs "+ projectName + "/" + projectName + ".xpr"
    print("Executing the following command:", command)
    system(command)
    
def makeSystem(projectName='myProject',ipPath="",blockName=""):
    command = "vivado -mode tcl -source " + path.join(path.dirname(__file__),'db/block.tcl') + " -tclargs " + projectName + "/" + projectName + ".xpr" + " " + ipPath+" "+blockName
    print("Executing the following command:", command)
    system(command)