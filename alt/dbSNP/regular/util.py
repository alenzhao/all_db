## utility methods for import scripts

# extract an element from array or empty string if not exists
def getValue(i, list):
    if i < len(list):
        return list[i]
    else:
        return ""

# translate chromosome string to int
def getChr(c):
    c = c.replace("chr","")
    if c == "X":
        return 23
    elif c == "Y":
        return 24
    elif c == "M" or c == "MT":
        return 25
    elif c == "PAR":
        return 26
    elif c == "Un":
        return 27
    elif "_" in c:
        subs = c.split("_")
        if len(subs) > 0:
            return getChr(getValue(0, subs))
    else:
        return int(c)

# get ncbi, for GRCh38
def getNcbi(c):
    ncbi = ''
    if "_" in c:
        subs = c.split("_")
        if len(subs) > 1:
            ncbi = getValue(1, subs)
    return ncbi

# get chr_type, for GRCh38 
def getChrType(c):
    ct = ''
    if "_" in c:
        subs = c.split("_")
        if len(subs) > 2:
            ct = getValue(2, subs)
    return ct    
 
# translation to positive strand
complement_dict = { 'A':'T', 'C':'G', 'T':'A', 'G':'C' }

def complement_bases(str):
    newstr = ''
    for i in range(len(str)):
        if str[i].upper() in 'ACTG':
           newstr = complement_dict[str[i].upper()] + newstr
        else: 
           newstr += str[i]
    return newstr

# parse arguments for import AnnotationSource
def getArgs(list):
    args = {} 
    i = 1
    if (list[1] == "-h"):
        args["host"] = list[2].split(":")[0].split("/")[0]
        args["ip"] = int(list[2].split(":")[1])
        i = 3
    else:
        args["host"] = "localhost"
        args["ip"] = 27017        
    if (list[i] == "-m"):
        args["mapfile"] = list[i+1]
        i = i + 2
# spaces in arguments should come in with special string "[]"
    if len(list) >= i:
        args["datafile"] = list[i].replace("[]", " ")
    if len(list) > i+2:
        args["name"] = list[i+1].replace("[]", " ")
        args["version"] = list[i+2].replace("[]", " ")
        if len(list) > i+3:
            args["table_name"] = list[i+3].replace("[]", "_")
        else:
            temp1 = args["name"].replace(" ", "_")
            temp2 = args["version"].replace(" ", "_")        
            args["table_name"] = temp1 + "_" + temp2
    return args

# reading mapping between BLAST and chromosome
def readmapping(filepath):
    mapping = {}
    f = open(filepath)
    for line in f:
        line = line.strip()
        if line[0] == '#':
            continue
        fields = line.split("\t")
        mapping[fields[6]] = fields[9]
    return mapping

