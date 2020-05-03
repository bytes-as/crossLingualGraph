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

def readWalks(path, delim, count_only=True):
	walks = []
	count = 0
	with open(path, 'r') as readFile:
		for line in readFile:
			count += 1
			if count_only: continue
			if count % 100000 == 0:
				print('{} lines readed from the file {}'.format(count, path))
			walks.append(line.rstrip().split(delim))
	print('Total runs readed from the file {} : {}'.format(path, count))
	return walks, count

def main(args):
	dictionary = readDict(args)
	walks1, total1 = readWalks(args.WALKS1, args.DELIMITER1, count_only=True)
	walks2, total2 = readWalks(args.WALKS2, args.DELIMITER2)
	writeFile = open(args.OUTPUT, 'w')
	count1 = 0
	count2 = 0
	total = 0
	for i in range(total1):
		with open(args.WALKS1, 'r') as readFile:
			count1 = 0
			for line in readFile:
				if count1 == i:
					walk1 = line.rstrip().split(args.DELIMITER1)
					break
				count1 += 1
		print('{} walks completed in first language walks'.format(i))
		for word1 in walk1:
			if not word1 in dictionary:
				print('{} not found in dictinoary'.format(word1))
				continue
			translated = dictionary[word1]
			count2 = 0
			for walk2 in walks2:
				count2 += 1
				if count2 % 10000 == 0:
					print('{}/{} walks compared successfully'.format(count2, total2))
				if word1 in walk2:
					total += 1
					if total % 100 == 0:
						print('{} walks written'.format(total))
					writeFile.write(' '.join(walk1) + ' ' + ' '.join(walk2) + '\n')
			if count1 == 0:
				total2 = count2
	print('Total walks written : {}'.format(total))

if __name__ == '__main__':
	main(argumentParser())
