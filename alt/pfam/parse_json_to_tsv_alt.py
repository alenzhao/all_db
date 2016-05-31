#!/usr/bin/python
import re
import os
import pdb

def json_to_tsv_pfam(inf, ouf):
	#json_f = open('hg38_pfam_alt.json', 'r')
	#tsv_f  = open('hg38_pfam_json_to_tsv', 'w')
	json_f = open(inf, 'r')
	tsv_f  = open(ouf, 'w')
	header = json_f.readline()
	json_to_tsv = {}
	for al in json_f:
		al = re.sub('\s+$', '', al)
		fun = re.findall('{(.*?)}', al)## fetech one fun block
	
		#al = re.sub('"', '', al)
		fun[0] = re.sub('"','', fun[0])
		pos = re.search('c:(\d+),ct:([a-zA-Z]+),ep:(\d+),ncbi:([0-9a-zA-Z]+),p:(\d+)', fun[0])
		regp = re.search('c:(\d+),ep:(\d+),p:(\d+)', fun[0])
		chrmp = re.search('c:(\d+),ep:(\d+),ncbi:([0-9a-zA-Z]+),p:(\d+)', fun[0])
		vid = ''
		if bool(pos):
			pos = pos.groups()
			vid = 'chr'+pos[0]+'_'+ pos[3]+'_'+ pos[1]+':'+pos[4]+':'+pos[2]
		elif bool(regp):
			regp = regp.groups()
			vid = 'chr'+regp[0] +':'+ regp[2] +':'+ regp[1]
		elif bool(chrmp):
			chrmp = chrmp.groups()
			vid = 'chr'+chrmp[0]+'_'+ chrmp[2] + ':'+chrmp[3]+':'+chrmp[1]
		json_val = ''
		al = re.sub('^{', '', al)
		al = re.sub('}$', '', al)
		#fun = re.findall('{(.*?)}', al)## fetech one fun block
		outstr = ''
		orig_cont = vid
		json_val = ''
		alt_alle_idx = 0
		for fidx in range(1,len(fun)):
			onef = {}
			tsv_f.write(vid)
			field = fun[fidx].split('\",')
			for fd in field:# for each sub-block in f
				fd = re.sub('"','', fd)
				kv = fd.split(':')
				tsv_f.write("\t"+kv[1])
				#f_cont = kv[1]
				#onef[kv[0]] = kv[1]
			tsv_f.write('\n')
	tsv_f.close()


#main():

if __name__ == '__main__':
	f1 = "hg38_pfam_alt.json"
	f2 = "hg38_pfam_json_to_tsv"
	json_to_tsv_pfam(f1, f2)
