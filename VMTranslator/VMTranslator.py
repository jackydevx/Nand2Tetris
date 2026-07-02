import json, sys, os

filepath=sys.argv[1]

def translate(line, line_number):
    global lang, filepath
    split_line=line.split()

    if len(split_line)==1:
        return lang[line].format(line_number=line_number)
    else:
        operation,segment,i=split_line
        this_or_that=""
        if segment=="pointer":
            if i=='0':
                this_or_that="3"
            else:
                this_or_that="4"
        return (lang[operation][segment].format(filename=os.path.basename(filepath),i=i,this_or_that=this_or_that))


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