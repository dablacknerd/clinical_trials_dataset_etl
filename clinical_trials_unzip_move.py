import os
import shutil
from zipfile import ZipFile
import datetime

cwd = os.getcwd()
zip_file_name = raw_input('Enter name of zip file WITHOUT the .zip extension: ')
zip_file = cwd + '/' + zip_file_name + '.zip'
today = datetime.datetime.now()
download_date = '_' + str(today.month) + '_' + str(today.day) + '_' + str(today.year)
zip_destination = cwd + '/' + zip_file_name + download_date + '_unzipped/'

print 'Creating unzip destination folder ---> %s' % (zip_destination)
os.makedirs(zip_destination)
print 'Unzip destination folder %s  ---> created' % (zip_destination)
zip = ZipFile(zip_file)

print "Unzipping %s ---> %s" % (zip_file,zip_destination)
zip.extractall(zip_destination)

print 'Done unzipping %s into destination %s' %(zip_file,zip_destination)
