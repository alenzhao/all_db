#!/usr/bin/python
import re
import os
import pdb
import copy

orig_f = '20151110_clinvar_original.vcf';
#clinvar_f  = open('multiple_variant_same_loc', 'r')
#clinvar_f  = open('test', 'r')
clinvar_f = open('20151110_clinvar_original.vcf.mt', 'r')
clin = {}
#cln_allele = {}

for aline in clinvar_f:
	if(not re.match('^#', aline)):
		aline = re.sub('\s+$', '', aline)
		#aline = repr(aline)
		#aline = re.sub(r'\\x2c_', r'\\\\x2c_', aline)
		#aline = re.sub(r'\\x3d_', r'\\\\x3d_', aline)
		content = aline.split('\t')
		aVar = {}
		var_chr = content[0]
		var_p   = content[1]
		var_rsid  = content[2]
		var_ref = content[3]
		var_alt = content[4]
		var_id = ':'.join([var_chr, var_p ])
		if( var_chr== 'X'):
			var_chr = '23'
		elif (var_chr =='Y'):
			var_chr = '24'
		elif(var_chr =='MT'):
			var_chr = '25'
		
		alt_allele = re.split(',', var_alt)
		num_allele = len(re.split(',', var_alt))
		grp_size = []
		total_size = 0
		cln_allele = {}
		info = content[-1].split(';')
		for data in info:
			if re.match('CLNDSDBID', data):
				d_grp = re.split(',', data)
				for i in range(0, len(d_grp)):
					grp_size.append( len(re.split('\|', d_grp[i]))  )
					total_size +=  len(re.split('\|', d_grp[i]))
			if re.match('CLNALLE=', data):
				cln_allele = data.split(',')

		cln_allele[0] = re.sub('CLNALLE=', '', cln_allele[0])
		pop_0 = 0
		for r in range(0,len(cln_allele)):
			if int(cln_allele[r]) ==0:
				cln_allele[r] = alt_allele[0]
			else:
				cln_allele[r] = alt_allele[int(cln_allele[r])-1]

		if pop_0:
			cln_allele.pop(0)


		unit_info = ['']*len(grp_size)
		for g in range(0, len(grp_size)):
			unit_info[g] = unit_info[g] + 'o='+cln_allele[g]
		
		for io in info:
			data = re.split('=', io)
			if len(data)>1:
				d_grp = re.split(',', data[1])
				#if data[0] == 'CLNDBN':
				#	data[1] = data[1].replace('cancer\\x2c','cancer')
				if len(d_grp) ==1:
					for i in range(0, len(grp_size)):
						unit_info[i] = ';'.join([unit_info[i], '='.join([data[0],d_grp[0]])])
						#unit_info[i] = ';'.join([unit_info[i], '='.join(['o', ]))
				elif data[0] == 'CLNREVSTAT' or data[0] == 'CAF':
					for i in range(0, len(grp_size)):
						unit_info[i] = ';'.join([unit_info[i], '='.join([data[0],data[1]])])
				else:
					for i in range(0, len(grp_size)):
						unit_info[i] = (';'.join([unit_info[i], '='.join([data[0],d_grp[i]])]) )

		idx = 0
		sub_unit_info = ['']*total_size
		for k in range(0,len(unit_info)):
			u = re.sub('^;', '', unit_info[k])
			u_info = re.split(';', u)
			for ui in u_info:
				data = re.split('=', ui)
				if len(data) >1:
					d_grp = re.split('\|', data[1])
					if len(d_grp) ==1:
						for i in range(0,grp_size[k]):
							sub_unit_info[i+idx] = ( ';'.join([sub_unit_info[i+idx], '='.join([data[0],d_grp[0]])]) )
					elif data[0] == 'CLNREVSTAT' or data[0] == 'CAF':
						for i in range(0,grp_size[k]):
							sub_unit_info[i+idx] = ( ';'.join([sub_unit_info[i+idx], '='.join([data[0],data[1]])]) )
					else:
						for j in range(0, grp_size[k]):
							sub_unit_info[j+idx] = (  ';'.join([sub_unit_info[j+idx], '='.join([data[0],d_grp[j]])]) )
							
			idx += grp_size[k]

		idx = 0
		for chk in sub_unit_info:
			info = chk.split(';')
			tmp = copy.deepcopy(aVar)
			for ele in info:  ## parse the info column of VCF file
				pair = ele.split('=')
				if(len(pair) ==2):
					## deal with multiple annotation for one allele
					##specific for clinvar
					if(pair[0] == 'CLNSIG'):
						if pair[1] == '0':
							pair[1] = 'unknown'
						elif pair[1] == '1':
							pair[1] = 'untested'
						elif pair[1] == '2':
							pair[1] = 'non-pathogenic'
						elif pair[1] == '3':
							pair[1] = 'probable-non-pathogenic'
						elif pair[1] == '4':
							pair[1] = 'probable-pathogenic'
						elif pair[1] == '5':
							pair[1] = 'pathogenic'
						elif pair[1] == '6':
							pair[1] = 'drug-response'
						elif pair[1] == '7':
							pair[1] = 'histocompatibility'
						elif pair[1] == '255':
							pair[1] = 'other'
					elif pair[0] == 'CLNACC':
						pair[1] = re.sub('\.\d+$', '', pair[1])

					tmp[pair[0]] = pair[1]
			#tmp['o'] = cln_allele[idx]
			#idx+=1
			tmp['r'] = var_ref
			tmp['id'] = var_rsid
			if var_id not in clin.keys():
				#clin[var_id] = ['']*total_size
				clin[var_id] = []
				clin[var_id].append(tmp)
				#clin[var_id][idx] = tmp
			else:
				clin[var_id].append(tmp)
				#clin[var_id][idx] = tmp
			idx +=1
			#print "%s\n" % tmp
			#print "%s\b" % clin

