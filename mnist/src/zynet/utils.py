import json
import math
# TODO remove bitstring dependency
import bitstring

'''
    DtoB converts your floating point number into fixed point representation with fracBits bits dedicated
    to the decimal part and (dataWidth - fracBits) dedicated to the integer part
'''
def floatToFix(floatNumber, fracBits, totalBits):             
    fixPoint = int(round(abs(floatNumber) * (2**fracBits)))
    fixPointBinary = bitstring.BitArray(int=fixPoint, length=totalBits)
    bin_list = list(fixPointBinary.bin)
   
    if(floatNumber < 0):
        bin_list[0] = "1"

    return ''.join(bin_list)

def fixedToFloat(bin_str, fracBits, totalBits) -> float:
    
    bit_list = list(bin_str)
    sign = 1
    if(bit_list[0] == "1"):
        sign = -1
        bit_list[0] = "0"

    bin_str = ''.join(bit_list)

    intRepresentation = int(bin_str, 2)

    return sign * (intRepresentation * 1.0)/(2 ** fracBits)

def genWeightArray(filename=""):
    with open(filename, "r") as f:
        output = []
        myWeights = json.load(f)['weights']
        # TODO remove this flatten
        flatten(myWeights,output)
        #maxVal = max(output)
        #minVal = min(output)
        #minBits = max(math.ceil(math.log2(abs(int(maxVal))+1)),math.ceil(math.log2(abs(int(minVal))+1)))+1 #One additional bit for sign
        #print("Minimum bits required for integer representation of Weight Values",minBits)
        return myWeights
    
    
def genBiasArray(filename=""):
    with open(filename, "r") as f:
        return json.loads(f.read())['biases']
    
    
def flatten(l,output): #Recursive function to flatten a multi-dimensional list
    for i in l: 
        if type(i) == list: 
            flatten(i,output) 
        else: 
            output.append(i) 