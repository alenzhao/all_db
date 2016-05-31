#!/usr/bin/python

import re
import os
import pdb
import argparse


def paste_phylop(infl):
	in_file = open(infl, 'r')
	out_f = open(infl+'.score', 'w')
	for aline in in_file:
		if '{' in aline:
			aline = aline.strip()
			sc = re.search('\"sc\"\s+:\s+\"([\-0-9\.,]+)\"', aline).groups()
			out_f.write(re.sub(',','\n', sc[0]))
			out_f.write('\n')
	in_file.close()
	out_f.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input')
	args = parser.parse_args()
	paste_phylop(args.input)
	#infls = open(args.input, 'r')


