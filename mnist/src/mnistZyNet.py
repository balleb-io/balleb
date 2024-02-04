import sys
import numpy as np
from zynet import net
from zynet import utils
from zynet import xilinxUtils


def genMnistZynet(dataWidth,sigmoidSize):
    model = net.model()
    model.add(net.layer("flatten",784))
    model.add(net.layer("Dense",30,"ReLU"))
    model.add(net.layer("Dense",30,"ReLU"))
    model.add(net.layer("Dense",10,"ReLU"))
    model.add(net.layer("Dense",10,"ReLU"))
    model.add(net.layer("Dense",10,"hardmax"))
    weightArray = utils.genWeightArray('WeigntsAndBiasesReLU.txt')
    biasArray = utils.genBiasArray('WeigntsAndBiasesReLU.txt')
    model.compile(pretrained='Yes',weights=weightArray,biases=biasArray,dataWidth=dataWidth,sigmoidSize=sigmoidSize,weightIntSize=4,inputIntSize=1)
    xilinxUtils.makeVivadoProject('myProject1')
    xilinxUtils.makeIP('myProject1')
    # TODO automate IP packaging
    input("Please package the IP in the Vivado GUI. Press enter when done.")
    xilinxUtils.makeSystem('myProject1','myBlock1')

if __name__ == "__main__":
    genMnistZynet(dataWidth=31,sigmoidSize=5)