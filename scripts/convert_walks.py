import argparse
import pickle

def parseArguments():
	parser = argparse.ArgumentParser(description='convert walks from int to char or vice versa')
	parser.add_argument('INPUT', help='file path for the walks input')
	parser.add_argument('DICT', help='dictionary file for conversion')
	parser.add_argument('--OUTPUT', default=None, help='output path to save the converted walks')
	parser.add_argument('--IN_DELIMITER', default='\t', help='delimiter for the input file\ndefault is tab')
	parser.add_argument('--OUT_DELIMITER', default='\t', help='delimiter for the output file\ndefault is tab')
	args = parser.parse_args()
	if args.OUTPUT is None:
		args.OUTPUT = args.INPUT
	return args

def loadConversionDict(path):
	with open(path, 'rb') as readFile:
		return pickle.load(readFile)

def main(args):
	walks = []
	count = 0
	print('Opening file: {}'.format(args.INPUT))
	with open(args.INPUT, 'r') as readFile:
		for line in readFile:
			count += 1
			if count % 1000000 == 0:
				print('{} run readed successfully'.format(count))
			tokens = line.rstrip().split(args.IN_DELIMITER)
			try:
				walks.append([int(token) for token in tokens])
			except:
				walks.append(tokens)
	total = count
	count = 0
	conversion_dict = loadConversionDict(args.DICT)
	with open(args.OUTPUT, 'w') as writeFile:
		for walk in walks:
			count += 1
			if count % 1000000 == 0:
				print('{}/{} line has written succesfully'.format(count, total))
			writeFile.write(args.OUT_DELIMITER.join([conversion_dict[word] for word in walk]) + '\n')
	print('File conversion succesfull\nNew file path: {}'.format(args.OUTPUT))

if __name__ == '__main__':
	main(parseArguments())
