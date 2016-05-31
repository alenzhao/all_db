#!/usr/bin/python
import re
import os
import pdb

i_f = open('20151110_clinvar_original.vcf','r')
cnt = {}
for i in range(1,26):
	cnt[i] = 0

o_f = open('clinvar_GRCh38_testData.oneAlt', 'w')
for al in i_f:
	if(not re.match('^#', al)):
		al = re.sub('\s+$', '',al)
		cols = al.split('\t')
		if cols[0] == 'X':
			cols[0] = 23
		elif cols[0] == 'Y':
			cols[0] =  24
		elif cols[0] == 'MT':
			cols[0] = 25

		clnsig = re.search('CLNSIG=([\d,|]+);', cols[-1]).groups()
		#if ',' in cols[4] or ( '|' in clnsig and  ',' in clnsig):
		if ',' not in cols[4] and '|' in clnsig[0] and  ',' in clnsig[0]:
		#if cols[-1].find('[,|]') == True:
		#if(cols[4].find(',') == True and cols[-1].find('[,|]') == True):
			cnt[int(cols[0])] = 1 + cnt[int(cols[0])]
			if (cnt[int(cols[0])] <= 20):
				o_f.write(al+'\n')

o_f.close()
i_f.close()

