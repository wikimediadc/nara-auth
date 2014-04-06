#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os, sys, pickle
import lxml.etree as etree

root_to_scan = sys.argv[1]
outputfile = sys.argv[2]
print(root_to_scan)
xmlfiles = []
masterlist = []

def xml_to_dict(xmlfile):
    result = {}
    with open(xmlfile, 'r') as f:
        tree = etree.parse(f)
        root = tree.getroot()
        for x in root.iter():
            result.update({x.tag : x.text})
    return result

def read_pickle(source):
    with open(source, 'r') as f:
        pickle.load(f)
        
def pickle_data(data, filename):
    pickle.dump(data, open(filename, "wb"))

def filterdata(source):
    pass

def build_file_list(dir):
    result = []
    filecount = 0
    for root, dirs, files in os.walk(dir):
        for f in files:
            if f.endswith(".xml"):
                fullpath = os.path.join(root, f)
                result.append(fullpath)
                filecount += 1
                print(fullpath)
            else:
                pass
    print(filecount)
    return result

def harvest():
    xmlfiles = build_file_list(root_to_scan)
    for xmlfile in xmlfiles:
        mydict = xml_to_dict(xmlfile)
        masterlist.append(mydict)
        print(mydict)
    pickle_data(masterlist, outputfile)
    print("FINISHED! Filecount = {0}".format(len(xmlfiles)))

if __name__ == "__main__":
    harvest()
