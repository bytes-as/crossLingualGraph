# crossLingualGraph


The script `script.sh` follows a sequence of python scripts and monolingual embedding generation directly invoked from word2vec binary files

`script.sh` script takes 7 command line arguments:
1. Source language graph database file <FILE PATH>
2. Minimum frequency for the source language graph nodes which is to be used in generating sentences <INT>
3. Source language graph database file <FILE PATH>
4. Minimum frequency for the target language graph nodes which is to be used in generating sentences <INT>
5. Dictionary for translation of source langauge to target langauge <two words per line seperated by '\t'>
6. Number of walks for the source language to be generated in between the process <INT>
7. Number of walks for the target language to be generated in between the process <INT>

the script will work as follows:
1. convert word edge list graph to int edge list graph for both language, target and source
  code written in `scripts/preprocess.py`: will convert the word to int and create edge list graph and save the conversion dictionarie in pickle file
2. run deepwalks to generate random walks for both languages
3. run a conversion of int walks to word walks for both langauges
4. run monolingual embedding generation on both random walks generated for intermeditary analysis
5. Merge walks of two languages using the translational dictionaries
  for every sentence in first language walks
  take each word
  find it's translation
  find the sentences with the translated word in second language walks
  create a new sentence by joining those two sentence
6. Generate word embedding of that merged walks data
7. Split word embedding according to the language
8. Call vecmap scripts to evaluate cross lingual word embedding

Each individual python script has its own help section which can be accessed by `python <script>.py -h`.

Result will be in the exp folder here itself.
an example of script running could be:
`user@machine:~/crossLingualGraph$ ./script.sh ./../may/corpus/LMI_w1000_p1000 20000 ./../may/corpus/DT_hin 200
00 ./../may/corpus/en-hi.txt  1 1 `
which will result in following files:
```
user@machine:~/crossLingualGraph/exp$ ll -h
drwxr-xr-x. 6 16CS10008 btech 4.0K May  4 04:27 ./
drwxr-xr-x. 8 16CS10008 btech 4.0K May  4 04:34 ../
drwxr-xr-x. 2 16CS10008 btech 4.0K May  4 04:21 english_20000/
drwxr-xr-x. 2 16CS10008 btech 4.0K May  4 03:15 english_25000/
-rw-r--r--. 1 16CS10008 btech  11M May  4 04:20 english_25000_21000.cross_emb  <-- english embedding in crosslingual domain
drwxr-xr-x. 2 16CS10008 btech 4.0K May  4 04:22 hindi_20000/
drwxr-xr-x. 2 16CS10008 btech 4.0K May  4 02:47 hindi_21000/
-rw-r--r--. 1 16CS10008 btech  15M May  4 04:20 hindi_25000_21000.cross_emb  <-- hindi embedding in cross lingual domain
-rw-r--r--. 1 16CS10008 btech 5.8G May  4 04:23 merged_walks_20000_20000.txt
-rw-r--r--. 1 16CS10008 btech 1.4G May  4 03:59 merged_walks_25000_21000.txt  <-- merged walks
-rw-r--r--. 1 16CS10008 btech 110M May  4 04:20 merged_walks_25000_21000.VEC  <-- merged embeddings
-rw-r--r--. 1 16CS10008 btech 910K May  4 04:20 test_dict.txt  <-- tranlational dictionary with ' ' as delimiter in line
```
and in the folder named `english_25000` which means english processed data with minimum node frequency of 25000:
```
user@machine:~/crossLingualGraph/exp/english_25000$ ll -h 
drwxr-xr-x. 2 16CS10008 btech 4.0K May  4 03:15 ./
drwxr-xr-x. 6 16CS10008 btech 4.0K May  4 04:27 ../
-rw-r--r--. 1 16CS10008 btech  24M May  4 03:15 english_int_25000.VEC  --> embedding vec(s) with words replaced by unique integer
-rw-r--r--. 1 16CS10008 btech 2.3M May  4 03:14 english_int_25000.walks --> random walks with unique ints
-rw-r--r--. 1 16CS10008 btech 2.5M May  4 03:15 english_word_25000.walks --> random walks
-rw-r--r--. 1 16CS10008 btech 231K May  4 03:07 graph_int_25000.english  --> graph with unique int for every word
-rw-r--r--. 1 16CS10008 btech  50M May  4 03:06 int2word_25000.english  --> int to word mapping
-rw-r--r--. 1 16CS10008 btech  50M May  4 03:06 word2int_25000.english  --> word to int mapping
```
