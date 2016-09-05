import os
import sys
from bs4 import BeautifulSoup as bs
import codecs
import datetime
import pyodbc
import shutil
import zipfile


class EndOfQueue(Exception):
    pass

def unzip_files():
    cwd = os.getcwd()
    zip_file_name = raw_input('Enter zip file name: ')
    zip_path = cwd + '/clinical_trials_zip/' + zip_file_name
    clinical_trials_folder = return_folder_name()
    unzipped_folder = cwd + '/' + clinical_trials_folder + '/'
    zipped_file = zipfile.ZipFile(zip_path)
    print 'Extracting files...'
    zipped_file.extractall(unzipped_folder)
    zipped_file.close()
    print 'Extraction complete'
    #delete zip file
    print 'Deleting zip file...'
    os.unlink(zip_path)
    print 'Zip file deleted'
    print 'Done!!!'
    return unzipped_folder

def return_folder_name():
    today = datetime.datetime.now()
    day = today.day
    month = today.month
    year = today.year
    hour = today.hour
    minute = today.minute
    second = today.second
    return_string = "clinical_trials_%s_%s_%s_%s_%s_%s" % (str(today.year),str(today.month),str(today.day),str(today.hour),str(today.minute),str(today.second))
    return return_string

def write_out(nctID,fullDesc):
    cwd_wo = os.getcwd()
    today = datetime.datetime.now()
    download_date = '_' + str(today.month) + '_' + str(today.day) + '_' + str(today.year)
    final_destination_folder = cwd + '/' + 'clinical_trials' + download_date
    if os.path.exists(final_destination_folder) == False :
        os.makedirs(final_destination_folder)
    if fullDesc:
        file_name = str(nctID) + '.txt'
        fulloutput_path = final_destination_folder + "/" + file_name
        writer = open(fulloutput_path,'wb')
        writer.write(fullDesc)
        writer.close()
        return 1
    else:
        return 0

def create_files_for_semrep(fileCue,path):
    while True:
        row = fileCue.get()
        if isinstance(row,EndOfQueue):
            fileCue.task_done()
        try:
            full_path = path + str(row[0]) + '.txt'
            writer = open(full_path,'wb')
            writer.write(row[1])
            writer.close()
        except:
            exc_type, exc_value = sys.exc_info()[:2]
            print "Problem in subroc %s:%s" % (exc_type, exc_value)
        fileCue.task_done()
        #finally:
        #continue

def is_tag_empty(tag):
    if tag:
        return tag.text
    else:
        return None

def is_tag_textblock_empty(tag):
    if tag:
        return tag.textblock.text
    else:
        return None

def is_tag_city_empty(tag):
    if tag:
        return tag.city
    else:
        return None

def is_tag_facility_name_empty(tag):
    if tag:
        return tag.text.split('\n')[1].encode('UTF-8','strict')
    else:
        return None

def is_tag_state_empty(tag):
    if tag:
        return tag.state
    else:
        return None

def is_tag_country_empty(tag):
    if tag:
        return tag.country
    else:
        return None

def convert_string_to_date(date_string):
    month_dict = {'january':1,'february':2,'march':3,
                'april':4, 'may':5, 'june':6, 'july':7,
                'august':8, 'september':9, 'october':10,
                'november':11, 'december':12
                }
    if date_string:
        m = date_string.split(None)
        date_month = int(month_dict[m[0].lower()])
        date_day = int(m[1].rstrip(','))
        date_year = int(m[2])
        return str(datetime.date(date_year,date_month,date_day))
    else:
        return None
