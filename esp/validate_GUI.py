#!/usr/bin/python
import re
import os
import pdb

vcf_inf = 'GRCh38_test_annotate_VCF_JS_xz-full.tsv'
avar = {}
with open(vcf_inf, 'r') as inf:
	for aline in inf:
		if not re.match('^#', aline):
			#esp_v = re.search('AMAF=([0-9Ee\-\.]+):EMAF=([0-9Ee\-\.]+):GMAF=([0-9Ee\-\.]+)', aline).groups()
			esp_v = re.search('(AMAF=.*?GMAF=[A-Za-z0-9:\-\.]+)', aline).groups()
			cont = re.split('\t', aline)
			#vid = ':'.join([cont[0], cont[1]])
			avar[cont[0]] = esp_v[0]


dbf = 'hg38_esp6500_exome.json'
db_maf = {}
with open (dbf, 'r') as f:
	next(f)
	for al in f:
		al = re.sub('\s+$', '', al)
		al = re.sub('"', '', al)
		pos = re.search('c:(\d+),p:(\d+)', al).groups()
		vid = 'chr'+pos[0]+':'+pos[1]
		gmaf = re.search('GMAF:([0-9Ee\-\.]+),', al).groups()
		emaf = re.search('EMAF:([0-9Ee\-\.]+),', al).groups()
		amaf = re.search('AMAF:([0-9Ee\-\.]+),', al).groups()
		db_maf[vid] = 'AMAF='+amaf[0]+':EMAF='+emaf[0]+':GMAF='+gmaf[0]

outf = open('gui_exported_5000EXOME', 'w')
for vid, maf in avar.iteritems():
	if maf == db_maf[vid]:
		outf.write(vid+'\t'+maf+'\t'+db_maf[vid]+'yes\n')
	else:
		outf.write(vid+'\t'+maf+'\t'+db_maf[vid]+'no\n')
outf.close()
