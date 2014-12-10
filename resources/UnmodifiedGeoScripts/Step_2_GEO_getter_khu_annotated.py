'''
    Library for getting and processing GDS SOFT Files from GEO
    GDS Files have a particular structure for the construction of their gzipped files.
    This script will take a GDS as input and return the samples (GSMs) and their experimental conditions with it
'''

import gzip
import urllib2
import StringIO
import re
from collections import defaultdict as ddict
import json
import sys

def __constructURL(dataset_identifier):
    '''
        Example URL:
            ftp://ftp.ncbi.nlm.nih.gov/geo/datasets/GDS4nnn/GDS4999/soft/GDS4999.soft.gz
    '''

    number_digits = len(dataset_identifier) - 3;    ## "GDS" is of length 3

    if number_digits > 3:
        folder = dataset_identifier[:4] + "nnn"
    else:
        folder = dataset_identifier[:3] + "n" * number_digits

    url = '/'.join(["ftp://ftp.ncbi.nlm.nih.gov/geo/datasets", 
                                       folder,
                                       dataset_identifier,
                                       "soft",
                                       dataset_identifier + ".soft.gz"])
    print 'URL constructed'

    #print url
    return url

def __constructGSEURL(dataset_identifier, platform):
    '''
        Example URL:
            ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/GSE4nnn/GSE4999/matrix/GSE4999.txt.gz
    '''

    number_digits = len(dataset_identifier) - 3;    ## "GSE" is of length 3

    if number_digits < 4:
        folder = dataset_identifier[:3] + "nnn" #GSEnnn
    elif 3 < number_digits < 5:
        folder = dataset_identifier[:4] + "nnn" #GSE1nnn
    else:
        folder = dataset_identifier[:5] + "nnn" #GSE39nnn

##    baseurl = '/'.join(["ftp://ftp.ncbi.nlm.nih.gov/geo/series", 
##                                       folder,
##                                       dataset_identifier,
##                                       "matrix"])
##
##    file_like_object = urllib2.urlopen(baseurl)
##    source_page = file_like_object.read()
##    file_like_object.close()
##
##    source_page_list = source_page.split('\r\n')
##    if source_page_list[1]:
##        series_matrix_identifier = '{0}-{1}'.format(dataset_identifier, platform)
##    else:
##        series_matrix_identifier = dataset_identifier


    url = '/'.join(["ftp://ftp.ncbi.nlm.nih.gov/geo/series", 
                                       folder,
                                       dataset_identifier,
                                       "matrix",
                                       dataset_identifier + "_series_matrix.txt.gz"])

    print 'GSE URL constructed'

    #print url
    return url

def __constructGPLURL(dataset_identifier):
    '''
        Example URL:
            ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL4nnn/GDS4999/annot/GPL4999.annot.gz
    '''

    number_digits = len(dataset_identifier) - 3;    ## "GPL" is of length 3

    if number_digits < 4:
        folder = dataset_identifier[:3] + "nnn"
    elif 3 < number_digits < 5 :
        folder = dataset_identifier[:4] + "nnn"
    else:
        folder = dataset_identifier[:5] + "nnn"

    url = '/'.join(["ftp://ftp.ncbi.nlm.nih.gov/geo/platforms", 
                                       folder,
                                       dataset_identifier,
                                       "annot",
                                       dataset_identifier + ".annot.gz"])

    #print url
    return url

def __unzip(compressedString):
    #Unzips the file without allowing it to touch the disk

    f = StringIO.StringIO(compressedString)
    decompressed = gzip.GzipFile(fileobj=f)
    print 'Unzipping file'
    return decompressed.read()


def __getFile(dataset_identifier, attempts = 5):
    #Attempts to get the file from URL. 
    #Tries five times before giving up.

    url = __constructURL(dataset_identifier)

    while attempts > 0:
        try:
            response = urllib2.urlopen(url)
            'Print attempting to get file'
        except urllib2.URLError:
            print url #So we know what did not exist
            sys.exit("Error: URL does not exist.")
        
        if response.getcode() < 201:
                break
        else:
                attempts -= 1
    else:
            return None

    return response.read()

def __getGSEFile(dataset_identifier, platform, attempts = 5):
    #Attempts to get the file from URL. 
    #Tries five times before giving up.
    print 'Stop spying on me 1'
    url = __constructGSEURL(dataset_identifier, platform)
    print 'Revolution for Freedom'
    while attempts > 0:
        try:
            response = urllib2.urlopen(url)
            print 'attempting to get file'
        except urllib2.URLError:
            print url #So we know what did not exist
            sys.exit("Error: URL does not exist.")        
        
        if response.getcode() < 201:
                break
        else:
                attempts -= 1
    else:
            return None

    return response.read()

