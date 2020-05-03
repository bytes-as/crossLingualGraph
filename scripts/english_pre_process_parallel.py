import argparse
import os
import sys
import pickle
import multiprocess as mp
from multiprocess import Process, Lock, Pool
from time import time

def assignNumbers(pid, args, word2int, output_file_descriptor, lock, lines, total_lines_count):
	print('Starting Process | id: {}'.format(pid))
	count = 0
	for line in lines:
		word1 = word2int[line[0]]
		word2 = word2int[line[1]]
		weight = line[2]
		if args.WEIGHTED:
			lock.acquire()
			output_file_descriptor.write(str(word1) + '\t' + str(word2) + '\t' + weight + '\n')
			lock.release()
		else:
			lock.acquire()
			output_file_descriptor.write(str(word1) + '\t' + str(word2) + '\n')
			lock.release()
		count += 1
		if count % 10 == 0:
			print('successfully written {}/{} edges in the file with the process pid: {}'.format(\
				count, total_lines_count, pid))
	print('Exiting Process | id {}'.format(pid))

def writeFileModule(dictionary, file_name):
	with open(file_name, 'wb') as writeFile:
		pickle.dump(dictionary, writeFile)
	print('Writing file {} done'.format(file_name))

def main(args):
	lines = []
	word2int = {}
	int2word = {}
	count = 0
	line_count = 0
	pid = 0
	readFile = open(args.FILE_PATH, 'r')
	writeFile = open(args.OUTPUT_FILE_PATH, 'w')
	start = time()
	cpu_count = mp.cpu_count()
	pool = Pool(cpu_count-1)
	processes = []
	print('Starting everything...')
	lock = mp.Lock()
	for line in readFile:
		print('line count: {}'.format(line_count))
		word1 = line.split('\n')[0].split('\t')[0].split('/')[0]
		word2 = line.split('\n')[0].split('\t')[1].split('/')[1]
		weight = line.split('\n')[0].split('\t')[-1]
		lines.append([word1, word2, weight])
		for word in [word1, word2]:
			if not word in word2int:
				word2int[word] = count
				int2word[count] = word
				count += 1
		line_count += 1
		if line_count % 8000000 == 0:
			# senf the lines to be written in new file
			p = Process(target=assignNumbers, args=(pid, args, word2int, writeFile, lock, lines, len(lines)))
			processes.append(p)
			p.start()
			pid += 1
			lines = []
	for process in processes:
		process.join()
	end = time()
	print('Total time for the whole process : {} seconds'.format(end - start))
	print('proceddings with writign mappings')
	# pool.map(writeFileModule, [(word2int, 'word2int.eng'), (int2word, 'int2word.eng')])
	P = Process(target=writeFileModule, args=(word2int, 'word2int.eng'))
	Q = Process(target=writeFileModule, args=(int2word, 'int2word.eng'))
	P.start()
	Q.start()
	P.join()
	Q.join()
	readFile.close()
	writeFile.close()



	
def parseArguments():
	parser = argparse.ArgumentParser(description='Preprocess english graph and remove weights and assigns the unique number')
	parser.add_argument('FILE_PATH', help='Input file path of the raw graph')
	parser.add_argument('--OUTPUT_FILE_PATH', default='./graph.eng')
	parser.add_argument('--WEIGHTED', action='store_true')
	return parser.parse_args()

if __name__ == '__main__':
	args = parseArguments()
	main(args)