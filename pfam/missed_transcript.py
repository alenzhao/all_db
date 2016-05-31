#!/usr/bin/python
import re
import os
import pdb

vcf_f = open('create_hg38_pfam_from_VCF.json','r')
json_f = open('hg38_pfam.json','r')

vcf_t = {}
json_t = {}
for al in vcf_f:
	al = re.sub('"', '', al)
	pos = re.search('c:(\d+),ep:(\d+),p:(\d+)', al).groups()
	vcf_t['chr'+pos[0]+':'+pos[2]+'-'+pos[1]] = 1

vcf_f.close()
header = json_f.readline()
for al in json_f:
	al = re.sub('"', '', al)
	pos = re.search('c:(\d+),ep:(\d+),p:(\d+)', al).groups()
	json_t['chr'+pos[0]+':'+pos[2]+'-'+pos[1]] = 1
	

for t in vcf_t.keys():
	if not t in json_t.keys():
		print(t)
