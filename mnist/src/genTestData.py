import pdb
import sys

outputPath = "./testData/"
headerFilePath = "./testData/"

try:
    import cPickle as pickle
except:
    import pickle
import gzip
import numpy as np


try:
    testDataNum = int(sys.argv[1])
except:
    testDataNum = 3

# probably rewrite this
'''
    DtoB converts your floating point number into fixed point representation with fracBits bits dedicated
    to the decimal part and (dataWidth - fracBits) dedicated to the integer part
'''
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

def load_data():
    f = gzip.open('mnist.pkl.gz', 'rb')         #change this location to the resiprositry where MNIST dataset sits
    try:
        training_data, validation_data, test_data = pickle.load(f,encoding='latin1')
    except:
        training_data, validation_data, test_data = pickle.load(f)
    f.close()
    return (training_data, validation_data, test_data)

def genTestData(dataWidth,IntSize,testDataNum):
    dataHeaderFile = open(headerFilePath+"dataValues.h","w")
    dataHeaderFile.write("int dataValues[]={")
    tr_d, va_d, te_d = load_data()
    test_inputs = [np.reshape(x, (1, 784)) for x in te_d[0]]
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
        

def fixedToFloat(bin_str: str) -> float:
    power = 0.5
    res = 0
    for i in bin_str:
        if i == '1': res += power
        power /=2 
    return res
        
def genAllTestData(dataWidth,IntSize):
    tr_d, va_d, te_d = load_data()
    # what is this reshape doing?
    test_inputs = [np.reshape(x, (1, 784)) for x in te_d[0]]
    x = len(test_inputs[0][0])
    # What is dataWidth and IntSize?
    d=dataWidth-IntSize
    for i in range(1):
        ext = str(i).zfill(4)
        ###
        fileName = 'test_data_'+ext+'.txt'
        f = open(outputPath+fileName,'w')
        # iterates over each pixel
        for j in range(0,x):
            dInDec = DtoB(test_inputs[i][0][j],dataWidth,d)
            myData = bin(dInDec)[2:].ljust(31, "0")
            pixel = test_inputs[i][0][j]
            to_fixed_and_back = fixedToFloat(myData)
            if (test_inputs[i][0][j] != 0): print(str(pixel).ljust(10), "->", myData, "->", str(to_fixed_and_back).ljust(10), "-> delta = %", str((abs(pixel - to_fixed_and_back)/pixel) * 100).ljust(12), "->", (str(len(myData)) +  " bits"))
            f.write(myData+'\n')
        print("Answer:", te_d[1][i])
        f.write(bin(DtoB((te_d[1][i]),dataWidth,0))[2:])
        f.close()



# this is all inconsistent
# how is the sign bit used
        

if __name__ == "__main__":
    #genTestData(dataWidth,IntSize,testDataNum=1)
    dataWidth = 32                    #specify the number of bits in test data
    IntSize = 1 #Number of bits of integer portion including sign bit
    genAllTestData(dataWidth,IntSize)
