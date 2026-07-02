import json, sys, os

langSpec={"comp":{"0":"0101010","1":"0111111","-1":"0111010","D":"0001100","A":"0110000","M":"1110000","!D":"0001101","!A":"0110001","!M":"1110001","-D":"0001111","-A":"0110011","-M":"1110011","D+1":"0011111","A+1":"0110111","M+1":"1110111","D-1":"0001110","A-1":"0110010","M-1":"1110010","D+A":"0000010","D+M":"1000010","D-A":"0010011","D-M":"1010011","A-D":"0000111","M-D":"1000111","D&A":"0000000","D&M":"1000000","D|A":"0010101","D|M":"1010101"},"dest":{"null":"000","M":"001","D":"010","MD":"011","A":"100","AM":"101","AD":"110","AMD":"111"},"jump":{"null":"000","JGT":"001","JEQ":"010","JGE":"011","JLT":"100","JNE":"101","JLE":"110","JMP":"111"}}
symbolTable = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15, "SCREEN": 16384, "KBD": 24576}

addressCounter = 16

#Get the filename from the command line arguments
filename=sys.argv[1]

def main():

    #Read file
    with open(filename, 'r') as file:
        data = file.readlines()

    #First pass to build the symbol table
    lineCounter=0
    for line in data:
        line=line.strip()
        if "//" in line:
            line=line.split('//')[0].strip()
        if "(" in line:
            line=line[1:-1]
            symbolTable[line] = lineCounter
        elif line:
            lineCounter+=1

    #Second pass to assemble the code
    code=[]
    for line in data:
        line=line.strip()
        if "//" in line:
            line=line.split('//')[0].strip()
        if line and "(" not in line:
            code.append(assemble(line)+"\n")

    #Write the assembled code to a .hack file
    with open(os.path.splitext(filename)[0]+".hack",'w') as file:
        file.writelines(code)

    print("Completed")

def assemble(line):
    global addressCounter
    if line[0]=="@":    #A-instruction
        address=line.strip("@")
        
        if address.isdigit():
            decimal=address
        else:           #Variable or label
            if address not in symbolTable:
                symbolTable[address] = addressCounter
                addressCounter += 1
            decimal=symbolTable[address]

        return format(int(decimal),'016b')
    else:               #C-instruction
        if "=" in line:
            dest,rest = line.split('=')
            if ";" in rest:
                comp,jump = rest.split(";")
            else:
                comp=rest
                jump="null"
        else:
            comp,jump = line.split(";")
            dest = "null"

        destb = langSpec["dest"][dest]
        compb = langSpec["comp"][comp]
        jumpb = langSpec["jump"][jump]

        return "111"+compb+destb+jumpb

main()