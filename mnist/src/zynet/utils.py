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
    if floatNumber < 0:
        fixPoint = ~fixPoint
        fixPoint += 1

    fixPointBinary = bitstring.BitArray(int=fixPoint, length=totalBits)
    bin_list = list(fixPointBinary.bin)
   
    return ''.join(bin_list)

def fixedToFloat(bin_str, fracBits, totalBits) -> float:
    # There's probably a faster way of doing this
    # Honestly I just don't want to mess with Python's 
    # Sign extension logic here, I just want to make
    # Inference work, so,
    # TODO do this with bitwise manipulation <3
    if bin_str[0] == '1':
        inverted_bin_str = ''
        for x in bin_str:
            if x == '0': inverted_bin_str+= '1'
            if x == '1': inverted_bin_str+= '0'

        x = int(inverted_bin_str, 2) + 1

        sign = 1 if bin_str[0] == '0' else -1

        return sign * x / 2**fracBits
    else:
        return int(bin_str, 2) / 2**fracBits

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