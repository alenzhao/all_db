#!/usr/bin/python

import os
import re
import pdb


#GRCh38_POSITION=7_KI270803v1_alt:516133
out_f = open('esp.alt.GRCh38.vcf', 'w')

esp = open('esp.alt.vcf', 'r')
for al in esp:
	aline = al.strip().split('\t')
	grch38 = re.search('GRCh38_POSITION=(.*?:\d+$)', aline[-1]).groups()
	grch38_cor = grch38[0].split(':')
	out_f.write('\t'.join([grch38_cor[0], grch38_cor[1], aline[2], aline[3],aline[4], aline[5],aline[6],aline[7] ]))
	out_f.write('\n')
out_f.close()






