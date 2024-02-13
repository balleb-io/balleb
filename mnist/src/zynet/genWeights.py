outputPath = "./src/fpga/rtl/"
headerPath = "."

from zynet.utils import floatToFix, fixedToFloat

def DtoB(num,dataWidth,fracBits):   #funtion for converting into two's complement format
    if num >= 0:
        num = num * (2**fracBits)
        num = int(num)
        if num == 0:
            d = 0
        else:
            d = num
    else:
        num = -num
        num = num * (2**fracBits)    #number of fractional bits
        num = int(num)
        if num == 0:
            d = 0
        else:
            d = 2**dataWidth - num
    return d

def genWeights(dataWidth, weightFracWidth, biasFracWidth, weightArray, biasArray):
    weightIntWidth = dataWidth-weightFracWidth
    biasIntWidth = dataWidth-biasFracWidth
    myBiases = biasArray
    try:
        for layer in range(len(weightArray)):
            for neuron in range(len(weightArray[layer])):
                with open(outputPath + 'w_'+str(layer+1)+'_'+str(neuron)+'.mif','w') as f:
                    for weight in range(0,len(weightArray[layer][neuron])):
                        ftfx = floatToFix(weightArray[layer][neuron][weight], weightFracWidth, dataWidth)
                        f.write(ftfx)
                        f.write("\n")
    except:
        print("Number of weights do not match with number of neurons")
        
    try:
        for layer in range(0,len(myBiases)):
            for neuron in range(0,len(myBiases[layer])):
                with open(outputPath+'b_'+str(layer+1)+'_'+str(neuron)+'.mif','w') as f:
                    f.write(floatToFix(myBiases[layer][neuron][0], biasFracWidth, dataWidth))
                    f.write("\n")
    except:
        print("Number of biases do not match with number of neurons")