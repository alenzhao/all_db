var phylop = db.GRCh38_phylop_20151118.find({"_id.ncbi":"GL383578v2"}).sort({"_id.p":1})
while(phylop.hasNext()){	printjsononeline(phylop.next())}