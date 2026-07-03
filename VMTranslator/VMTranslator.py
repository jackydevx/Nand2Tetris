import json, sys, os
from pathlib import Path

filepath=sys.argv[1]
filename=os.path.splitext(os.path.basename(filepath))[0]

def translate(line, line_number, filename):
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

code = []  # list of (line, source_filename) tuples

if os.path.isdir(filepath):
    thisdir = Path(filepath)
    target_file_path = os.path.join(filepath, os.path.basename(filepath) + '.asm')
    for f in thisdir.iterdir():
        if f.suffix == '.vm':
            file_stem = f.stem  # e.g. "Class1", "Class2" — no .vm extension
            with open(f, 'r') as file:
                for line in file.readlines():
                    code.append((line, file_stem))

elif os.path.isfile(filepath):
    target_file_path = os.path.join(os.path.dirname(filepath), os.path.basename(filepath).split('.')[0] + '.asm')
    file_stem = Path(filepath).stem
    with open(filepath, 'r') as file:
        code = [(line, file_stem) for line in file.readlines()]

with open(target_file_path, 'w') as target_file:
    target_file.write(lang['init']+'\n')
    target_file.write(lang['call'].format(function_name='Sys.init',line_number=0,n=0)+'\n')
    for line_number in range(len(code)):
        line, src_filename = code[line_number]
        line = line.strip()
        if "//" in line:
            line = line.split('//')[0].strip()
        if line:
            target_file.write(translate(line, line_number, src_filename) + '\n')