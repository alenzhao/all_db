#!/usr/bin/python 
import re
import os
import pdb

#infl = open('phylop.wigFix.alt.filelist', 'r')
chrom = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','X','Y']
exe_cmd = open('extract_data_per_chr_cmd.sh', 'w')


for af in chrom:
	#aline = re.split('[_\.]', af.strip())
	#outfname = '_'.join([aline[0],aline[1]]) + '.js'
	outfname = 'chr'+af+'.js'
	out_f = open(outfname, 'w')
	out_f.write('var phylop = db.GRCh38_refgeneScores_5.find({\"_id.c\":'+af+'})\nwhile(phylop.hasNext())\n{\tprintjsononeline(phylop.next())}')
	out_f.close()
	exe_cmd.write('mongo AnnotationSource '+outfname+'  > chr'+af+'.json\n')


exe_cmd.close()
