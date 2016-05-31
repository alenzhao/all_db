#!/usr/bin/python
import re
import os
import pdb

#orig_f = '20151110_clinvar_original.vcf';
clinvar_f  = open('test_chr17_43071011', 'r')
#clinvar_f = open('20151110_clinvar_original.vcf.mt', 'r')
clin = {}

for aline in clinvar_f:
	if not re.match('^#', aline):
		aline = re.sub('\s+$', '', aline)
		content = aline.split('\t')
		aVar = {
			'c': content[0],
			'p': content[1],
			'id': content[2],
			'ref': content[3],
			'alt': content[4],
		}
		if(aVar['c'] == 'X'):
			aVar['c'] = '23'
		elif (aVar['c']=='Y'):
			aVar['c'] = '24'
		elif(aVar['c']=='MT'):
			aVar['c'] = '25'

		num_allele = len(re.split(',', aVar['alt']))
				
		grp_size = []
		total_size = 0
		info = content[-1].split(';')
		for data in info:
			if re.match('CLNDSDBID', data):
				d_grp = re.split(',', data)
				for i in range(0, len(d_grp)):
					grp_size.append( len(re.split('\|', d_grp[i]))  )
					total_size +=  len(re.split('\|', d_grp[i]))

		unit_info = ['']*num_allele
		for io in info:
			data = re.split('=', io)
			if len(data)>1:
				d_grp = re.split(',', data[1])
				if len(d_grp) ==1:
					for i in range(0, num_allele):
						unit_info[i]= ';'.join([unit_info[i], '='.join([data[0],d_grp[0]])])
				else:
					for i in range(0, num_allele):
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
							#idx +=1
					else:
						for j in range(0, grp_size[k]):
							sub_unit_info[j+idx] = (  ';'.join([sub_unit_info[j+idx], '='.join([data[0],d_grp[j]])]) )
			idx += grp_size[k]
		print "done"


