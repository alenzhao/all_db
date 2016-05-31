### 
### Set the "f.ucsc" flags in dbsnp annotation source for snps whose 
### id appears in the UCSC common snps list.
###
### Programmer: Willa Chui
###
 
import pymongo
import sys
import time
from pymongo import Connection

if len(sys.argv) < 3:
    print """
        Usage: python set-ucsc-common-snps.py [-h host:ip] file tablename
        Example: python set-ucsc-common-snps.py snp137common.bed hg19_dbsnp_137 
        """ 
    sys.exit()
elif sys.argv[1] == "-h" and len(sys.argv) < 5:
    print """
        Usage: python set-ucsc-common-snps.py -h host:ip file tablename
        Example: python set-ucsc-common-snps.py -h apple:27017 snp137common.bed hg19_dbsnp_137
        """

# Argument index.
i = 1
host = "localhost"
ip = 27017
# User has entered host and ip.
if (sys.argv[1] == "-h"):
    i = 3
    host = sys.argv[2].split(":")[0]
    ip = int(sys.argv[2].split(":")[1])    
# Data file is the next argument.
datafile = sys.argv[i]
# The last argument is the table name.
tablename = sys.argv[i+1]

file_row_count = 0
db_rec_count = 0
ucsc_flag_count = 0
ts = time.time()

# Connect to mongodb.
c = Connection(host, ip)
db = c["AnnotationSource"]
table = db[tablename]

# create index to improve performance.
table.ensure_index("f.i", pymongo.ASCENDING)

f = open(datafile, "r")
for line in f:
    file_row_count = file_row_count + 1
    fields = line.strip().split("\t")
    if len(fields) >= 4:
        sid = fields[3]
        # Find records with the snp id.
        reclist = table.find({"f.i": sid})
        if reclist is None:
            print "Cannot find " + str(sid) + " in " + tablename + "."
        else:
            for rec in reclist:
                db_rec_count = db_rec_count + 1
                # Go through each record in features list.
                for r in rec["f"]:
                    if r["i"] == sid:
                        ucsc_flag_count = ucsc_flag_count + 1
                        r["ucsc"] = 1
                table.save(rec)

# Drop index.
table.drop_index("f.i_1")

print " ********** Read " + str(file_row_count) + " rows of data. ********** "
print " ********** Updated " + str(db_rec_count) + " records in " + tablename + ". ********** "
print " ********** Set " + str(ucsc_flag_count) + " ucsc flags in " + tablename + ". ********** "
print " ********** Elapsed time is " + str(time.time() - ts) + " seconds. ********** "
    