def strip_utf8(content):
    #line = content.decode('latin-1')
    line = content
    try:
         #Misc non-latin formatting characters
         line = line.replace(u'\u2018', '')  # left single quote mark
         line = line.replace(u'\u2019', '')  # right single quote mark
         line = line.replace(u'\u201C', '')  # left double quote mark
         line = line.replace(u'\u201D', '')  # right double quote mark
         line = line.replace(u'\u2010', '-')  # hyphen
         line = line.replace(u'\u2011', '-')  # non-break hyphen
         line = line.replace(u'\u2012', '-')  # figure dash
         line = line.replace(u'\u2013', '-')  # dash
         line = line.replace(u'\u2014', '-')  # some sorta dash
         line = line.replace(u'\u2015', '-')  # long dash
         line = line.replace(u'\u2017', '_')  # double underscore
         line = line.replace(u'\u2014', '-')  # some sorta dash
         line = line.replace(u'\u2016', '|')  # long dash
         line = line.replace(u'\u2024', '...')  # ...
         line = line.replace(u'\u2025', '...')  # ...
         line = line.replace(u'\u2026', '...')  # ...
         line = line.replace(u'\u2000', ' ')  # ...
         line = line.replace(u'\u2001', '')  # ...
         line = line.replace(u'\u2002', '')  # ...
         line = line.replace(u'\u2003', '')  # ...
         line = line.replace(u'\u2004', '')  # ...
         line = line.replace(u'\u2005', '')  # ...
         line = line.replace(u'\u2006', '')  # ...
         line = line.replace(u'\u00a9', '')  # copyright
         line = line.replace(u'\u00ae', '')  # registered trademark
         line = line.replace(u'\u2122', '')  # trademark
         line = line.replace(u'\u00b0', '')  # degree sign
         line = line.replace(u'\u00b7', '.')  # middle dot
         line = line.replace(u'\u00bc', '0.25')  # Vulgar 1/4
         line = line.replace(u'\u00bd', '0.50')  # Vulgar 1/2
         line = line.replace(u'\u00be', '0.75')  # Vulgar 3/4
         line = line.replace(u'\u00bf', '?')  # Upside down question mark
         line = line.replace(u'\u00b5', 'u')  # Micro sign
         line = line.replace(u'\u00d7', 'x')  # Multiplication sign
         line = line.replace(u'\u2217', 'x')  # Other multiplication sign
         line = line.replace(u'\u00f7', '')  # Division sign
         line = line.replace(u'\u2265', '>=')  # Greater-than equal to sign
         line = line.replace(u'\u2264', '<=')  # Less-than equal to sign
         line = line.replace(u'\u223c', '')  # ~ operator
         line = line.replace(u'\u22ef', '')  # ... operator
         line = line.replace(u'\u00a3', '')  # GB pound sign
         line = line.replace(u'\xa0', u' ')  # ... operator
         line = line.replace(u'\u2192', u' ')  # ... operator
         line = line.replace(u'\u00a5', '')  # yen sign
         line = line.replace(u'\xa7', '')  # ... sign
         line = line.replace(u'\u20ac', '')  # euro sign
         line = line.replace(u'\u0192', 'f')  # function operator
         line = line.replace(u'\u221e', '')  # infinity operator
         line = line.replace(u'\u2200', '')  # ... operator
         line = line.replace(u'\u2202', '')  # PDE operator
         line = line.replace(u'\u2207', '')  # NABLA operator
         line = line.replace(u'\u2206', '')  # increment operator
         line = line.replace(u'\u2208', '')  # element of operator
         line = line.replace(u'\u2209', '')  # not element operator
         line = line.replace(u'\u220f', '')  # array product
         line = line.replace(u'\u2211', '')  # summation
         line = line.replace(u'\u2212', '-')  # minus sign
         line = line.replace(u'\u221a', '')  # root
         line = line.replace(u'\u2260', '!=')  # not equal operator
         line = line.replace(u'\u27c2', '')  # perpendicular
         line = line.replace(u'\u2191', '')  # up arrow
         line = line.replace(u'\u2193', '')  # down arrow
         line = line.replace(u'\u2261', '')  # triple bond
         line = line.replace(u'\u222b', '')  # integral
         line = line.replace(u'\u2030', '')  # per 1k
         line = line.replace(u'\u2031', '')  # per 10k
         line = line.replace(u'\u2032', '')  # prime
         line = line.replace(u'\u2033', '')  # double prime
         line = line.replace(u'\u2034', '')  # triple prime
         line = line.replace(u'\u2248', '')  # wavy equals
         line = line.replace(u'\u2245', '=')  # aprox equals
         line = line.replace(u'\u2243', '')  # asymptotically equal
         line = line.replace(u'\u27e8', '')  # left bracket
         line = line.replace(u'\u27e9', '')  # right bracket
         line = line.replace(u'\u2310', '')  # not sign
         line = line.replace(u'\xb1', '')  # not sign
         line = line.replace(u'\u2201', '')  # compliment
         line = line.replace(u'\u2204', '')  # not exists sign
         line = line.replace(u'\u2203', '')  # exists sign
         line = line.replace(u'\u2205', '')  # empty set
         line = line.replace(u'\u220a', '')  #
         line = line.replace(u'\u220b', '')  #
         line = line.replace(u'\u220c', '')  #
         line = line.replace(u'\u220d', '')  #
         line = line.replace(u'\u220e', '')  #
         line = line.replace(u'\u220f', '')  #
         line = line.replace(u'\u2213', '')  #
         line = line.replace(u'\u2214', '')  #
         line = line.replace(u'\u2215', '')  #
         line = line.replace(u'\u2216', '')  #
         line = line.replace(u'\u2218', '')  #
         line = line.replace(u'\u2210', '')  #
         line = line.replace(u'\u0300', 'a')  #
         line = line.replace(u'\u2009', ' ')  #
         line = line.replace(u'\xaf', ' ')  #
         line = line.replace(u'\u2022', '')  #
         line = line.replace(u'\u043a', '')  #
         line = line.replace(u'\u200a', '')  #
         line = line.replace(u'\u200e', '')  #
         line = line.replace(u'\u2100', '')  #
         line = line.replace(u'\u2103', 'C')  # Degree C
         line = line.replace(u'\xb4', '')  #
         line = line.replace(u'\xba', '')  #
         line = line.replace(u'\u226a', '<')  # Much less than
         line = line.replace(u'\u226b', '>')  # Much greater than
         line = line.replace(u'\u2008', '')  # White space
         line = line.replace(u'\u212b', 'A')  # Angstrom sign
         line = line.replace(u'\u221d', '')  # Proportional to sign
         line = line.replace(u'\u0327', '')  #
         line = line.replace(u'\u2190', '')  # Reaction left arrow
         line = line.replace(u'\u2192', '')  # Reaction right arrow
         line = line.replace(u'\u02c3', '>')  #
         line = line.replace(u'\u02c2', '<')  #
         line = line.replace(u'\ue605', '')  #
         line = line.replace(u'\u2a7d', '<=')  #
         line = line.replace(u'\u2a7e', '=>')  #
         line = line.replace(u'\u02c2', '<')  #
         line = line.replace(u'\u22c5', '')  #
         line = line.replace(u'\u2550', '=')  #
         line = line.replace(u'\u2044', '/')  #
         line = line.replace(u'\u0303', '')  #
         line = line.replace(u'\u22a5', '')  #
         line = line.replace(u'\u25cf', '')  #
         line = line.replace(u'\u2267', '')  #
         line = line.replace(u'\ue232', '')  #
         line = line.replace(u'\u030a', '')  #
         line = line.replace(u'\uf8ff', '')  # This is the sign for the Klingon Empire
         line = line.replace(u'\ue2f6', '')  #
         line = line.replace(u'\u2225', '')  #
         line = line.replace(u'\u2020', '')  #
         line = line.replace(u'\u0308', '')  #
         line = line.replace(u'\u02d9', '')  #
         line = line.replace(u'\u02dc', '')  #
         line = line.replace(u'\u025b', '')  #
         line = line.replace(u'\ufffd', '')  #
         line = line.replace(u'\u03a0', '')  #
         line = line.replace(u'\u22dc', '')  #
         
         #Greek characters
         line = line.replace(u'\u0391', 'A')  # Greek Capital Alpha
         line = line.replace(u'\u0392', 'B')  # Greek Capital Beta
         line = line.replace(u'\u0393', '')  # Greek Capital Gamma
         line = line.replace(u'\u0394', '')  # Greek Capital Delta
         line = line.replace(u'\u0395', 'E')  # Greek Capital Epsilon
         line = line.replace(u'\u0396', 'Z')  # Greek Capital Zeta
         line = line.replace(u'\u0397', 'H')  # Greek Capital Eta
         line = line.replace(u'\u0398', '')  # Greek Capital Theta
         line = line.replace(u'\u0399', 'I')  # Greek Capital Iota
         line = line.replace(u'\u039a', 'K')  # Greek Capital Kappa
         line = line.replace(u'\u039b', '')  # Greek Capital Lambda
         line = line.replace(u'\u039c', 'M')  # Greek Capital Mu
         line = line.replace(u'\u039d', 'N')  # Greek Capital Nu
         line = line.replace(u'\u039e', '')  # Greek Capital Xi
         line = line.replace(u'\u039f', 'O')  # Greek Capital Omicron
         line = line.replace(u'\u03a1', 'P')  # Greek Capital Rho
         line = line.replace(u'\u03a3', '')  # Greek Capital Sigma
         line = line.replace(u'\u03a4', 'T')  # Greek Capital Tau
         line = line.replace(u'\u03a5', 'Y')  # Greek Capital Upsilon
         line = line.replace(u'\u03a6', '')  # Greek Capital Phi
         line = line.replace(u'\u03a7', 'T')  # Greek Capital Chi
         line = line.replace(u'\u03a8', '')  # Greek Capital Psi
         line = line.replace(u'\u03a9', '')  # Greek Capital Omega
         line = line.replace(u'\u03b1', 'a')  # Greek small alpha
         line = line.replace(u'\u03b2', 'b')  # Greek small beta
         line = line.replace(u'\u03b3', '')  # Greek small gamma
         line = line.replace(u'\u03b4', '')  # Greek small delta
         line = line.replace(u'\u03b5', 'e')  # Greek small epsilon
         line = line.replace(u'\u03b6', '')  # Greek small zeta
         line = line.replace(u'\u03b7', '')  # Greek small eta
         line = line.replace(u'\u03b8', '')  # Greek small theta
         line = line.replace(u'\u03b9', 'i')  # Greek small iota
         line = line.replace(u'\u03ba', 'k')  # Greek small kappa
         line = line.replace(u'\u03bb', '')  # Greek small lambda
         line = line.replace(u'\u03bc', 'u')  # Greek small mu
         line = line.replace(u'\u03bd', 'v')  # Greek small nu
         line = line.replace(u'\u03be', '')  # Greek small xi
         line = line.replace(u'\u03bf', 'o')  # Greek small omicron
         line = line.replace(u'\u03c0', '')  # Greek small pi
         line = line.replace(u'\u03c1', 'p')  # Greek small rho
         line = line.replace(u'\u03c2', 'c')  # Greek small final sigma
         line = line.replace(u'\u03c3', '')  # Greek small sigma
         line = line.replace(u'\u03c4', 't')  # Greek small tau
         line = line.replace(u'\u03c5', 'u')  # Greek small upsilon
         line = line.replace(u'\u03c6', '')  # Greek small phi
         line = line.replace(u'\u03c7', 'x')  # Greek small chi
         line = line.replace(u'\u03c8', 'x')  # Greek small psi
         line = line.replace(u'\u03c9', 'w')  # Greek small omega
         
         #Super and sub scripts
         line = line.replace(u'\u207A', '+')
         line = line.replace(u'\u207B', '-')
         line = line.replace(u'\u2070', '0')
         line = line.replace(u'\u00B9', '1')
         line = line.replace(u'\u00B2', '2')
         line = line.replace(u'\u00B3', '3')
         line = line.replace(u'\u2074', '4')
         line = line.replace(u'\u2075', '5')
         line = line.replace(u'\u2076', '6')
         line = line.replace(u'\u2077', '7')
         line = line.replace(u'\u2078', '8')
         line = line.replace(u'\u2079', '9')
         line = line.replace(u'\u208B', '-')
         line = line.replace(u'\u2080', '0')
         line = line.replace(u'\u2081', '1')
         line = line.replace(u'\u2082', '2')
         line = line.replace(u'\u2083', '3')
         line = line.replace(u'\u2084', '4')
         line = line.replace(u'\u2085', '5')
         line = line.replace(u'\u2086', '6')
         line = line.replace(u'\u2087', '7')
         line = line.replace(u'\u2088', '8')
         line = line.replace(u'\u2089', '9')
         line = line.replace(u'\u2071', 'i')
         
         #Non English Latin characters (Latin Extended-A)
         
         line = line.replace(u'\u0100', 'A')
         line = line.replace(u'\u0101', 'a')
         line = line.replace(u'\u0102', 'A')
         line = line.replace(u'\u0103', 'a')
         line = line.replace(u'\u0104', 'A')
         line = line.replace(u'\u0105', 'a')
         line = line.replace(u'\u0106', 'C')
         line = line.replace(u'\u0107', 'c')
         line = line.replace(u'\u0108', 'C')
         line = line.replace(u'\u0109', 'c')
         line = line.replace(u'\u010a', 'C')
         line = line.replace(u'\u010b', 'c')
         line = line.replace(u'\u010c', 'C')
         line = line.replace(u'\u010d', 'c')
         line = line.replace(u'\u010e', 'D')
         line = line.replace(u'\u010f', 'd')
         line = line.replace(u'\u0110', 'D')
         line = line.replace(u'\u0111', 'd')
         line = line.replace(u'\u0112', 'E')
         line = line.replace(u'\u0113', 'e')
         line = line.replace(u'\u0114', 'E')
         line = line.replace(u'\u0115', 'e')
         line = line.replace(u'\u0116', 'E')
         line = line.replace(u'\u0117', 'e')
         line = line.replace(u'\u0118', 'E')
         line = line.replace(u'\u0119', 'e')
         line = line.replace(u'\u011a', 'E')
         line = line.replace(u'\u011b', 'e')
         line = line.replace(u'\u011c', 'G')
         line = line.replace(u'\u011d', 'g')
         line = line.replace(u'\u011e', 'G')
         line = line.replace(u'\u011f', 'g')
         line = line.replace(u'\u0120', 'G')
         line = line.replace(u'\u0121', 'g')
         line = line.replace(u'\u0122', 'G')
         line = line.replace(u'\u0123', 'g')
         line = line.replace(u'\u0124', 'H')
         line = line.replace(u'\u0125', 'h')
         line = line.replace(u'\u0126', 'H')
         line = line.replace(u'\u0127', 'h')
         line = line.replace(u'\u0128', 'I')
         line = line.replace(u'\u0129', 'i')
         line = line.replace(u'\u012a', 'I')
         line = line.replace(u'\u012b', 'i')
         line = line.replace(u'\u012c', 'I')
         line = line.replace(u'\u012d', 'i')
         line = line.replace(u'\u012e', 'I')
         line = line.replace(u'\u012f', 'i')
         line = line.replace(u'\u0130', 'I')
         line = line.replace(u'\u0131', 'i')
         line = line.replace(u'\u0132', 'IJ')
         line = line.replace(u'\u0133', 'ij')
         line = line.replace(u'\u0134', 'J')
         line = line.replace(u'\u0135', 'j')
         line = line.replace(u'\u0136', 'K')
         line = line.replace(u'\u0137', 'k')
         line = line.replace(u'\u0138', 'k')
         line = line.replace(u'\u0139', 'L')
         line = line.replace(u'\u013a', 'l')
         line = line.replace(u'\u013b', 'L')
         line = line.replace(u'\u013c', 'l')
         line = line.replace(u'\u013d', 'L')
         line = line.replace(u'\u013e', 'l')
         line = line.replace(u'\u0140', 'l')
         line = line.replace(u'\u0141', 'L')
         line = line.replace(u'\u0142', 'l')
         line = line.replace(u'\u0143', 'N')
         line = line.replace(u'\u0144', 'n')
         line = line.replace(u'\u0145', 'N')
         line = line.replace(u'\u0146', 'n')
         line = line.replace(u'\u0147', 'N')
         line = line.replace(u'\u0148', 'n')
         line = line.replace(u'\u0149', 'n')
         line = line.replace(u'\u014a', 'N')
         line = line.replace(u'\u014b', 'n')
         line = line.replace(u'\u014c', 'O')
         line = line.replace(u'\u014d', 'o')
         line = line.replace(u'\u014e', 'O')
         line = line.replace(u'\u014f', 'o')
         line = line.replace(u'\u0150', 'O')
         line = line.replace(u'\u0151', 'o')
         line = line.replace(u'\u0152', 'OE')
         line = line.replace(u'\u0153', 'oe')
         line = line.replace(u'\u0154', 'R')
         line = line.replace(u'\u0155', 'r')
         line = line.replace(u'\u0156', 'R')
         line = line.replace(u'\u0157', 'r')
         line = line.replace(u'\u0158', 'R')
         line = line.replace(u'\u0159', 'r')
         line = line.replace(u'\u015a', 'S')
         line = line.replace(u'\u015b', 's')
         line = line.replace(u'\u015c', 'S')
         line = line.replace(u'\u015d', 's')
         line = line.replace(u'\u015e', 'S')
         line = line.replace(u'\u015f', 's')
         line = line.replace(u'\u0160', 'S')
         line = line.replace(u'\u0161', 's')
         line = line.replace(u'\u0162', 'T')
         line = line.replace(u'\u0163', 't')
         line = line.replace(u'\u0164', 'T')
         line = line.replace(u'\u0165', 't')
         line = line.replace(u'\u0166', 'T')
         line = line.replace(u'\u0167', 't')
         line = line.replace(u'\u0168', 'U')
         line = line.replace(u'\u0169', 'u')
         line = line.replace(u'\u016a', 'U')
         line = line.replace(u'\u016b', 'u')
         line = line.replace(u'\u016c', 'U')
         line = line.replace(u'\u016d', 'u')
         line = line.replace(u'\u016e', 'U')
         line = line.replace(u'\u016f', 'u')
         line = line.replace(u'\u0170', 'U')
         line = line.replace(u'\u0171', 'u')
         line = line.replace(u'\u0172', 'U')
         line = line.replace(u'\u0173', 'u')
         line = line.replace(u'\u0174', 'W')
         line = line.replace(u'\u0175', 'w')
         line = line.replace(u'\u0176', 'Y')
         line = line.replace(u'\u0177', 'y')
         line = line.replace(u'\u0178', 'Y')
         line = line.replace(u'\u0179', 'Z')
         line = line.replace(u'\u017a', 'z')
         line = line.replace(u'\u017b', 'Z')
         line = line.replace(u'\u017c', 'z')
         line = line.replace(u'\u017d', 'Z')
         line = line.replace(u'\u017e', 'z')
         line = line.replace(u'\u017f', 's')
         
         #Non English Latin characters (Latin-1 Supplement)
         line = line.replace(u'\u00fc', 'u')
         line = line.replace(u'\u00f6', 'o')
         line = line.replace(u'\u00e6', 'ae')
         line = line.replace(u'\u00c0', 'A')
         line = line.replace(u'\u00c1', 'A')
         line = line.replace(u'\u00c2', 'A')
         line = line.replace(u'\u00c3', 'A')
         line = line.replace(u'\u00c4', 'A')
         line = line.replace(u'\u00c5', 'A')
         line = line.replace(u'\u00c6', 'AE')
         line = line.replace(u'\u00c7', 'C')
         line = line.replace(u'\u00c8', 'E')
         line = line.replace(u'\u00c9', 'E')
         line = line.replace(u'\u00ca', 'E')
         line = line.replace(u'\u00cb', 'E')
         line = line.replace(u'\u00cc', 'I')
         line = line.replace(u'\u00cd', 'I')
         line = line.replace(u'\u00ce', 'I')
         line = line.replace(u'\u00cf', 'I')
         line = line.replace(u'\u00d0', 'D')
         line = line.replace(u'\u00d1', 'N')
         line = line.replace(u'\u00d2', 'O')
         line = line.replace(u'\u00d3', 'O')
         line = line.replace(u'\u00d4', 'O')
         line = line.replace(u'\u00d5', 'O')
         line = line.replace(u'\u00d6', 'O')
         line = line.replace(u'\u00d7', 'X')
         line = line.replace(u'\u00d8', 'O')
         line = line.replace(u'\u00d9', 'U')
         line = line.replace(u'\u00da', 'U')
         line = line.replace(u'\u00db', 'U')
         line = line.replace(u'\u00dc', 'U')
         line = line.replace(u'\u00dd', 'Y')
         line = line.replace(u'\u00de', '')
         line = line.replace(u'\u00df', 'B')
         line = line.replace(u'\u00e0', 'a')
         line = line.replace(u'\u00e1', 'a')
         line = line.replace(u'\u00e2', 'a')
         line = line.replace(u'\u00e3', 'a')
         line = line.replace(u'\u00e4', 'a')
         line = line.replace(u'\u00e5', 'a')
         line = line.replace(u'\u00e7', 'c')
         line = line.replace(u'\u00e8', 'e')
         line = line.replace(u'\u00e9', 'e')
         line = line.replace(u'\u00ea', 'e')
         line = line.replace(u'\u00eb', 'e')
         line = line.replace(u'\u00ec', 'i')
         line = line.replace(u'\u00ed', 'i')
         line = line.replace(u'\u00ee', 'i')
         line = line.replace(u'\u00ef', 'i')
         line = line.replace(u'\u00f0', 'o')
         line = line.replace(u'\u00f1', 'n')
         line = line.replace(u'\u00f2', 'o')
         line = line.replace(u'\u00f3', 'o')
         line = line.replace(u'\u00f4', 'o')
         line = line.replace(u'\u00f5', 'o')
         line = line.replace(u'\u00f8', 'o')
         line = line.replace(u'\u00f9', 'u')
         line = line.replace(u'\u00fa', 'u')
         line = line.replace(u'\u00fb', 'u')
         line = line.replace(u'\u00fd', 'y')
         line = line.replace(u'\u00fe', 'b')
         line = line.replace(u'\u00ff', 'y')
         line = line.replace(u'\u03f5', 'E')
         line = line.encode('ascii', 'ignore')
    except Exception as e:
        print e
    
    return line

