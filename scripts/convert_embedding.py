import argparse
import os
import pickle

def parseArguments():
	parser = argparse.ArgumentParser(description='Convert the embedding file\'s keys according to the dictionray provided')
	parser.add_argument('INPUT', help='Embedding file to be converted')
	parser.add_argument('DICT', help='dictionary file to be used for conversion')
	parser.add_argument('--OVERWRITE', help='enabling overwrites over the embedding file', action='store_true', default=False)
	parser.add_argument('--OUTPUT', help='Seperate output file path', default=None)
	args = parser.parse_args()
	if not args.OVERWRITE and args.OUTPUT is None:
		raise Exception('If overwrite is not opted then the output argument is mandatory')
	if args.OVERWRITE:
		args.OUTPUT = args.INPUT
	return args

def readEmbeddings(path):
	embeddings = {}
	with open(path) as readFile:
		n, dim = list(map(int, next(readFile).rstrip().split()))
		for line in readFile:
			tokens = line.rstrip().split()
			try:
				tokens[0] = int(tokens[0])
			except:
				pass
			embeddings[tokens[0]] = list(map(float, tokens[1:]))
	return embeddings, n, dim


def main(args):
	print(args)
	with open(args.DICT, 'rb') as readFile:
		DICT = pickle.load(readFile)
	embeddings, n, dim = readEmbeddings(args.INPUT)
	print('[WRITE FILE]: {} opening...'.format(args.OUTPUT))
	with open(args.OUTPUT, 'w') as writeFile:
		writeFile.write(str(n) + ' ' + str(dim) + '\n')
		for word in embeddings:
			if word not in DICT:
				raise Exception('word not found in DICT file, please check it once')
			writeFile.write(DICT[word] + ' ' + ' '.join([str(em) for em in embeddings[word]]) + '\n')
	print('[WRITE]: Writing done in file: {}'.format(args.OUTPUT))
		
if __name__ == '__main__':
	main(parseArguments())
