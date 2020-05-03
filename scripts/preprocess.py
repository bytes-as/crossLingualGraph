import argparse
import os
import sys
import pickle
from time import time

def writeFileModule(dict_object, file_name):
	start = time()
	with open(file_name, 'wb') as writeFile:
		pickle.dump(dict_object, writeFile)
	end = time()
	print('Writing file {} done in {:.2f} minutes'.format(file_name, (end-start)/60))

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
		for word in [word1, word2]:
			if not word in word2int:
				word2int[word] = count
				int2word[count] = word
				count += 1
			if word not in frequency:
				frequency[word] = 1
			else :
				frequency[word] += 1
		line_count += 1
		if line_count % 100000000 == 0:
			print("{} lines have been read from the input file".format(line_count))
	end = time()
	print('Total time for reading graph : {:.2f} minutes'.format((end - start)/60))
	writeFileModule(word2int, args.OUTPUT_DIR + '/word2int_' + str(max(0, args.MIN)) + '.' + args.LANGUAGE)
	writeFileModule(int2word, args.OUTPUT_DIR + '/int2word_' + str(max(0, args.MIN)) + '.' + args.LANGUAGE)
	writeFile = open(os.path.join(args.OUTPUT_DIR, args.OUTPUT_FILE), 'w')
	print('Starting writing...')
	start = time()
	if args.MIN > 0:
		print('FILTERING EDGES: based on the minimum word frequency of {}'.format(args.MIN))
		for line in lines:
			word1, word2, weight = line
			if frequency[word1] > args.MIN or frequency[word2] > args.MIN:
				if args.WEIGHTED:
					writeFile.write(str(word2int[word1]) + args.DELIMITER + str(word2int[word2]) + args.DELIMITER + weight + '\n')
				else:
					writeFile.write(str(word2int[word1]) + args.DELIMITER + str(word2int[word2]) + '\n')
	else:
		for line in lines:
			word1, word2, weight = line
			if args.WEIGHTED:
				writeFile.write(str(word2int[word1]) + args.DELIMITER + str(word2int[word2]) + args.DELIMITER + weight + '\n')
			else:
				writeFile.write(str(word2int[word1]) + args.DELIMITER + str(word2int[word2]) + '\n')
	end = time()
	print('Total time for writing graph: {} minutes'.format((end-start)/60))
	print('File Path: {}'.format(os.path.join(args.OUTPUT_DIR, args.OUTPUT_FILE)))
	readFile.close()
	writeFile.close()
	print('File closed')

def parseArguments(manualArguments=None):
	parser = argparse.ArgumentParser(description='Preprocess english graph and remove weights and assigns the unique number')
	parser.add_argument('FILE_PATH', help='Input file path of the raw graph')
	parser.add_argument('LANGUAGE', help='Language for the names of the files to be written')
	parser.add_argument('--ROOT', help='Root directory for saving the file, defauit is None', default=None)
	parser.add_argument('--DELIMITER', help='DELIMITER for the file in edgelist, default is tabs', default='\t')
	parser.add_argument('--OUTPUT_DIR', default=None, help='Output file directory where all the files will be stored')
	parser.add_argument('--OUTPUT_FILE', default='graph.unknown', help='output file name')
	parser.add_argument('--WEIGHTED', action='store_true', help='enable writing with weights')
	parser.add_argument('--MIN', default=-1, type=int, help='Minimum frequency for the filtering')
	if manualArguments is None:
		args = parser.parse_args()
	else:
		args = parser.parse_args(manualArguments)
	if args.ROOT is None:
		args.ROOT = '/'.join(args.FILE_PATH.split('/')[:-1])
	if args.OUTPUT_DIR is None:
		args.OUTPUT_DIR = args.ROOT
	if args.MIN >= 0:
		args.OUTPUT_FILE =  'graph_int_' + str(args.MIN) + \
			'.' + args.LANGUAGE
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
