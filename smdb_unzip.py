import gzip

def smdbp_gunzip(file_tupe):
	file_name = file_tupe[1]
	zipped_file = file_tupe[0]
	unzipped = 'file_path' + filename
	fout = open(unzipped,'w')
	fgzip = gzip.open(zipped_file,'r')
	content = fgzip.read()
	fout.write(content)
	fout.close()
	fgzip.close()