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
		for word in [word1, word2]:
			if not word in word2int:
				word2int[word] = count
				int2word[count] = word
				count += 1
			if word not in frequency:
				# print('adding {}'.format(word))
				frequency[word] = 0
			frequency[word] += 1
		line_count += 1
		if line_count % 10000000 == 0:
			print("{} lines have been read from the input file".format(line_count))
	end = time()
	readFile.close()
	print('Total time for reading graph : {:.2f} minutes'.format((end - start)/60))
	writeFileModule(word2int, args.OUTPUT_DIR + '/word2int.' + args.LANGUAGE)
	writeFileModule(int2word, args.OUTPUT_DIR + '/int2word.' + args.LANGUAGE)
	writeFileModule(frequency, args.OUTPUT_DIR + '/frequency.' + args.LANGUAGE)

def parseArguments(manualArguments=None):
	parser = argparse.ArgumentParser(description='Preprocess english graph and remove weights and assigns the unique number')
	parser.add_argument('FILE_PATH', help='Input file path of the raw graph')
	parser.add_argument('LANGUAGE', help='Language for the names of the files to be written')
	parser.add_argument('--ROOT', help='Root directory for saving the file, defauit is None', default=None)
	parser.add_argument('--DELIMITER', help='DELIMITER for the file in edgelist, default is tabs', default='\t')
	parser.add_argument('--OUTPUT_DIR', default=None, help='Output file directory where all the files will be stored')
	if manualArguments is None:
		args = parser.parse_args()
	else:
		args = parser.parse_args(manualArguments)
	if args.ROOT is None:
		args.ROOT = '/'.join(args.FILE_PATH.split('/')[:-1])
	if args.OUTPUT_DIR is None:
		args.OUTPUT_DIR = args.ROOT
	return args

if __name__ == '__main__':
	# args = parseArguments(manualArguments=[
	# 	os.path.join(root, 'My Drive/Colab Notebooks/NodeEmbedding/graph.eng'),
	# 	'english',
	# 	'--MIN',
	# 	400])
	args = parseArguments()
	main(args)
