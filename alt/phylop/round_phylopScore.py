#!/usr/bin/python
import re
import os
import pdb
import argparse

def round_phylop(inf):
	in_f = open(inf, 'r')
	out_f = open(inf+'.round', 'w')
	for aline in in_f:
		if 'fixed' not in aline:
			sc = round(float(aline.strip()),2)
			out_f.write(str(sc) + '\n')
			#out_f.write('\n')
	out_f.close()
	in_f.close()



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input')
	args = parser.parse_args()
	round_phylop(args.input)
