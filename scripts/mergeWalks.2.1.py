import argparse
import pickle

def argumentParser():
	parser = argparse.ArgumentParser(description='merge the runs using the dictionaries given as input')
	parser.add_argument('WALKS1', help='input for walks language 1')
	parser.add_argument('WALKS2', help='input for walks language 2')
	parser.add_argument('DICT', help='input for dictionary from language 1 to language 2')
	parser.add_argument('--DELIMITER1', help='delimiter for walk 1, default is tab', default='\t')
	parser.add_argument('--DELIMITER2', help='delimiter for walk 2, default is tab', default='\t')
	parser.add_argument('--DICT_DELIMITER', help='delimiter for dict, default is tab', default='\t')
	parser.add_argument('OUTPUT', help='output file for merged walks')
	return parser.parse_args()

def readDict(args):
	dictionary = {}
	count = 0
	with open(args.DICT, 'r') as readFile:
		for line in readFile:
			count += 1
			if count % 10000 == 0:
				print('{} entries readed'.format(count))
			tokens = line.rstrip().split(args.DICT_DELIMITER)
			if tokens[0] not in dictionary:
				dictionary[tokens[0]] = set()
			for word in tokens[1:]:
				dictionary[tokens[0]].add(word)
			# dictionary[tokens[0]] = tokens[1:]
	print('Total entries readed from the dictionary: {}'.format(count))
	return dictionary

def readWalks(path, delim, count_only=False, inverse=False):
	walks = []
	inverse_index = {} if inverse else None
	count = 0
	with open(path, 'r') as readFile:
		for line in readFile:
			count += 1
			if count_only: continue
			if count % 100000 == 0:
				print('{} lines readed from the file {}'.format(count, path))
			rline = line.strip()
			tokens = rline.split(delim)
			walks.append(tokens)
			if inverse:
				for word in tokens:
					if word not in inverse_index:
						inverse_index[word] = set()
					inverse_index[word].add(count-1)
	print('Total runs readed from the file {} : {}'.format(path, count))
	return walks, count, inverse_index

def main(args):
	dictionary = readDict(args)
	walks1, total1, inverse1 = readWalks(args.WALKS1, args.DELIMITER1, count_only=False)
	walks2, total2, inverse2 = readWalks(args.WALKS2, args.DELIMITER2, inverse=True)
	writeFile = open(args.OUTPUT, 'w')
	count1 = 0
	count2 = 0
	written_count = 0
	for i, walk1 in enumerate(walks1):
		if i % 100 == 0: print('{}/{} walks completed in first language walks'.format(i, total1))
		valid = False
		for word1 in walk1:
			if not word1 in dictionary:
				continue
			valid = True
			print('translated: ', dictionary[word1])
			for word in dictionary[word1]:
				if not word in inverse2:
					continue
				for index in inverse2[word]:
					writeFile.write(' '.join(walk1) + ' ' + ' '.join(walks2[index]))
					written_count += 1
					if written_count % 10 == 0:
						print('{} walks written successfully'.format(written_count))
		if not valid:
			print('something is wrong.... no walks in other language corresponds to the word'.format(walks1[i]))
	print('Total walks written : {}'.format(written_count))

if __name__ == '__main__':
	main(argumentParser())
