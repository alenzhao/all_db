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
			#reg_chr = re.compile('"_id" : {  "p" : (\d+),  "c" : ([a-zA-Z0-9]+),  "t" : "([A-Z_0-9\.]+)"')
			#alt_chr = re.compile('"p" : (\d+),  "c" : (\d+),  "t" : "([A-Z_0-9\.]+)",  "ncbi" : "([A-Z_0-9\.]+)",  "ct" : "(\w+)"')
			reg_chr = re.search('"_id" : {  "p" : (\d+),  "c" : (\d+),  "t" : "([A-Z_0-9\.]+)" }', aline)
			alt_chr = re.search('"p" : (\d+),  "c" : (\d+),  "t" : "([A-Z_0-9\.]+)",  "ncbi" : "([a-zA-Z0-9]+)",  "ct" : "([a-zA-Z]+)"', aline)
			var = []
			vid = ''
			#var = re.search('"_id" : {  "p" : (\d+),  "c" : ([a-zA-Z0-9]+),  "t" : "([A-Z_0-9\.]+)"', aline).groups()
			if reg_chr:
				var = reg_chr.groups()
				vid = 'chr'+var[1]
			elif alt_chr:
				var = alt_chr.groups()
				vid = 'chr'+var[1]+'_'+var[3]+'_'+var[4]
			else:
				print('unknow format\n')
			#if re.search(reg_chr, aline):
			#	var = re.search(reg_chr, aline).group()
			#elif alt_chr.match(aline):
			#	var = alt_chr.match(aline).group()
			#else:
			#	print('unknow format\n')

			#var = re.search('"_id" : {  "p" : (\d+),  "c" : ([a-zA-Z0-9]+),  "t" : "([A-Z_0-9\.]+)"', aline).groups()
			#sift = re.search('\"s\"\s+:\s+\"([\-0-9\.,]+|ALL_0s)\"', aline).groups()
			#pp = re.search('\"y\"\s+:\s+\"([\-0-9\.,]+|ALL_0s)\"', aline).groups()
			sift = []
			pp = []
			s_score = []
			y_score = []
			none_score = ''
			if re.search('\"s\"\s+:\s+\"([\-0-9\.,]+|ALL_0s)\"', aline):
				sift = re.search('\"s\"\s+:\s+\"([\-0-9\.,]+|ALL_0s)\"', aline).groups()
				s_score = (re.split(',', sift[0]))
				if len(s_score) == 1:
					none_score = '0.00'
			if re.search('\"y\"\s+:\s+\"([\-0-9\.,]+|ALL_0s)\"', aline):
				pp = re.search('\"y\"\s+:\s+\"([\-0-9\.,]+|ALL_0s)\"', aline).groups()
				y_score = (re.split(',', pp[0]))
				if len(y_score) ==1:
					none_score = '0.00'
			ref = re.search('\"ra\" : \"([A-Z])\"', aline).groups()
			
			#s_score = (re.split(',', sift[0]))
			#y_score = (re.split(',', pp[0]))
			
			if len(s_score) == len(y_score):
				for i in range(len(s_score)):
					out_f.write('\t'.join([vid, var[0], ref[0], ','.join([s_score[i] , y_score[i]]), var[2] ])+'\n')
			elif len(s_score) < len(y_score):
				for i in range(len(y_score)):
					#out_f.write('\t'.join(['chr'+ var[1], var[0], ref[0], ','.join(['0.00' , y_score[i]]), var[2] ])+'\n')
					out_f.write('\t'.join([vid, var[0], ref[0], ','.join([none_score , y_score[i]]), var[2] ])+'\n')
			elif len(s_score) > len(y_score):
				for i in range(len(s_score)):
					out_f.write('\t'.join([vid, var[0], ref[0], ','.join([s_score[i]  , none_score]), var[2] ])+'\n')

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


