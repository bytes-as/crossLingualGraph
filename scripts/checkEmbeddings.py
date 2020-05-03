import argparse
import os
import sys
from sklearn.metrics.pairwise import cosine_distances
from numpy.random import rand
from numpy import array
import seaborn as sns
from matplotlib import pyplot as plt
from time import time

def readEmbedding(file_path):
	start = time()
	readFile = open(file_path, 'r')
	header = next(readFile).rstrip()
	n, dim = map(int, header.split())
	print('total count : {}\ndimension: {}'.format(n, dim))
	embeddings = {}
	for line in readFile:
		tokens = line.rstrip().split()
		print(len(tokens))
		embeddings[tokens[0]] = list(map(float, tokens[1:]))
	end = time()
	print('Reading completed in time: {:.2f} minutes'.format((end-start)/60))
	return embeddings

def main(args):
	embeddings = readEmbedding(args.EMB)
	random_index = rand(args.COUNT, )*len(embeddings)
	keys = list(embeddings.keys())
	random_words = [keys[i] for i in range(len(random_index))]
	X = [embeddings[random_words[i]] for i in range(args.COUNT)]
	distance = cosine_distances(X)
	if args.OUTPUT is not None:
		writeFile = open(args.OUTPUT, 'w')
	for i in range(args.COUNT):
		for j in range(i+1, args.COUNT):
			# print(random_words[i],' ', random_words[j], ' ', distance[i, j])
			if args.OUTPUT is not None:
				writeFile.write(' '.join([random_words[i], random_words[j], str(distance[i, j]), '\n']))
	if args.PLOT is not None:
		fig, ax = plt.subplots(figsize=(10, 10))
		title = "cosine similarities"
		plt.title(title, fontsize=18)
		#ax.set_xticks([])
		#ax.set_yticks([])
		#ax.axis('off')
		
		
		labels = array([keys[i] for i in range(args.COUNT)])
		print('values : {}'.format(distance.shape))
		print('labels: {}'.format(labels.shape), labels)
		# sns.heatmap(array(distance), cmap='YlGnBu', linewidths=0.2, vmin=0, vmax=1, ax=ax)
		plt.yticks(rotation=0)
		sns.heatmap(array(distance), xticklabels=labels, yticklabels=labels , cmap='YlGnBu', square=True, linewidths=0.30, vmin=-1, vmax=1, ax=ax)
		# ax.set_yticks(labels)
		# ax.set_xticks(labels)
		plt.yticks(rotation=0)
		plt.xticks(rotation=90)
		plt.savefig(args.PLOT, dpi=300)
	
		


def parseArguments():
	parser = argparse.ArgumentParser(description='Take random number of embeddings and check the cosine similarity with others')
	parser.add_argument('EMB', help='Input emebeddings in the standard format where the first row is the number of words and dimension')
	parser.add_argument('--DICT', default=None, help='dictionary file to check the specific word embeddings')
	parser.add_argument('--COUNT', type=int, default=10, help='number of words to be considered to display')
	parser.add_argument('OUTPUT', default=None, help='output file to print the similarities in rsv file')
	parser.add_argument('--PLOT', default=None, help='to save the heat map with the cosine similarity')
	return parser.parse_args()

if __name__ == '__main__':
	args = parseArguments()
	main(args)
