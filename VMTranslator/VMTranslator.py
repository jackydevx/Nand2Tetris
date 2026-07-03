import json, sys, os

filepath=sys.argv[1]
filename=os.path.basename(filepath)

def translate(line, line_number):
    split_line=line.split()

    if len(split_line)==1:
        return lang[line].format(line_number=line_number)
    elif len(split_line)==2:
        cmd, label=split_line
        return lang[cmd].format(label=label)
    elif len(split_line)==3:
        if split_line[0]=='push' or split_line[0]=='pop':
            operation, segment, i = split_line
            #this or that management
            this_or_that=""
            if segment=="pointer":
                if i=='0':
                    this_or_that="3"
                else:
                    this_or_that="4"
            #refer to lang and format to return
            return (lang[operation][segment].format(filename=filename,i=i,this_or_that=this_or_that))
        else:
            operation, fName, n = split_line
            return (lang[operation].format(function_name=fName,line_number=line_number,n=n,nVarsInit="\nA=M\nM=0\n@SP\nM=M+1"*int(n)))


with open('language.json','r') as file:
    lang=json.load(file)

with open(filepath,'r') as file:
    code=file.readlines()

with open(os.path.splitext(filepath)[0]+'.asm','w') as target_file:
    for line_number in range(len(code)):
        code[line_number]=code[line_number].strip()
        if "//" in code[line_number]:
            code[line_number]=code[line_number].split('//')[0].strip()
        if code[line_number]:
            target_file.write(translate(code[line_number],line_number)+'\n')