def __getGPLFile(dataset_identifier, attempts = 5):
    #Attempts to get the file from URL. 
    #Tries five times before giving up.

    url = __constructGPLURL(dataset_identifier)

    while attempts > 0:
        try:
            response = urllib2.urlopen(url)
        except urllib2.URLError:
            print url #So we know what did not exist
            sys.exit("Error: URL does not exist.")          
        
        if response.getcode() < 201:
                break
        else:
                attempts -= 1
    else:
            return None

    return response.read()

def __findSubsets(description):
    #Gets the subset information from the SOFT File header.

    #Separates header by subset.
    splits = re.split("\^SUBSET =.*?(?=\n)", description, flags=re.DOTALL)
    subsets = splits[1:]    #Ignores 0 which will contain no subset.

    #Creates the patterns for regex.

    pattern_samples = re.compile("(?<=!subset_sample_id = ).*?(?=\n)")
    pattern_type = re.compile("(?<=\!subset_type = ).*?(?=\n)")
    pattern_description = re.compile("(?<=\!subset_description = ).*?(?=\n)")

    subinfo = []
    for x in subsets:
        samples = pattern_samples.search(x).group(0).split(',')
        subset_type = pattern_type.search(x).group(0)
        subset_description = pattern_description.search(x).group(0)

        subinfo.append([samples, subset_type, subset_description])
        
    return subinfo


def __separateDescriptionFromTable(string):
    splits = re.split("!dataset_table_begin\n", string)
    description = splits[0]
    table = re.search(".*(?=\n\!dataset_table_end)", splits[1], flags=re.DOTALL)
    return description, table.group(0)


def __processTable(string):
    #Creates a dictionary of key: id_ref with value: (gene name and value).
    table = [line.split('\t') for line in string.split('\n')]

    identifiers = table[0][2:]  #Soft Tables start with
                                #"ID_Ref" | "Identifier" | Identifiers... 
    idDict = ddict(list)
    for elements in table[1:]:
        id_ref = elements[0]
        genename = elements[1]
        
        for i, element in enumerate(elements[2:]):
            ident = identifiers[i]
            idDict[ident].append([genename, float(element)])

    return idDict

def getSOFTFile(dataset_identifier, list_folder, descriptor=''): #descriptor (see variable annotation_info in processor) is an optional user-supplied argument that can be any descriptor for the SOFT file.
    
    bin_string = __getFile(dataset_identifier)
    if bin_string is None:
        return "Error: File does not exist."
    try:
        string = __unzip(bin_string)
    except IOError:
        return "Error: Cannot get file from GEO. Please try again later."
    #Write a SOFT file
    with open(list_folder + descriptor +'_'+ dataset_identifier + '.soft', 'w') as f:
        f.write(string)

    return "Done"
    #description, table = __separateDescriptionFromTable(string)
    #subsets = __findSubsets(description)
    ##print(subsets)

def getSeriesMatrixFile(dataset_identifier, platform, list_folder, annotation_info=''):
    print 'Freedom'
    bin_string = __getGSEFile(dataset_identifier, platform)
    print 'Freedom1'
    if bin_string is None:
        return "Error: File does not exist."
    try:
        string = __unzip(bin_string)
        print 'Unzipping Freedom'
    except IOError:
        return "Error: Cannot get file from GEO. Please try again later."
    #Write a txt_series_matrix file
    print 'Writing Freedom'
    with open(list_folder + annotation_info +'_'+ dataset_identifier + '.txt', 'w') as f:
        f.write(string)
    print 'Wrote Freedom'

    #description, table = __separateDescriptionFromTable(string)
    #subsets = __findSubsets(description)
    ##print(subsets)

def getGPLannot(GPL_identifier, list_folder, descriptor=''):

    bin_string = __getGPLFile(GPL_identifier)
    if bin_string is None:
        return "Error: File does not exist."
    try:
        string = __unzip(bin_string)
    except IOError:
        return "Error: Cannot get file from GEO. Please try again later."
    #Write a SOFT file
    with open(list_folder + descriptor +'_'+ dataset_identifier + '.soft', 'w') as f:
        f.write(string)

    #description, table = __separateDescriptionFromTable(string)
    #subsets = __findSubsets(description)
    ##print(subsets)

def toJSON(subsets, dataset_identifier):
    with open(dataset_identifier + ".json", "w") as file:
        json.dump(subsets, file)
