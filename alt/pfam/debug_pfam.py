#!/usr/bin/python
import re
import os
import pdb
from parse_json_to_tsv_alt import json_to_tsv_pfam

inputf = 'hg38_pfam_alt.json'
outf   =  'hg38_pfam_json_to_tsv'
json_to_tsv_pfam(inputf, outf)


uc_pf_f = open('knownToPfam.txt', 'r')
uc_pf = {}
for al in uc_pf:
	aline = al.strip().



