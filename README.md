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
3. run monolingual embedding generation on both random walks generated for intermeditary analysis
4. Conversion of embeddings where words represented by unique number to the actual representaion of words for both lang
5. Convert random walks generated using deepwalk from unique number representation to the word representation
6. Merge walks of two languages using the translational dictionaries
7. Generate word embedding of that merged walks data
8. Split word embedding according to the language
9. Call vecmap scripts to evaluate cross lingual word embedding

Each individual python script has its own help section which can be accessed by `python <script>.py -h`.
