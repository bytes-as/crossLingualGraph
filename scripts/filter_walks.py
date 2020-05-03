import argparse

def parseArguments():
	parser = argparse.ArgumentParser(description='removes the walks with no words present in the dictionary provided')
	parser.add_argument('INPUT', help='file path for the walks input')
	parser.add_argument('DICT', help='file path  for the dictionary')
	parser.add_argument('--WALKS_DELIMITER', help='delimiter for the walks, defult is tabs', default='\t')
	parser.add_argument('--DICT_DELIMITER', help='delimter for the dictionary, default is tabs', default='\t')
	parser.add_argument('--POSITION', help='determine which side is to be used from the dictionary.\ndefault is 0 for source language\n1 for target language', type=int, default=0)
	parser.add_argument('OUTPUT', help='output file for the filtered walks')
	return parser.parse_args()

def readDictionary(args):
	dictionary = {}
	count = 0
	with open(args.DICT, 'r') as readFile:
		for line in readFile:
			count += 1
			if count % 1000 == 0:
				print('{} lines processed from dictionary'.format(count))
			tokens = line.rstrip().split(args.DICT_DELIMITER)
			if tokens[0] not in dictionary:
				dictionary[tokens[0]] = set()
			for token in tokens[1:]:
				dictionary[tokens[0]].add(token)
		print('Total number of entries read from dictionary', count)
	return dictionary

def readWalks(args):
	walks = []
	count = 0
	with open(args.INPUT, 'r') as readFile:
		for line in readFile:
			count += 1
			if count % 10000 == 0:
				print('{} walks read successfully', format(count))
			walks.append(line.rstrip().split(args.WALKS_DELIMITER))
	print('Total number of walk: {}'.format(count))
	return walks

def main(args):
	walks = readWalks(args)
	dictionary = readDictionary(args)
	if args.POSITION == 0:
		vocab = set(dictionary.keys())
	else:
		vocab = set()
		for token in dictionary:
			for translated in dictionary[token]:
				vocab.add(translated)
	writeFile = open(args.OUTPUT, 'w')
	count = 0
	for walk in walks:
		count += 1
		if count % 10000 == 0:
			print('{} walks have been processed'.format(count))
		valid = False
		for token in walk:
			if token in vocab:
				valid = True
				break
		if valid:
			writeFile.write(' '.join(walk) + '\n')
	writeFile.close()

if __name__=='__main__':
	main(parseArguments())
