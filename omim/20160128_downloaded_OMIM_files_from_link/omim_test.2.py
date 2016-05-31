#!/usr/bin/python

import re
import os
import pdb

tgt_fl = open('genemap_processed1.txt','r')
src_fl = open('genemap2.txt','r')

src = {}
tgt = {}

#tmp = src_fl.readline()
#tmp = src_fl.readline()
#tmp = src_fl.readline()

for al in src_fl:
	cmt = re.match('^#', al)
	if not cmt:
		aline = al.strip().split('\t')
		if aline[3] =='':
			src[aline[5]] = '\t'.join([aline[4],aline[6],aline[7], aline[5]])
		else:
			src[aline[5]] = '\t'.join([aline[3],aline[6],aline[7], aline[5]])
		if len(aline) >= 12:
			src[aline[5]] = src[aline[5]]+'\t'+aline[11]

src_fl.close()

for al in tgt_fl:
	aline = al.strip().split('\t')
	tgt[aline[8]] = '\t'.join([aline[4],aline[5], aline[7],aline[8]])
	if len(aline) >= 10:
		tgt[aline[8]] = tgt[aline[8]] + '\t' + aline[9]
tgt_fl.close()

print(len(src.keys()))
print(len(tgt.keys()))

o_f = open('diff.1', 'w')

for mid in src.keys():
	if src[mid] != tgt[mid]:
		#o_f.write('\t'.join([mid, src[mid],tgt[mid]]))
		o_f.write('\t'.join([mid, src[mid]]))
		o_f.write('\n')
		o_f.write('\t'.join(['',tgt[mid]]))
		o_f.write('\n')
o_f.close()
