#!/usr/bin/python

import re
import pickle
import sys
import HTMLParser
import codecs
import time
import operator

#handling of the unwanted unicodes
chars = {
    '\xc2\x82' : ',',        # High code comma
    '\xc2\x84' : ',,',       # High code double comma
    '\xc2\x85' : '...',      # Tripple dot
    '\xc2\x88' : '^',        # High carat
    '\xc2\x91' : '\x27',     # Forward single quote
    '\xc2\x92' : '\x27',     # Reverse single quote
    '\xc2\x93' : '\x22',     # Forward double quote    
    '\xc2\x94' : '\x22',     # Reverse double quote
    '\xc2\x95' : ' ',
    '\xc2\x96' : '-',        # High hyphen
    '\xc2\x97' : '--',       # Double hyphen
    '\xc2\x99' : ' ',
    '\xc2\xa0' : ' ',
    '\xc2\xa6' : '|',        # Split vertical bar
    '\xc2\xab' : '<<',       # Double less than
    '\xc2\xbb' : '>>',       # Double greater than
    '\xc2\xbc' : '1/4',      # one quarter
    '\xc2\xbd' : '1/2',      # one half
    '\xc2\xbe' : '3/4',      # three quarters
    '\xca\xbf' : '\x27',     # c-single quote
    '\xcc\xa8' : '',         # modifier - under curve
    '\xcc\xb1' : '',          # modifier - under line
    '\xc3\x80' : 'A',
    '\xc3\x81' : 'A',
    '\xc3\x82' : 'A',
    '\xc3\x83' : 'A',
    '\xc3\x84' : 'A',
    '\xc3\x85' : 'A',
    '\xc3\x86' : 'AE',
    '\xc3\x87' : 'C',
    '\xc3\x88' : 'E',
    '\xc3\x89' : 'E',
    '\xc3\x8a' : 'E',
    '\xc3\x8b' : 'E',
    '\xc3\x8c' : 'I',
    '\xc3\x8d' : 'I',
    '\xc3\x8e' : 'I',
    '\xc3\x8f' : 'I',
    '\xc3\x90' : 'D',
    '\xc3\x91' : 'N',
    '\xc3\x92' : 'O',
    '\xc3\x93' : 'O',
    '\xc3\x94' : 'O',
    '\xc3\x95' : 'O',
    '\xc3\x96' : 'O',
    '\xc3\x97' : 'x',
    '\xc3\x99' : 'U',
    '\xc3\x9a' : 'U',
    '\xc3\x9b' : 'U',
    '\xc3\x9c' : 'U',
    '\xc3\x9d' : 'Y',
    '\xc3\xa0' : 'a',
    '\xc3\xa1' : 'a',
    '\xc3\xa2' : 'a',
    '\xc3\xa3' : 'a',
    '\xc3\xa4' : 'a',
    '\xc3\xa5' : 'a',
    '\xc3\xa6' : 'ae',
    '\xc3\xa7' : 'c',
    '\xc3\xa8' : 'e',
    '\xc3\xa9' : 'e',
    '\xc3\xaa' : 'e',
    '\xc3\xab' : 'e',
    '\xc3\xac' : 'i',
    '\xc3\xad' : 'i',
    '\xc3\xae' : 'i',
    '\xc3\xaf' : 'i',
    '\xc3\xb1' : 'n',
    '\xc3\xb2' : 'o',
    '\xc3\xb3' : 'o',
    '\xc3\xb4' : 'o',
    '\xc3\xb5' : 'o',
    '\xc3\xb6' : 'o',
    '\xc3\xb9' : 'u',
    '\xc3\xba' : 'u',
    '\xc3\xbb' : 'u',
    '\xc3\xbc' : 'u',
    '\xe2\x80\x9c' : '"',
    '\xe2\x80\x9d' : '"',
    '\xe2\x80\x99' : "'",
    '\xe2\x80\x94' : "-",
    '\xe2\x80\x98' : "'"
}



#function for handling the unicodes
def replace_chars(match):
    char = match.group(0)
    return chars[char]


#Open and read the file in the UTF-8 format and return the data
def openFileNRead(fileName):
    #rading data from the file
    try:
        with codecs.open(fileName, "r", "utf-8", errors = 'ignore') as fdata:
            data = fdata.read()
            data = data.encode("utf-8",errors='ignore') 
            data = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, data) #remove the buggy encodings.. see the big list :P
            data = data.replace("\0x93",'"')
            data = data.replace("\0x94",'"')
            data = data.decode("utf-8")
        fdata.close()
    except Exception, e:
        print "Unable to open file...[", fileName, "]"
        exit(0)

    return data
