import argparse
import os
import sys
import pickle
from time import time

def readFileModule(file_path):
	with open(file_path, 'rb') as readFile:
		return pickle.load(readFile)

def main(args):
	lines = []
	word2int = {}
	int2word = {}
	frequency = {}
	count = 0
	line_count = 0
	readFile = open(args.FILE_PATH, 'r')
	start = time()
	print('Reading Graph...')
	for line in readFile:
		if args.LANGUAGE[0] == 'E' or args.LANGUAGE[0] == 'e':
			word1 = line.split('\n')[0].split('\t')[0].split('/')[0]
			word2 = line.split('\n')[0].split('\t')[1].split('/')[1]
			weight = line.split('\n')[0].split('\t')[-1]
		else:
			(word1, word2, weight) = line.split('\n')[0].split(args.DELIMITER)
		lines.append([word1, word2, weight])
		line_count += 1
		if line_count % 10000000 == 0:
			print("{} lines have been read from the input file".format(line_count))
	end = time()
	total_count = line_count
	print('Total time for reading graph : {:.2f} minutes'.format((end - start)/60))
	word2int = readFileModule(args.CONVERTER)
	if args.MIN > 0: frequency = readFileModule(args.FREQ)
	writeFile = open(args.OUTPUT_FILE, 'w')
	print('Starting writing...')
	start = time()
	line_count = 0
	if args.MIN > 0:
		print('FILTERING EDGES: based on the minimum word frequency of {}'.format(args.MIN))
		for line in lines:
			word1, word2, weight = line
			if frequency[word1] >= args.MIN or frequency[word2] > args.MIN:
				if args.WEIGHTED:
					writeFile.write(str(word2int[word1]) + args.DELIMITER + str(word2int[word2]) + args.DELIMITER + weight + '\n')
				else:
					writeFile.write(str(word2int[word1]) + args.DELIMITER + str(word2int[word2]) + '\n')
				line_count += 1
	else:
		for line in lines:
			word1, word2, weight = line
			if args.WEIGHTED:
				writeFile.write(str(word2int[word1]) + args.DELIMITER + str(word2int[word2]) + args.DELIMITER + weight + '\n')
			else:
				writeFile.write(str(word2int[word1]) + args.DELIMITER + str(word2int[word2]) + '\n')
			line_count += 1
	end = time()
	print('Total time for writing graph: {} minutes'.format((end-start)/60))
	print('Total line written: {}/{}'.format(line_count, total_count))
	print('File Path: {}'.format(args.OUTPUT_FILE))
	readFile.close()
	writeFile.close()
	print('File closed')

def parseArguments(manualArguments=None):
	parser = argparse.ArgumentParser(description='Preprocess english graph and remove weights and assigns the unique number')
	parser.add_argument('FILE_PATH', help='Input file path of the raw graph')
	parser.add_argument('LANGUAGE', help='Language for the names of the files to be written')
	parser.add_argument('CONVERTER', help='dict pickle file for conversion from char to int')
	parser.add_argument('--DELIMITER', help='DELIMITER for the file in edgelist, default is tabs', default='\t')
	parser.add_argument('--OUTPUT_FILE', default=None, help='output file name')
	parser.add_argument('--WEIGHTED', action='store_true', help='enable writing with weights')
	parser.add_argument('--MIN', default=0, type=int, help='Minimum frequency for the filtering')
	parser.add_argument('--FREQ', default=None, help='frequency file path for the tokens')
	if manualArguments is None:
		args = parser.parse_args()
	else:
		args = parser.parse_args(manualArguments)
	if args.MIN >= 0:
		if args.MIN != 0 and args.FREQ is None:
			raise Exception('minimum frequency is greater than 0 and so conversion dict is mandatory')
		if args.OUTPUT_FILE is None:
			args.OUTPUT_FILE =  'graph_int_' + str(args.MIN) + '.' + args.LANGUAGE
	else: args.OUTPUT_FILE = 'graph_int.' + args.LANGUAGE
	return args

if __name__ == '__main__':
	# args = parseArguments(manualArguments=[
	# 	os.path.join(root, 'My Drive/Colab Notebooks/NodeEmbedding/graph.eng'),
	# 	'english',
	# 	'--MIN',
	# 	400])
	args = parseArguments()
	main(args)
