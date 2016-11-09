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
from math import log
from os import listdir
from os.path import isfile, join


# Module files
from Tokenizer import *
from inputMethod import *
from makeNGrams import *
from graphPlotModule import *
from classifier import *

# Global variable to store the fileNames
fileNameList = []

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



# Plot the graph from each grams
def getGramsNPlotGraph():

	inputPkl = open('PickleFiles/countOfGrams.pkl', 'rb')
	countGramDict = pickle.load(inputPkl)
	inputPkl.close()
	
	fileNameList = openFileNRead("fileNames").split('\n');

	for i in range(6):

		for fileName in fileNameList:

			# read python dict back from the file
			inputPkl = open('PickleFiles' + '/' + fileName + '_' + str(i) + '.pkl', 'rb')
			fileGramDict = pickle.load(inputPkl)
			
			sortedFileGramDictValues = list(fileGramDict.values())
			sortedFileGramDictValues.sort(reverse = True)			
			rank = [math.log(y + 1, 2) for y in range(len(sortedFileGramDictValues))]

			# With smoothing see the division
			frequency = [math.log(value, 2) / float(countGramDict[fileName][i]) for value in  sortedFileGramDictValues]
			
			# Without smoothing - Currently commeneted out, as different author we need to smooth the frequenct so consider the probabilities
			#frequency = [math.log(value, 2) for value in  sortedFileGramDictValues]

			plotGraph(rank, frequency, 'Frequecy', 'Rank', 'Rank vs Frequecy (' + str(i + 1) + '- Grams )')
						
			inputPkl.close()

		#Show the graph
		showGraph()



# Main Function
if __name__ == '__main__':

	# Start the timer
	start = time.clock()
	
	# Process the text and form the pickle files ONLY ONE TIME PROCESS
	#init()

	# Plot the graph for the all the files and for all the grams
	#getGramsNPlotGraph()

	# For checking the text to which author it belongs also just check for the 
	# Take the input from the file 

	fileName = raw_input("Enter the filename : ")
	text = openFileNRead(fileName)

	# Classify the text 	
	classify(text)
	
	print "\n\nCompleted in ",time.clock() - start