#!/usr/bin/python 
import re
import os
import pdb

infl = open('phylop.wigFix.alt.filelist', 'r')
exe_cmd = open('executation_cmd.sh', 'w')


for af in infl:
	aline = re.split('[_\.]', af.strip())
	outfname = '_'.join([aline[0],aline[1]]) + '.js'
	out_f = open(outfname, 'w')
	out_f.write('var phylop = db.GRCh38_phylop_20151118.find({\"_id.ncbi\":\"'+aline[1]+'\"}).sort({\"_id.p\":1})\nwhile(phylop.hasNext()){\tprintjsononeline(phylop.next())}')
	out_f.close()
	exe_cmd.write('mongo AnnotationSource '+outfname+'  > '+ '_'.join([aline[0],aline[1]]) +'.json\n')


exe_cmd.close()
