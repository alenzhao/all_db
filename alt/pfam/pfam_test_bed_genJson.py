#!/usr/bin/python
import re
import os
import json
import pdb


pfam = {}
origf = open('Pfam-A.clans.tsv', 'r')
for ap in origf:
	ap = re.sub('\s+$','', ap)
	al = re.split('\t', ap)
	ele = {}
	ele['clan_id'] = al[1]
	ele['clan'] = al[2]
	ele['id'] = al[3]
	ele['name'] = al[4]
	if al[0] not in pfam.keys():
		pfam[al[0]] = {}
		pfam[al[0]] = ele
	else:
		pfam[al[0]] = ele
	

uid = {}
knownToPfam = open('knownToPfam.txt', 'r')
for al in knownToPfam:
	al = re.sub('\s+$','', al)
	ui = re.split('\t',al)
	if ui[0] not in uid.keys():
		uid[ui[0]] = []
	uid[ui[0]].append(ui[1])

cano = {}
knownCanonical_pfam = open('knownCanonical_pfam.txt', 'r')
for al in knownCanonical_pfam:
	al = re.sub('\s+$','', al)
	cor = re.split('\t', al)
	cor[0] = re.sub('^chr','', cor[0])
	if cor[0] == 'X':
		cor[0] = '23'
	elif cor[0] == 'Y':
		cor[0] = '24'
	elif cor[0] == 'M':
		cor[0] = '25'
	#if '_' in str(cor[0]):
		#print("cor[0]")
	cid = ':'.join([str(cor[0]), str(int(cor[1])+1), str(cor[2])])
	if cid not in cano.keys():
		cano[cid] = {}
	cano[cid]['c'] = cor[0]
	cano[cid]['p'] = int(cor[1])+1
	cano[cid]['ep'] = int(cor[2])
	cano[cid]['uid'] = cor[4]


err_no_knownToPfam = open('err_no_knownToPfam', 'w')
err_no_Pfam		   = open('err_no_Pfam', 'w')


pfam_order = {}
bedf = open('Pfam_29_20160125_commaReplaced.bed', 'r')
hd = bedf.readline()
for al in bedf:
	al = re.sub('\s+$','', al)
	info = re.split('\t', al)
	chro = ''
	pf = re.search('chr([0-9a-zA-Z_]+)\t(\d+)\t(\d+)\tacc=(PF[0-9]+);', al).groups()
	chro = pf[0]
	if pf[0] == 'X':
		chro = '23'
	elif pf[0] == 'Y':
		chro = '24'
	elif pf[0] == 'M':
		chro = '25'
	#elif pf[0] == 'chrUn_GL000213v1':
	#	chro = '27'

	#if pf[2] == '179680974':
		#pdb.set_trace()
		#print(1)
	pid = ':'.join([ chro, str(pf[1]), str(pf[2]) ])
	if pid not in pfam_order.keys():
		pfam_order[pid] = []
		pfam_order[pid].append(pf[3])
	else:
		pfam_order[pid].append(pf[3])


o_f = open('create_hg38_pfam_from_VCF.bed_order.json', 'w')
for gene,cor in cano.items():
	id_json = '\"_id\":{\"c\":' +cor['c']+ ',\"ep\":' +str(cor['ep'])+ ',\"p\":' +str(cor['p'])+ '}'
	if '_' in cor['c']:
		contig = re.split('_', cor['c'])
		if 'X' in cor['c']:
			id_json = '\"_id\":{\"c\":23' + ',\"ct\":'+'\"'+contig[2]+'\"'+',\"ep\":' +str(cor['ep'])+ ',\"ncbi\":'+'\"'+contig[1]+'\"' + ',\"p\":' +str(cor['p'])+ '}'
		elif 'Un' in cor['c']:
			id_json = '\"_id\":{\"c\":27' +',\"ep\":' +str(cor['ep'])+ ',\"ncbi\":'+'\"'+contig[1]+'\"' + ',\"p\":' +str(cor['p'])+ '}'
		else:
			id_json = '\"_id\":{\"c\":'+ contig[0] + ',\"ct\":'+'\"'+contig[2]+'\"'+',\"ep\":' +str(cor['ep'])+ ',\"ncbi\":'+'\"'+contig[1]+'\"' + ',\"p\":' +str(cor['p'])+ '}'
	f_block = []
	if cor['uid'] not in uid.keys():
		err_no_knownToPfam.write(cor['uid']+'\t'+gene+'\n')
	else:
		domains = uid[cor['uid']]
		p_idx = {}
		for d in domains:
			if d not in pfam.keys():
				err_no_Pfam.write(cor['uid']+d+'\n')
			else:
				p_idx[pfam_order[':'.join([cor['c'],str(cor['p']-1),str(cor['ep']),])].index(d)] = d
		
		for i in sorted(p_idx):
			d = p_idx[i]
			tmp = '{\"acc\":\"' +d+ '\",\"clan\":\"'+ pfam[d]['clan']+ '\",\"clan_id\":\"'  +pfam[d]['clan_id']+ '\",\"id\":\"' +pfam[d]['id']+ '\",\"name\":'+'\"' +pfam[d]['name']+'\"}'
			f_block.append(tmp)
		if len(f_block) > 0:
			f_cont = ','.join(f_block)
			one_json = '{' + id_json + ',\"f\":[' + f_cont + ']}';
			o_f.write(one_json+'\n')

o_f.close()
err_no_knownToPfam.close()
err_no_Pfam.close()