def process_and_commit(fileCue,n):
    u01 = dict( driver = 'FreeTDS', database = 'db', server = 'ip', port = '1433', uid = 'username', password = 'password' )
    try:
        con = pyodbc.connect('DRIVER=%(driver)s;DATABASE=%(database)s;SERVER=%(server)s;PORT=%(port)s;UID=%(uid)s;PWD=%(password)s;CHARSET=UTF8;TDS_VERSION=8.0;'% u01 ,autocommit=True)
        cur = con.cursor()
        sqlTrialsInsert = """ SQL Insert""" 
        sqlInterventionsInsert = """ SQL Insert """ 
        while True:
            filr = fileCue.get()
            if isinstance(filr,EndOfQueue):
                fileCue.task_done()
            try:
                full_path =  filr
                soup = bs(codecs.open(full_path,'r'),'lxml')
                if soup.nct_id:
                    nctid= strip_utf8(soup.nct_id.text)
                    pid_1 = int(nctid[3:])
                else:
                    nctid= None
                if soup.required_header:
                    if soup.required_header.url:
                        url = strip_utf8(soup.required_header.url.text)
                    else:
                        url =None
                else:
                    url =None
                if soup.org_study_id:
                    org_study_id = strip_utf8(soup.org_study_id.text)
                else:
                    org_study_id = None
                if soup.brief_title:
                    brief_title = strip_utf8(soup.brief_title.text)
                else:
                    brief_title = None
                title_official = None
                if soup.sponsors:
                    if soup.sponsors.lead_sponsor:
                        if soup.sponsors.lead_sponsor.agency:
                            sponsor = strip_utf8(soup.sponsors.lead_sponsor.agency.text)
                        else:
                            sponsor = None
                    else:
                        sponsor = None
                else:
                   sponsor = None
                if soup.brief_summary:
                    brief_summary = strip_utf8(soup.brief_summary.text)
                else:
                    brief_summary =None
                if soup.detailed_description:
                    detailed_description = strip_utf8(soup.detailed_description.text)
                else:
                    detailed_description = None
                if soup.overall_status:
                    overall_status =strip_utf8( soup.overall_status.text)
                else:
                    overall_status = None
                if soup.firstreceived_date:
                    firstreceived_date = convert_string_to_date(soup.firstreceived_date.text)
                else:
                    firstreceived_date = None
                if soup.lastchanged_date:
                    lastchanged_date = convert_string_to_date(soup.lastchanged_date.text)
                else:
                    lastchanged_date =None
                if soup.study_type:
                    study_type = strip_utf8(soup.study_type.text)
                else:
                    study_type = None
                if soup.phase:
                    phase = strip_utf8(soup.phase.text)
                else:
                    phase = None
                if soup.study_design:
                    study_design = strip_utf8(soup.study_design.text)
                else:
                    study_design = None
                if soup.eligibility:
                    if soup.eligibility.criteria:
                        if soup.eligibility.criteria.textblock:
                            criteria = strip_utf8(soup.eligibility.criteria.textblock.text)
                        else:
                            criteria = None
                    else:
                        criteria = None
                else:
                    criteria = None
                if soup.gender:
                    gender = strip_utf8(soup.gender.text)
                else:
                    gender = None
                if soup.minimum_age:
                    minimum_age = strip_utf8(soup.minimum_age.text)
                else:
                    minimum_age = None
                if soup.maximum_age:
                    maximum_age = strip_utf8(soup.maximum_age.text)
                else:
                    maximum_age = None
                if soup.healthy_volunteers:
                    healthy_volunteers = strip_utf8(soup.healthy_volunteers.text)
                else:
                    healthy_volunteers = None
                if soup.facility:
                    if soup.facility.name:
                        facility_name = strip_utf8(soup.facility.name)
                    else:
                        facility_name = None
                    if soup.facility.city:
                        facility_city = strip_utf8(soup.facility.city.text)
                    else:
                        facility_city = None
                    if soup.facility.state:
                        facility_state = strip_utf8(soup.facility.state.text)
                    else:
                        facility_state = None
                    if soup.facility.country:
                        facility_country = strip_utf8(soup.facility.country.text)
                    else:
                        facility_country = None 
                else:
                    facility_name = None
                    facility_city = None
                    facility_state = None
                    facility_country = None
                trial_line = [
                  pid_1,nctid,url,org_study_id,brief_title,title_official,
                  sponsor,brief_summary,detailed_description,overall_status,firstreceived_date,lastchanged_date,
                  study_type,phase,study_design,criteria,gender,minimum_age,
                  maximum_age,healthy_volunteers,facility_name,facility_city,facility_state,facility_country
                 ]
                if soup.nct_id:
                    nctid2 = strip_utf8(soup.nct_id.text)
                else:
                    nctid2 = None
                if soup.intervention:
                    if  soup.intervention.intervention_type:
                        intervention_type = strip_utf8(soup.intervention.intervention_type.text)
                    else:
                        intervention_type = None
                    if  soup.intervention.intervention_name:
                        intervention_name = strip_utf8(soup.intervention.intervention_name.text)
                    else:
                        intervention_name = None
                if soup.phase:
                    phaze = strip_utf8(soup.phase.text)
                else:
                    phaze = None
                intervention_line = [pid_1,nctid,intervention_type,intervention_name,phaze] 
                #pid_1 += 1
                #content_list_1.append(trial_line)
                #content_list_1.append(intervention_line)
                #third_tup =()
                #if soup.detailed_description:
                    #item1 = soup.detailed_description.textblock.text
                    #item2 = strip_utf8(item1)
                    #third_tupe=(soup.nct_id.text,item2)
                    #write_out(third_tup[0],third_tup[1])
                    #fin = [trial_line,intervention_line,third_tupe]
                #content_list_1.append(fin)
                cur.execute(sqlTrialsInsert,trial_line)
                cur.execute(sqlInterventionsInsert,intervention_line)
                
            except:
                exc_type, exc_value = sys.exc_info()[:2]
                print "Problem in subroc %s:%s" % (exc_type, exc_value)
            fileCue.task_done()
    finally:
        cur.close()

