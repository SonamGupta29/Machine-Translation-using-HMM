#!/usr/bin/python

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

# Will return the filename with the absolute path
def getListOfFilesInDir(dirName):	
	fileNameList = dict()
	engFileNameList = list()
	hinFileNameList = list()
	for f in listdir(dirName):
		fileName = dirName + '/' + f
		if isfile(fileName):
			if 'hin' in fileName:
				hinFileNameList.append(fileName)
			else:	
				engFileNameList.append(fileName)

	# Map the files like english to hindi
	engFileNameList.sort()
	hinFileNameList.sort()
	for i in range(len(engFileNameList)):
		fileNameList[engFileNameList[i]] = hinFileNameList[i]

	return fileNameList

def processData(fileMap):

	# Create a dictionary which will store the mapping like {is : {hai :1, aahe : 2}}
	mappings = dict()
	for key, value in fileMap.iteritems():
		engFileName = key
		hinFileName = value
		print "[INFO] Parsing ", engFileName, "and", hinFileName

		hindiFileData = openFileNRead(hinFileName).strip('\n').split('\n')
		englishFileData = openFileNRead(engFileName).lower().strip('\n').split('\n')

		totalSentences = len(hindiFileData)

		# leave the header, and just consider the statement
		for i in range(1, totalSentences, 1):
			engSentence = englishFileData[i].split('\t')[1]
			hinSentence = hindiFileData[i].split('\t')[1]
			# print engSentence, hinSentence

			# Currently we won't use the tag, just use word
			engtokens = tokenize(engSentence.strip(), ' ')
			hintokens = tokenize(hinSentence.strip(), ' ')
			for engtoken in engtokens:
				if engtoken.count('\\') == 1:
					eword, etag = engtoken.split('\\')
				# Coz the word may be like //jj
				if engtoken.count('\\') == 2:
					eword, eword1, etag = engtoken.split('\\')
					eword = '\\'
				eword = eword.lower()
				if eword not in mappings:
					mappings[eword] = dict()

				for hintoken in hintokens:
					if hintoken.count('\\') == 1:
						hword, htag = hintoken.split('\\')
					# Coz the word may be like //jj
					if hintoken.count('\\') == 2:
						hword, hword1, htag = hintoken.split('\\')
						hword = '\\'
					# No concept of lower in hindi, :D
					# word = word.lower()
					if hword not in u'\u0964':
						if hword in mappings[eword]:
							mappings[eword][hword] = mappings[eword][hword] + 1
						else:
							mappings[eword][hword] =  1

	# For every english word just store the top 10 words, like champion list
	mappingsDict = dict()
	for key, value in mappings.iteritems():
		engWord = key		
		sorted_x = sorted(value.items(), key = operator.itemgetter(1), reverse = True)
		if len(sorted_x) > 10:
			sorted_x = sorted_x[:10]
		# Get just the hindi word, now we don't need the frequency
		sorted_x = [i[0] for i in sorted_x]
		mappingsDict[engWord] = sorted_x

	return mappingsDict


def saveToPickle(tostore):
	with open('PickleFiles/mappings.pickle', 'wb') as f:
		pickle.dump(tostore, f)


def init():

	'''	
		# Get the input from the user
		fileName = raw_input("Enter the file name : ")
	'''

	# To get the count of each file and of each grams
	countOfGrams = {}

	# Iterate though the directory
	fileList = ["Corpus/" + f for f in listdir('Corpus') if isfile(join('Corpus', f))]

	for fileName in fileList:

		# Try to open the file and read the file in the UTF-8 format
		fileData = openFileNRead(fileName)

		# Tokenize the data, in return will get the list
		tokens = tokenize(fileData)

		# Parse the data and make the unigrams,...
		# Returns a list of dictionaries starting from unigrams...
		gramdict =  getNGrams(6, tokens, 1)

		# Insert an empty dictionary in countOfGrams
		countOfGrams[fileName.split('/')[1]] = {}

		for i in range(6):

			outputPkl = open("PickleFiles/" + fileName.split('/')[1] + '_' + str(i) + '.pkl', 'wb' )
			pickle.dump(gramdict[i], outputPkl)
			outputPkl.close()
			countOfGrams[fileName.split('/')[1]][i] = getCountOfNGrams(i)

		fileNameList.append(fileName.split('/')[1])


	# Load the count of the grams of each file into the pickle
	outputPkl = open('PickleFiles/countOfGrams.pkl', 'wb')
	pickle.dump(countOfGrams, outputPkl)
	outputPkl.close()

	#Write the fileNames to the file 
	fileHandle = open("fileNames", "w")
	fileHandle.write('\n'.join(fileNameList))
	fileHandle.close()



# Main Function
if __name__ == '__main__':

	# Start the timer
	start = time.clock()

	# Get the directory name
	dirName = ""
	
	try:
		dirName = sys.argv[1]
	except Exception, e:
		dirName = raw_input("Enter the directory : ")

	fileMap = getListOfFilesInDir(dirName)
	
	mappingsDict = processData(fileMap)

	# Store the mappings in the pickle
	saveToPickle(mappingsDict)

	print "\n\nCompleted in ",time.clock() - start