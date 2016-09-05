from bs4 import BeautifulSoup as bs
import codecs
import sys
import zipfile
import os
from multiprocessing import Process, JoinableQueue
import datetime
import pyodbc
from clinical_trials_functions import *




if __name__ == '__main__':
    folder = unzip_files()
    #os.chdir(folder)
    list_of_xml_files = os.listdir(folder)
    cue_size = len(list_of_xml_files)
    #print 'Processing Files...'
    #processed_list = process_xml_files(folder,list_of_xml_files)
    #print 'Finished processing all %s files' % len(list_of_xml_files)
    PROC_WORKERS = 5
    print "Starting workers"
    fileCue = JoinableQueue(cue_size)
    print "%s files to be processed" % cue_size
    procWorkers = []
    for n in range(PROC_WORKERS):
        procWorkers.append(Process(target = process_and_commit, args=(fileCue,n)))
        procWorkers[-1].start()
    print 'Starting cue creation...'
    
    for filr in list_of_xml_files:
        new_filr = folder + filr
        fileCue.put(new_filr)
    
    print 'Cue creation complete'
    
    print "Assigning end of shift"
    for n in range(PROC_WORKERS):
        fileCue.put(EndOfQueue())
    
        print "Processing file queue"
        fileCue.join()
        print "Joined file queue"
       
        print "Waiting for processor workers"
        for procWorker in procWorkers:
                procWorker.join()
                print "Joined a processor worker"