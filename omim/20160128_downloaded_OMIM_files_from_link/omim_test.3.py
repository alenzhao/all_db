#!/usr/bin/python
import re
import io
import pdb


## mongoDB content is based on genemap_processed1.txt
## genemap2.txt is downloaded

omim = {}
genemap = {}
genemap_fl = open('genemap_processed1.txt', 'r')
out_f  = open('test_omim', 'w')
for al in genemap_fl:
	al = re.sub('\s$', '', al)
	cont = al.split('\t')
	#cont = al.strip().split('\t')
	genes = cont[5].split(', ')
	gid = []
	for g in genes:
		gid.append( '"'+g.strip()+'"' )
	id_json = ','.join(gid)
	out_srt = ''
	if len(cont)==13 and cont[11] == '':
		out_srt = ''.join(['{"_id":{"gs":[', id_json, ']},"f":[{"cloc":"', cont[4], '","cm":"', cont[10], '","gstatus":"', cont[6], '","mcorr":"',cont[12],'","md":"', cont[9],'","mim":"', cont[8],'","title":"', cont[7],'"}]}'])
	elif len(cont) ==13 and cont[11] != '':
		out_srt = ''.join(['{"_id":{"gs":[', id_json, ']},"f":[{"cloc":"', cont[4], '","cm":"', cont[10], '","dis":"',cont[11],'","gstatus":"', cont[6], '","mcorr":"',cont[12],'","md":"', cont[9],'","mim":"', cont[8],'","title":"', cont[7],'"}]}'])
	elif len(cont) ==12 and cont[11] == '':
		out_srt = ''.join(['{"_id":{"gs":[', id_json, ']},"f":[{"cloc":"', cont[4], '","cm":"', cont[10], '","gstatus":"', cont[6], '","mcorr":"","md":"', cont[9],'","mim":"', cont[8],'","title":"', cont[7],'"}]}'])
	elif len(cont) ==12 and cont[11] != '':
		out_srt = ''.join(['{"_id":{"gs":[', id_json, ']},"f":[{"cloc":"', cont[4], '","cm":"', cont[10], '","dis":"',cont[11],'","gstatus":"', cont[6], '","mcorr":"","md":"', cont[9],'","mim":"', cont[8],'","title":"', cont[7],'"}]}'])

	#if len(cont) <=11:
	#	out_srt = ''.join(['{"_id":{"gs":[', id_json, ']},"f":[{"cloc":"', cont[4], '","cm":"', cont[10], '","gstatus":"', cont[6], '","mcorr":"","md":"', cont[9],'","mim":"', cont[8],'","title":"', cont[7],'"}]}'])
	#elif len(cont)  ==12 and cont[11] != '':
	#	out_srt = ''.join(['{"_id":{"gs":[', id_json, ']},"f":[{"cloc":"', cont[4], '","cm":"', cont[10], '","dis":"',cont[11],'","gstatus":"', cont[6], '","mcorr":"","md":"', cont[9],'","mim":"', cont[8],'","title":"', cont[7],'"}]}'])
	#elif len(cont) ==12 and cont[11] == '':
	#	out_srt = ''.join(['{"_id":{"gs":[', id_json, ']},"f":[{"cloc":"', cont[4], '","cm":"', cont[10], '","gstatus":"', cont[6], '","mcorr":"","md":"', cont[9],'","mim":"', cont[8],'","title":"', cont[7],'"}]}'])
	#elif len(cont) ==13:
		

	out_f.write(out_srt+'\n')


out_f.close()
genemap_fl.close()




