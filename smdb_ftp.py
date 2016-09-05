import os
import re
import pickle
import ftplib
from datetime import date

def ftp(folder=None):
    download_file = None
    last_file = None
    if folder is None:
		foldr = "/{data}/{year}_medline_pubmed/"
	else:
		foldr = folder + '/'
    try:
        download_file = open('download.txt','r+')
        last_file = download_file.readline()
    except IOError:
        download_file = open('download.txt','w+')
    
    pattern =r'medline\d{2,}n\d{4,}.xml.gz'
    
    run_date_str = str(date.today())
    print " Connecting to Medline FTP site..."
    
    ftp = ftplib.FTP('ftp.nlm.nih.gov')
    ftp.login('anonymous','username')
    ftp.cwd('/nlmdata/.medlease/gz')

    print "Connection and login successful!!!"

    file_list =[]
    matches = []

    ftp.retrlines('NLST',file_list.append)
    
    for filr in file_list:
        if re.search(pattern,filr):
            j = re.search(pattern,filr)
            matches.append(j.group())
    size = len(matches)
    directory = foldr + run_date_str + "_DownLoad/"
    file_to_read = matches[size-1]
    if last_file:
        if file_to_read == last_file:
            print "No new file since last download of %s " % last_file
        else:
            print "New file found, since last download of file %s" % last_file
            print "Creating new folder for lastest download with folder name %s" % directory
            if os.path.exists(directory):
                pass
            else:
                os.makedirs(foldr + run_date_str + "_DownLoad/")
            download_file.write(file_to_read)
            file_name = foldr + run_date_str + "_DownLoad/" + file_to_read
            filw = open(file_name,'wb')
            print "Downloading new file %s to folder %s ...." % (file_to_read, directory)
            ftp.retrbinary('RETR ' + file_to_read ,filw.write,1024)
            
            print "Done with download"
            filw.close()
    else:
        print "Looks like you are running me for the first time on this machine"
        print "Creating new folder for new download with folder name %s" % directory
        if os.path.exists(directory):
            pass
        else:
            os.makedirs(run_date_str + "_DownLoad/")
        download_file.write(file_to_read)
        file_name = foldr + run_date_str + "_DownLoad/" + file_to_read
        filw = open(file_name,'wb')
        print "Downloading new file %s to folder %s ...." % (file_to_read,directory)
        ftp.retrbinary('RETR ' + file_to_read ,filw.write,1024)
    
        print "Done with download"
        filw.close()
    
    
    print "Closing FTP connection"    
    ftp.close()
    i = file_to_read.rfind('.gz')
	file_without_gz = file_to_read[:i]
	print "Done"
	return(file_name,file_without_gz)
