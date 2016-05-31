#!/usr/bin/python
import re
import os
import pdb
import copy

json_f = open('hg38_cosmic_75.json', 'r')
header = json_f.readline()

out_f = open('cosmic_convert_json_to_csv.tsv', 'w')

for al in json_f:
	al = al.strip()
	al = re.sub('\s', '', al)
	
	#al = re.sub('"', '', al)
	pos = re.search('c\":(\d+),\"p\":(\d+)', al).groups()
	#if pos[0] ==24 and pos[1] == 624389:
	#	print('here')
	vid = ':'.join([pos[1], pos[0]])
	json = {}
	al = re.sub('^{', '', al)
	al = re.sub('}$', '', al)
	fun = re.findall('{(.*?)}', al)## fetech one fun block
	outstr = ''
	
	for fidx in range(1,len(fun)):
		field = fun[fidx].split('","')
		for fd in field:# for each sub-block in f
			fd = re.sub('"', '', fd)
			kv = fd.split(':')
			json[kv[0]] = kv[1]
		#outstr = '\t'.join([json['g'], json['tid'], json['hid'],  json['ps'], json['ss'], json['ph'],json['dis'], 'COSM'+json['id'],json['cds'], json['aa'], pos[0]+':'+pos[1]+'-'+pos[1], json['st'], json['pmid'], json['hs']])
		if json['hid'] == '.':
			json['hid'] = ''
		if json['pmid'] == '.':
			json['pmid'] = ''
		outstr = '\t'.join([json['g'], json['tid'], json['hid'],  json['ps'], json['ss'], json['ph'],json['hs'], 'COSM'+json['id'],json['cds'], json['aa'], pos[0]+':'+pos[1]+'-'+pos[1],json['st'], json['pmid']])
		out_f.write(outstr+'\n')

out_f.close()



