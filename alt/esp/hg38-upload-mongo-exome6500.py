""" Imports a vcf file (that has been left alligned) format to mongodb
    Assumes a FEATURE field as the first field in INFO in JSON format
    Key Fields in mongodb; chr and genomic location
"""

import pymongo
import sys
import util
from pymongo import Connection
from pymongo.collection import Collection
import re

if len(sys.argv) < 4: 
    print """
    Usage: hg38-upload-mongo-exome6500.py VCFFile name version
    Example: python hg38-upload-mongo-exome6500.py decisionsupport/test/data/cancer_hotspots_LeftAlligned739variants.vcf myVariantVCF v1
    """
    sys.exit()


args = util.getArgs(sys.argv)

c = Connection(args["host"], args["ip"])
db = c["AnnotationSource"]
db.drop_collection(args["table_name"])
vcf = db[args["table_name"]]
print "Created mongoDB table " + args["table_name"]

def getChrStr(chr):
    if chr == 23:
      return "X"
    elif chr == 24:
      return "Y"
    elif chr == 25:
      return "Z"
    else:
      return str(chr)

def getChrInt(chr):
    if chr == "X":
      return 23
    elif chr == "Y":
      return 24
    elif chr == "Z":
      return 25
    elif chr.isdigit():
      return int(chr)
    else:
      return -1

count = 0
filterkey=None
skip_count = 0

f = open(args["datafile"], "r")

for line in f:
    line = line.strip()
    if line[0] == '#':
        continue
    fields = line.split("\t")
    if len(fields) < 8:
        print line
        print " Invalid vcf, Not enough columns in the provided vcf file "
        sys.exit(1)
        
    chr = util.getChr(util.getValue(0,fields))
    pos = util.getValue(1,fields)
    id = util.getValue(2,fields)
    refA = util.getValue(3,fields)
    obsA = []
    obsA = util.getValue(4,fields).split(",")
    info = util.getValue(7,fields)

    # parse info field as list of key=value fields and add to record
    var_record = {}
    var_record["hg19_position"] = getChrStr(chr) + ":" + str(pos)

    skip = False
    for field in info.split(';'):
        if "=" in field:
           k = field.split('=')[0]
           v = field.split('=')[1]
           if k == "MAF":
             temp=float(v.split(',')[0])/100.0
             temp="%.4f"%temp
             var_record["EMAF"] = str(temp)
             temp2=float(v.split(',')[1])/100.0
             temp2="%.4f"%temp2
             var_record["AMAF"] = str(temp2)
             temp3=float(v.split(',')[2])/100.0
             temp3="%.4f"%temp3
             var_record["GMAF"] = str(temp3)
           elif k == "GRCh38_POSITION":
             if v == str("-1"):
               skip = True
               skip_count = skip_count + 1
               break
             else:
               chr == getChrInt(v.split(":")[0])
               if chr == -1:
                 skip = True
                 skip_count = skip_count + 1
                 break
               pos = int(v.split(":")[1])
           else:
             k = field.split('=')[0]
             v = field.split('=')[1]
             if filterkey == None:
               filterkey=k;
             var_record[k] = v
 
    if (skip):
      continue

    if len(fields) == 10:
	if "GT" in fields[8]:
	    GTFormat = util.getValue(8,fields)
	    GTValue= util.getValue(9,fields)
    	    GT_record = {}
    	    k=GTFormat.split(':')[0] 
  	    v=GTValue.split(':')[0] 
    	    var_record[k] = v;

    rec = { "_id" : { "c" : chr, "p" : pos } }

    var_record["id"] = id
    var_record["r"] = refA
    var_record["o"] = obsA
     
    pushUnique = {"$addToSet":{"f":var_record}}
    #pushUnique = {"$addToSet":{"f":info_dict_obj2}}
    vcf.update(rec, pushUnique, True, False)
    count = count + 1



""" Adding a meta data line"""
print "Adding meta record..."
meta = { "_id" : "meta",
         "level" : "variant",
         "name" : args["name"],
         "type" : "VARIANTDB",
         "version" : args["version"],
         "links" : ["http://evs.gs.washington.edu/EVS/PopStatsServlet?searchBy=Gene+Hugo&target={GL}&upstreamSize=0&downstreamSize=0&x=0&y=0"],
         "buildVer": ["5.2"],
         "desc" : "5000Exomes",
         "reference" : "GRCh38"
       }

if filterkey!=None:
    meta["filterKeys"] = [filterkey]

vcf.insert(meta)
print "Inserted meta record "

#print "Creating Index on chr, pos..."
vcf.ensure_index([("_id.c",pymongo.ASCENDING),
                   ("_id.p",pymongo.DESCENDING)])  
#print "Created index on {_id.chr:1, _id.pos:-1}"

ins_count = vcf.count()
print " ********** Processed " + str(count) + " records in file ********** "
print " ********** Inserted " + str(ins_count-1) + " records in table ********** "
print " ********** Skipped for missing GRCh38 coords " + str(skip_count) + " records in table ********** "

