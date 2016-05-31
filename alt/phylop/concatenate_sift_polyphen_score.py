#!/usr/bin/python

import re
import os
import pdb
import argparse


def paste_siftpolyphen(infl):
	in_file = open(infl, 'r')
	out_f = open(infl+'.score', 'w')
	for aline in in_file:
		if '{' in aline:
			aline = aline.strip()
			var = re.search('"_id" : {  "p" : (\d+),  "c" : ([a-zA-Z0-9]+),  "t" : "([A-Z_0-9\.]+)"', aline).groups()
			sift = re.search('\"s\"\s+:\s+\"([\-0-9\.,]+|ALL_0s)\"', aline).groups()
			pp = re.search('\"y\"\s+:\s+\"([\-0-9\.,]+|ALL_0s)\"', aline).groups()
			ref = re.search('\"ra\" : \"([A-Z])\"', aline).groups()
			
			s_score = (re.split(',', sift[0]))
			y_score = (re.split(',', pp[0]))
			
			if len(s_score) == len(y_score):
				for i in range(len(s_score)):
					out_f.write('\t'.join(['chr'+ var[1], var[0], ref[0], ','.join([s_score[i] , y_score[i]]), var[2] ])+'\n')
			elif len(s_score) < len(y_score):
				for i in range(len(s_score)):
					out_f.write('\t'.join(['chr'+ var[1], var[0], ref[0], ','.join(['0.00' , y_score[i]]), var[2] ])+'\n')
			elif len(s_score) > len(y_score):
				for i in range(len(y_score)):
					out_f.write('\t'.join(['chr'+ var[1], var[0], ref[0], ','.join([s_score[i]  , '0.00']), var[2] ])+'\n')

			#out_f.write(re.sub(',','\n', sc[0]))

			#out_f.write('\n')
	in_file.close()
	out_f.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input')
	args = parser.parse_args()
	paste_siftpolyphen(args.input)
	#infls = open(args.input, 'r')