def process_xml_files(folder,list_of_files):
    content_list_1 =[]
    #content_list_2 =[]
    #content_list_3 =[]
    
    pid_1 = 0
    for filr in list_of_files:
        full_path = folder + filr
        soup = bs(codecs.open(full_path,'r'),'lxml')
        if soup.nct_id:
            nctid= strip_utf8(soup.nct_id.text)
            pid_1 = int(nctid[3:])
        else:
            nctid= None
        if soup.required_header:
            if soup.required_header.url:
                url = strip_utf8(soup.required_header.url.text)
            else:
                url =None
        else:
            url =None
        if soup.org_study_id:
            org_study_id = strip_utf8(soup.org_study_id.text)
        else:
            org_study_id = None
        if soup.brief_title:
            brief_title = strip_utf8(soup.brief_title.text)
        else:
            brief_title = None
        title_official = None
        if soup.sponsors:
            if soup.sponsors.lead_sponsor:
                if soup.sponsors.lead_sponsor.agency:
                    sponsor = strip_utf8(soup.sponsors.lead_sponsor.agency.text)
                else:
                    sponsor = None
            else:
                sponsor = None
        else:
            sponsor = None
        if soup.brief_summary:
            brief_summary = strip_utf8(soup.brief_summary.text)
        else:
            brief_summary =None
        if soup.detailed_description:
            detailed_description = strip_utf8(soup.detailed_description.text)
        else:
            detailed_description = None
        if soup.overall_status:
            overall_status =strip_utf8( soup.overall_status.text)
        else:
            overall_status = None
        if soup.firstreceived_date:
            firstreceived_date = convert_string_to_date(soup.firstreceived_date.text)
        else:
            firstreceived_date = None
    
        if soup.lastchanged_date:
            lastchanged_date = convert_string_to_date(soup.lastchanged_date.text)
        else:
            lastchanged_date =None
        
        if soup.study_type:
            study_type = strip_utf8(soup.study_type.text)
        else:
            study_type = None
        
        if soup.phase:
            phase = strip_utf8(soup.phase.text)
        else:
            phase = None
        
        if soup.study_design:
            study_design = strip_utf8(soup.study_design.text)
        else:
            study_design = None
        
        if soup.eligibility:
            if soup.eligibility.criteria:
                if soup.eligibility.criteria.textblock:
                   criteria = strip_utf8(soup.eligibility.criteria.textblock.text)
                else:
                    criteria = None
            else:
                criteria = None
        else:
            criteria = None
        
        if soup.gender:
            gender = strip_utf8(soup.gender.text)
        else:
            gender = None
        
        if soup.minimum_age:
            minimum_age = strip_utf8(soup.minimum_age.text)
        else:
            minimum_age = None
       
        if soup.maximum_age:
            maximum_age = strip_utf8(soup.maximum_age.text)
        else:
            maximum_age = None
        
        if soup.healthy_volunteers:
            healthy_volunteers = strip_utf8(soup.healthy_volunteers.text)
        else:
            healthy_volunteers = None
        
        if soup.facility:
            if soup.facility.name:
                facility_name = strip_utf8(soup.facility.name)
            else:
                facility_name = None
            if soup.facility.city:
                facility_city = strip_utf8(soup.facility.city.text)
            else:
                facility_city = None
            if soup.facility.state:
                facility_state = strip_utf8(soup.facility.state.text)
            else:
                facility_state = None
            if soup.facility.country:
                facility_country = strip_utf8(soup.facility.country.text)
            else:
                facility_country = None 
        else:
            facility_name = None
            facility_city = None
            facility_state = None
            facility_country = None
    
        trial_line = [
                  pid_1,nctid,url,org_study_id,brief_title,title_official,
                  sponsor,brief_summary,detailed_description,overall_status,firstreceived_date,lastchanged_date,
                  study_type,phase,study_design,criteria,gender,minimum_age,
                  maximum_age,healthy_volunteers,facility_name,facility_city,facility_state,facility_country
                 ]
        if soup.nct_id:
            nctid2 = strip_utf8(soup.nct_id.text)
        else:
            nctid2 = None
        if soup.intervention:
           if  soup.intervention.intervention_type:
              intervention_type = strip_utf8(soup.intervention.intervention_type.text)
           else:
              intervention_type = None
           if  soup.intervention.intervention_name:
              intervention_name = strip_utf8(soup.intervention.intervention_name.text)
           else:
              intervention_name = None
        if soup.phase:
            phaze = strip_utf8(soup.phase.text)
        else:
            phaze = None
        
        intervention_line = [pid_1,nctid,intervention_type,intervention_name,phaze] 
        #pid_1 += 1
        #content_list_1.append(trial_line)
        #content_list_1.append(intervention_line)
        third_tup =()
        if soup.detailed_description:
            item1 = soup.detailed_description.textblock.text
            item2 = strip_utf8(item1)
            third_tupe=(soup.nct_id.text,item2)
        fin = [trial_line,intervention_line,third_tupe]
        content_list_1.append(fin)
    return content_list_1

