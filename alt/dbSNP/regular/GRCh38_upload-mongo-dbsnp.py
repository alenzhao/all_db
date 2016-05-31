""" Imports a dbsnp vcf file format to mongodb
    Supporting only hg19 currently
    Key fields in mongodb: chr and genomic location
    TO DO: get rid of harcoded vcf and ref minor allele txt file
"""

import pymongo
import sys
import util
from pymongo import Connection
from pymongo.collection import Collection
import os 

if len(sys.argv) < 6: 
    print """
    Usage: python GRCh38_upload-mongo-dbsnp.py -m mapping_file dbsnpFiles name version
    Example: python GRCh38_upload-mongo-dbsnp.py -m GCF_000001405.28.assembly.txt 00-All.vcf,00-All_papu.vcf GRCh38_dbsnp 146
    """
    sys.exit()

args = util.getArgs(sys.argv)
mapping = util.readmapping(args["mapfile"])

c = Connection(args["host"], args["ip"])
db = c["AnnotationSource"]
db.drop_collection(args["table_name"])
dbsnp = db[args["table_name"]]
print "Created mongodb table " + args["table_name"]

print "Adding meta record..."
meta = { "_id" : "meta",
         "level" : "variant",
         "name" : "dbsnp",
         "type" : "DBSNP",
         "version" : 146,
         "links" : ["http://www.ncbi.nlm.nih.gov/SNP/snp_ref.cgi?rs={i}"],
         "desc" : "dbSNP",
         "buildVer" : ["5.2"],
         "reference" : ["GRCh38"]
       }
dbsnp.insert(meta)

print "Adding dbSNP records..."
count = 0
files = args["datafile"].split(",")
for ff in files:
    f = open(ff, "r")
    for line in f:
        line = line.strip()
        if line[0] == '#':
            continue
        fields = line.split("\t")
        if len(fields) < 8:
            print "Invalid vcf, Not enough columns in the provided vcf file " + ff 
            sys.exit(1)
        
        tchr = util.getValue(0, fields) 
        if tchr in mapping:
            tchr = mapping[tchr]
            if tchr == "na": 
                print "Unrecognized chromosome: " + line
                continue
        chr = util.getChr(tchr)
        ncbi = util.getNcbi(tchr)
        ct = util.getChrType(tchr)
        pos = int(util.getValue(1, fields))
        refA = util.getValue(3, fields)
        obsA = []
        obsA = util.getValue(4, fields).split(",")
        info = util.getValue(7, fields)

        version = ""
        if "RS=" in info:
            i = "rs" + info.split("RS=")[1].split(";")[0]        

        if "dbSNPBuildID=" in info:
            version = info.split("dbSNPBuildID=")[1].split(";")[0]
        
        variant_class = "" 
        if "VC=" in info:
            variant_class = info.split("VC=")[1].split(";")[0]
            if variant_class == 'DIV' or variant_class == 'STR' or variant_class == 'MIXED':
                variant_class = 'INDEL'
     
        rec = { "_id" : { "c" : chr, "p" : pos } }
        if ncbi:
            rec["_id"]["ncbi"] = ncbi
        if ct:
            rec["_id"]["ct"] = ct
        count = count + 1

        var_record = {
            "t" : [variant_class],
            "i" : i,
            "r" : refA,
            "o" : obsA,
        }

        if ("RSPOS=" in info):
            opos=info.split("RSPOS=")[1].split(";")[0] 
            opos=int(opos)
            # for indels, RSPOS is not anchored
            if (variant_class != 'INDEL' and opos != pos) or (variant_class == 'INDEL' and opos != (pos+1)) :
                var_record["opos"] = opos

        if "CAF=" in info:
            maf = info.split("CAF=")[1].split(";")[0]
            maf = maf.replace("[","")
            maf = maf.replace("]","")
            maf = maf.split(",")
            floatMaf = []
            temp = []
            for elem in maf:
                if elem != ".":
                    floatMaf.append(float(elem))
            if len(floatMaf) >= 2:
                temp = max(floatMaf)
                floatMaf.remove(temp)
                secondLargest = max(floatMaf)
                var_record["maf"] = round(secondLargest,3) 
                if maf[0] != ".": 
                    mafRef=float(maf[0])
                    if secondLargest == mafRef:
                        var_record["rma"] = 1
         
        if ("SAO=" in info):
            sao=info.split("SAO=")[1].split(";")[0]
            sao=int(sao)
            var_record["s"] = sao
            
        pushUnique = {"$addToSet":{"f":var_record}}
        dbsnp.update(rec, pushUnique, True, False)
          
    
print "Creating Index on chr and pos..." 
dbsnp.ensure_index([("_id.c", pymongo.ASCENDING),
                    ("_id.ncbi", pymongo.ASCENDING),
                    ("_id.ct", pymongo.ASCENDING),
                    ("_id.p", pymongo.DESCENDING)])
                      
ins_count = dbsnp.count()
print " ********** Processed " + str(count) + " records from the dbsnp file ********** "
print " ********** Inserted " + str(ins_count-1) + " records in the dbsnp table ********** "

