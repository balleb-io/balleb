import sys

outputPath = "./src/fpga/testData/"
headerFilePath = "./src/fpga/testData/"

try:
    import cPickle as pickle
except:
    import pickle
import gzip
import numpy as np
import os
from zynet.utils import floatToFix, fixedToFloat

try:
    testDataNum = int(sys.argv[1])
except:
    testDataNum = 3

if(not os.path.isdir(outputPath)):
    os.makedirs(outputPath)
    print(f"Created directory {outputPath}")
if(not os.path.isdir(headerFilePath)):
    os.makedirs(headerFilePath)
    print(f"Created directory {headerFilePath}")

def load_data():
    f = gzip.open('mnist.pkl.gz', 'rb')         #change this location to the resiprositry where MNIST dataset sits
    try:
        training_data, validation_data, test_data = pickle.load(f,encoding='latin1')
    except:
        training_data, validation_data, test_data = pickle.load(f)
    f.close()
    return (training_data, validation_data, test_data)

def DtoB(num,dataWidth,fracBits):                        #funtion for converting into two's complement format
    if num >= 0:
        num = num * (2**fracBits)
        d = int(num)
    else:
        num = -num
        num = num * (2**fracBits)        #number of fractional bits
        num = int(num)
        if num == 0:
            d = 0
        else:
            d = 2**dataWidth - num
    return d


def genTestData(dataWidth,IntSize,testDataNum):
    dataHeaderFile = open(headerFilePath+"dataValues.h","w")
    dataHeaderFile.write("int dataValues[]={")
    tr_d, va_d, te_d = load_data()
    test_inputs = [np.reshape(x, (1, 784))*-1 for x in te_d[0]]
    x = len(test_inputs[0][0])
    d=dataWidth-IntSize
    count = 0
    fileName = 'test_data.txt'
    f = open(outputPath+fileName,'w')
    fileName = 'visual_data'+str(te_d[1][testDataNum])+'.txt'
    g = open(outputPath+fileName,'w')
    k = open('testData.txt','w')
    for i in range(0,x):
        k.write(str(test_inputs[testDataNum][0][i])+',')
        dInDec = DtoB(test_inputs[testDataNum][0][i],dataWidth,d)
        myData = bin(dInDec)[2:]
        dataHeaderFile.write(str(dInDec)+',')
        f.write(myData+'\n')
        if test_inputs[testDataNum][0][i]>0:
            g.write(str(1)+' ')
        else:
            g.write(str(0)+' ')
        count += 1
        if count%28 == 0:
            g.write('\n')
    k.close()
    g.close()
    f.close()
    dataHeaderFile.write('0};\n')
    dataHeaderFile.write('int result='+str(te_d[1][testDataNum])+';\n')
    dataHeaderFile.close()

        

        
def genAllTestData(dataWidth: int, IntSize: int, cases: int = 0, debug: bool = False) -> None:
    if IntSize <= 0: 
        print(f"Invalid integer portion ({IntSize}) of fixed point representation specified")
        return

    _, _, te_d = load_data()
    
    test_inputs = te_d[0] 
    input_size = len(test_inputs[0])

    # What is dataWidth and IntSize?
    #Answer: This is the radix point AKA:
    #place to put the comma
    
    radixPoint = dataWidth-IntSize

    cases = len(test_inputs) if cases == 0 else cases
    
    for i in range(cases):
        ext = str(i).zfill(4)
        ###
        fileName = 'test_data_'+ext+'.txt'
        f = open(outputPath+fileName,'w')
        f_float = open("./model/testData/"+"float_"+fileName, 'w')
        # iterates over each pixel
        for j in range(0,input_size):
            fixedPointBinary = floatToFix(test_inputs[i][j],radixPoint, dataWidth)
            pixel =test_inputs[i][j]
            f_float.write(str(pixel) + '\n')
            to_fixed_and_back = fixedToFloat(fixedPointBinary, radixPoint, dataWidth)
            
            if debug and test_inputs[i][j] != 0: print(str(pixel).ljust(10), "->", fixedPointBinary, "->", str(to_fixed_and_back).ljust(10), "-> delta = %", str((abs(pixel - to_fixed_and_back)/pixel) * 100).ljust(12), "->", (str(len(fixedPointBinary)) +  " bits"))
            f.write(fixedPointBinary+'\n')
        
        if debug: print("Answer:", te_d[1][i])
        if te_d[1][i] >= 2**(IntSize - 1): 
            print(f"Error: integer representation part too small to fit dependent variable -> {te_d[1][i]} too large for {IntSize} bits")
            return
        f.write(floatToFix((te_d[1][i]), radixPoint, dataWidth))
        f_float.write(str(te_d[1][i]))
        f.close()
        f_float.close()



# this is all inconsistent
# how is the sign bit used
        

#if __name__ == "__main__":
#    #genTestData(dataWidth,IntSize,testDataNum=1)
#    dataWidth = 32                    #specify the number of bits in test data
#    IntSize = 9 #Number of bits of integer portion including sign bit
#    genAllTestData(dataWidth,IntSize, 10, debug=True)
#    genTestData(32, 5, 10)
