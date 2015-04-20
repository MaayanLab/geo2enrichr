import urllib 
import urllib2  
import urlparse 
import xml.etree.ElementTree as ET
Filetoxins = open('ToxinsFound.txt','w')
Invalidtoxins = open('InvalidToxins.txt','w')
# Open a file
fo = open("toxins.txt", "r")
print "Name of the file: ", fo.name

for search_gene  in fo:
     print "Line No- %s" % ( search_gene)
     url ='https://urldefense.proofpoint.com/v2/url?u=http-3A__eutils.ncbi.nlm.nih.gov_entrez_eutils_esearch.fcgi&d=AAIGAQ&c=4R1YgkJNMyVWjMjneTwN5tJRn8m8VqTSNCjYLg1wNX4&r=XUOXQUh8ddpXKMy21RBIjALrSONejOO3CM-iMv-sXy8&m=ZncPDfghB2vR_RUFl7f4OPPpqzH89Psst4tTUCFBi0g&s=zbUO23c4dF_HxMmg-ODkjIgcStlNW5ne6dFXhZUq1SM&e= '
     query_args = {'db' : 'gds', 'term' : search_gene}
     data  = urllib.urlencode(query_args) 
     req =urllib2.Request(url,data)
     response = urllib2.urlopen(req)
     the_page = response.read()
     saveFile = open('xmlresult.xml','w')
     saveFile.write((the_page))
     saveFile.close()

          
     tree = ET.parse('xmlresult.xml')
     
     #Create an iterator
     iter = tree.getroot()

      #Iterate
     for element in iter:
        print "processing toxin " ,search_gene
        #First the element tag name
        count = element.tag
        if count == 'Count':
            print "got count" , count
        print "Element:", element.tag
        #Next the attributes (available on the instance itself using
        #the Python dictionary protocol
        if element.keys():
            print "\tAttributes:"
            for name, value in element.items():
                print "\t\tName: '%s', Value: '%s'"%(name, value)
            
        #Next the child elements and text
        print "\tChildren:"
        #Text that precedes all child elements (may be None)
        if element.text:
           text = element.text
           text = len(text) > 40 and text[:40] + "..." or text
           print "\t\tText:", repr(text)
           if count ==  'Count':
                 print "I am here and the value is ",text
           if count =='Count':
               if text == '0'   :
                   print "not valid toxin"
                   Invalidtoxins.write(search_gene)
           if count == 'Count': 
              if text > '0' :
                  print('found the toxin')
                  Filetoxins.write(search_gene)
        
        if element.getchildren():
           #Can also use: "for child in element.getchildren():"
            for child in element:
                #Child element tag name
               #print "\t\tElement", child.tag
                 #The "tail" on each child element consists of the text
                  #that comes after it in the parent element content, but
                  #before its next sibling.
                if child.tail:
                    text = child.tail
                    text = len(text) > 40 and text[:40] + "..." or text
                   # print "\t\tText:", repr(text)  
        
     
# Close opend file
fo.close() 
Filetoxins.close()
Invalidtoxins.close()