json_f = open('multiple_json', 'r')
dig_log = open('comparison_log', 'w')

#json_f = open('hg38_clinvar.json.1k', 'r')
#header = json_f.readline()
for al in json_f:
	al = re.sub('\s+$', '', al)
	comp_json = al
	al = re.sub('"', '', al)
	pos = re.search('p : (\d+), c : (\d+)', al).groups()
	orig_cont = clin[':'.join([pos[1], pos[0]])] ## fetch content for this location
	vid = ':'.join([pos[1], pos[0]])
	json_val = ''
	al = re.sub('^{', '', al)
	al = re.sub('}$', '', al)
	fun = re.findall(' { (.*?) }', al)## fetech one fun block
	field = fun[1].split(', ')                 ## split fields in fun block
	outstr = ''

	alt_alle_idx = 0
	for anno in clin[':'.join([pos[1],pos[0]])]:
		asJson_cont = ''
		for fd in field:
			kv = fd.split(' : ')
			if kv[0] == 'o':
				f_cont = '"'+kv[0]+'"'+' : '+'[ "'+anno[kv[0]]+'" ]'
			else:
				f_cont = '"'+kv[0]+'"'+' : '+'"'+anno[kv[0]]+'"'  ## "RSPOS" : "583" e.g.
			
			asJson_cont = ', '.join([asJson_cont, f_cont])
		asJson_cont = re.sub('^, ','',asJson_cont)
		asJson_cont = '{ '+asJson_cont+' }'
		
		if json_val == '':
			json_val = asJson_cont
		else:
			json_val = ', '.join([json_val, asJson_cont])
		alt_alle_idx +=1

	json_line = ''.join(['{"_id":{"p":',pos[0], ',"c":', pos[1], '},"f":[', json_val,']}'])
	#print "%s" % json_line	
	json_line = json_line.replace('\\x2c', '')
	json_line = json_line.replace('\\x3d', '')
	comp_json = comp_json.replace('\\\\x2c', '')
	comp_json = comp_json.replace('\\\\x3d', '')
	#json_line = re.sub(r'\x2c', r'x2c', json_line)
	#json_line = repr(json_line)
	if(not json_line == comp_json):
	#	print "%s:%s not equal between original file and MongoDB Json file" % pos[0], pos[1]
		dig_log.write(pos[0]+':'+pos[1] +'\n')
		dig_log.write(json_line+'\n'+comp_json+'\n')

dig_log.close()
