import argparse
import os
import io

def parser():
	parser = argparse.ArgumentParser(description='split embeddings in given two languges in dictionary')
	parser.add_argument('input', help='input file for merged embeddings.')
	parser.add_argument('dictionary', help='dictionary file path')
	parser.add_argument('output1', help='path for the first output file')
	parser.add_argument('output2', help='path for the second output file')
	return parser.parse_args()

def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
    return data, n, d

def main(args):
	lang2_vocab = set()
	lang1_vocab = set()
	# reading dictionary
	with open(args.dictionary, 'r') as readFile:
		for row in readFile:
			tokens = row.rstrip().split('\t')
			lang1_vocab.add(tokens[0])
			for token in tokens[1:]:
				lang2_vocab.add(token)
	# reading embedding
	count1 = 0
	count2 = 0
	emb1 = {}
	emb2 = {}
	merged, n, dim = load_vectors(args.input)
	for key in merged:
		if key in lang1_vocab:
			emb1[key] = merged[key]
			count1 += 1
		elif key in lang2_vocab:
			emb2[key] = merged[key]
			count2 += 1
	if count1 + count2 != n:
		print('doesnt matching....')
	with open(args.output1, 'w') as writeFile:
		writeFile.write(str(count1) + ' ' + str(dim) + '\n')
		for key in emb1:
			writeFile.write(key + ' ' +' '.join([str(e) for e in emb1[key]]) + '\n')
	with open(args.output2, 'w') as writeFile:
                writeFile.write(str(count2) + ' ' + str(dim) + '\n')
                for key in emb2:
                        writeFile.write(key + ' ' +' '.join([str(e) for e in emb2[key]]) + '\n')
	print('embedding splitted in file:')
	print(args.output1)
	print(args.output2)

if __name__ == '__main__':
	main(parser())
