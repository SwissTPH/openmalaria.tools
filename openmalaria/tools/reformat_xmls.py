#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the openmalaria.tools package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/openmalaria.tools
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This script is used to reformat the xml files if you're experiencing problems
with whitespaces. You will need to have PyXML installed.
Usage: ./reformat_xmls.py -p folder_path | file_path
"""

from xml.dom.minidom import parse, parseString
# xml.dom.ext comes from PyXML which is no longer maintained an not always available :-(
from xml.dom.ext import PrettyPrint
from os.path import exists
from os.path import isdir
from os.path import isfile
import os
import sys
import getopt

def write_to_file(doc, output_file_path):
    file_object = open(output_file_path, "w")
    PrettyPrint(doc, file_object)
    file_object.close()

def parse_and_write(input_file_path):
    basename, extension = input_file_path.split('.')
    if(extension == 'xml'):
        doc = parse(input_file_path)
        write_to_file(doc, input_file_path)


opts, extraparams = getopt.getopt(sys.argv[1:], 'p', 'path')

for o, p in opts:
    if o in ['-p', '--path']:
        path = extraparams[0]

if exists(path) :
    if isdir(path):
        dirList = os.listdir(path)
        for fname in dirList:
            parse_and_write(path + "/" + fname)
    elif isfile(path):
            parse_and_write(path)
else:
    print("Please enter a valid file or folder path...")
