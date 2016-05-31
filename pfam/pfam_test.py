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
	#c = {}
	cid = ':'.join([str(cor[0]), str(int(cor[1])+1), str(cor[2])])
	if cid not in cano.keys():
		cano[cid] = {}
	cano[cid]['c'] = str(cor[0])
	cano[cid]['p'] = int(cor[1])+1
	cano[cid]['ep'] = int(cor[2])
	cano[cid]['uid'] = cor[4]


err_no_knownToPfam = open('err_no_knownToPfam', 'w')


o_f = open('create_hg38_pfam_from_VCF.json', 'w')
for gene,cor in cano.items():
	id_json = '\"_id\":{\"c\":' +cor['c']+ ',\"ep\":' +str(cor['ep'])+ ',\"p\":' +str(cor['p'])+ '}'
	f_block = []
	if cor['uid'] not in uid.keys():
		err_no_knownToPfam.write(cor['uid']+'\t'+gene+'\n')
	else:
		domains = uid[cor['uid']]
		for d in domains:
			#print(d)
			tmp = '{\"acc\":\"' +d+ '\",\"clan\":\"'+ pfam[d]['clan']+ '\",\"clan_id\":\"'  +pfam[d]['clan_id']+ '\",\"id\":\"' +pfam[d]['id']+ '\",\"name\":\"\\\"' +pfam[d]['name'] + '\\\"\"}'
			f_block.append(tmp)
		f_cont = ','.join(f_block)
		one_json = '{' + id_json + ',\"f\":[' + f_cont + ']}';
		o_f.write(one_json+'\n')

o_f.close()
	









o_f = open('hg38_pfam.tab', 'w')
with open('hg38_pfam.json', 'r') as i_f:
	pmeta = i_f.readline()
	for al in i_f:
		pfam_j = json.loads(al)
		out_str = ''
		listed_pfam = []
		for k,v in pfam_j['_id'].items():
			#o_f.write(k+':'+str(v)+'\t')
			out_str = out_str+ k+':'+str(v)+'\t'
		for f_idx in range(0,len(pfam_j['f'])):
			listed_pfam.append(pfam_j['f'][f_idx]['acc'])
			for k,v in pfam_j['f'][f_idx].items():
				out_str = out_str + k+':'+str(v)+'\t'
				#o_f.write(k+':'+str(v)+'\t')
		    #o_f.write('\n')
			p_acc = pfam_j['f'][f_idx]['acc']
			d_id = ':'.join([str(pfam_j['_id']['c']), str(pfam_j['_id']['p']),str(pfam_j['_id']['ep']) ])

			p_p = 'p:' +  str(cano[d_id]['p'])
			p_c = 'c:' +  str(cano[d_id]['c'])
			p_ep = 'ep:'+ str(cano[d_id]['ep'])
			p_clan_id = 'clan_id:' + pfam[p_acc]['clan_id']
			p_clan 	= 'clan:' 	+ pfam[p_acc]['clan']
			p_id 	= 'id' 		+ pfam[p_acc]['id']
			p_name 	= 'name:"' 	+ pfam[p_acc]['name'] + '"'
			
			#p_p = 'p:' + pfam_j['f'][f_idx]['acc']
			#p_p 	= 'p:' + pfam[pfam_j['f'][f_idx]]['p']
			#p_c 	= 'c:' + pfam[pfam_j['f'][f_idx]]['c']
			#p_ep 	= 'ep:'+ pfam[pfam_j['f'][f_idx]]['ep']
			#p_clan_id = 'clan_id' + pfam[pfam_j['f'][f_idx]]['clan_id']
			#p_clan 	= 'clan:' + pfam[pfam_j['f'][f_idx]]['clan']
			#p_id 	= 'id:' + pfam[pfam_j['f'][f_idx]]['id']
			#p_name 	= 'name:' + pfam[pfam_j['f'][f_idx]]['name']
			#p_acc 	= 'acc:' + pfam[pfam_j['f'][f_idx]]['acc']
			#orig_data = '\t'.join(['c:'+pfam[pfam_j['f'][f_idx]]['c'], 'p:'+ , 'acc:'+pfam[pfam_j['f'][f_idx]['acc']] 
			orig_data = '\t'.join([p_c, p_p, p_ep, p_clan_id, p_id, p_clan, p_name, p_acc])

o_f.close()
i_f.close()
print('1')



