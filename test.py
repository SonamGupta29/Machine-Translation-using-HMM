#!/usr/bin/python

from collections import defaultdict
import re
import pickle
import sys
import HTMLParser
import codecs
import time
import pickle
import operator
import math
import nltk
from math import log
from os import listdir
from os.path import isfile, join

# Module files
from Tokenizer import *
from inputMethod import *
from makeNGrams import *

reload(sys)

sys.setdefaultencoding("utf-8")

# Emission count "TAG -> WORD" for P(word / tag)
mappingsDict = dict()

def loadFromPickle():
	#Load wordCount Dict
	global mappingsDict
	with open('PickleFiles/mappings.pickle', 'rb') as f:
		mappingsDict = pickle.load(f)


def printData(present,length,inputTextTokens,inter):

	count = 0
	global mappingsDict
	if present == length-1:
		for eachWord in mappingsDict[inputTextTokens[present]][:3]:
			for e in inter:
				print e,
			print eachWord
		return
	else:
		for eachWord in mappingsDict[inputTextTokens[present]][:3]:
			inter.append(eachWord)
			printData(present+1,length,inputTextTokens,inter)
			inter.pop()

def translate(text):

	# Get the mapping dictionary
	global mappingsDict
	#print mappingsDict
	# Search the word in the dictionary and output the translation
	inputTextTokens = tokenize(text.lower(), ' ')

	# translatedText = list()
	# for token in inputTextTokens:
	# 	if token in mappingsDict:
	# 		translatedText.append(mappingsDict[token][0])

	# translatedStatement = ' '.join(translatedText)
	# translatedStatement = translatedStatement.decode("utf-8")
	# print translatedStatement
	inter = []
	printData(0,len(inputTextTokens),inputTextTokens,inter)






# Main Function
if __name__ == '__main__':
	
	# Load all the dictionaries from pickle files
	loadFromPickle()
	while True:
		# Get the input from the user
		inputText = raw_input("Enter the sentence : ")

		# Start the timer
		start = time.clock()

		translate(inputText)
		
	# Complete
	print "\n\nCompleted in ",time.clock() - start