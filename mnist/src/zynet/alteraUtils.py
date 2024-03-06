from os import system, path

def makeQuartusProject(projectName = 'MyProject', fpgaFamily='Cyclone10LP', fpgaDevice='10CL055YU484C8G'):
    #Runs tclScript and creates the project
    command = "quartus_sh -t " + path.join(path.dirname(__file__),'db/quartusScript.tcl ') + projectName + " " + fpgaFamily+ " " + fpgaDevice
    
    print('Executing the following command:', command)
    system(command)

    #analysis and synthesis
    system("quartus_map " + projectName) 

    #fitter
    system("quartus_fit " + projectName)

    #assembler
    system("quatus_asm " + projectName)

    #runs slow corner model aka worst scenario in conditions
    system("quartus_sta " + projectName + " --export_settings=off")

makeQuartusProject()