def commit(fileCue,n):
    u01 = dict( driver = 'FreeTDS', database = 'db', server = 'ip', port = '1433', uid = 'username', password = 'password' )
    try:
        con = pyodbc.connect('DRIVER=%(driver)s;DATABASE=%(database)s;SERVER=%(server)s;PORT=%(port)s;UID=%(uid)s;PWD=%(password)s;CHARSET=UTF8;TDS_VERSION=8.0;'% u01 ,autocommit=True)
        cur = con.cursor()
        sqlTrialsInsert = """ SQL INSERT""" 
        sqlInterventionsInsert = """ SQL INSERT""" 
        while True:
            row = fileCue.get()
            if isinstance(row,EndOfQueue):
                fileCue.task_done()
            try:
                cur.execute(sqlTrialsInsert,row[0])
                cur.execute(sqlInterventionsInsert,row[1])
                write_out(row[2][0],row[2][1])
            except:
                exc_type, exc_value = sys.exc_info()[:2]
                print "Problem in subroc %s:%s" % (exc_type, exc_value)
            fileCue.task_done()
    finally:
        cur.close()


def call_process_and_commit(fileCue,n):
    intermediate_product = process_xml_files(fileCue)
    commit(intermediate_product[0],intermediate_product[1],intermediate_product[2])