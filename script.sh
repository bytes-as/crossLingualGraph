#ROOT=/home/bt0/16CS10008/may
ROOT=.
mkdir "./exp"
EXP_DIR=$ROOT/exp
SCRIPTS=$ROOT/scripts
FREQ1=${2}
ENGLISH=${1}
HINDI=${3}
FREQ2=${4}
DICTIONARY=${5}
PYTHON=python

# Generate Graph replacing word with number ro run deepwalk
mkdir "$EXP_DIR/english_$FREQ1"
mkdir "$EXP_DIR/hindi_$FREQ2"


# Generate conversion dictionaries and frequencies table and shorten graph if required, will save the conversion dictionaries from word to int and vice versa in the passed argument of root folder
# Python Scripy <preprocess.py> takes argument as follows:
#	<english edge list> <language 1: english> --ROOT <ROOT directory for this english instance> --OUTPUT_FILE <output file NAME to save the graph> --MIN <minimum frequency for graph nodes>
$PYTHON $SCRIPTS/preprocess.py $ENGLISH english --ROOT $EXP_DIR/english_$FREQ1 --OUTPUT_FILE graph_int_${FREQ1}.english --MIN $FREQ1

$PYTHON $SCRIPTS/preprocess.py $HINDI hindi --ROOT $EXP_DIR/hindi_$FREQ2 --OUTPUT_FILE graph_int_${FREQ2}.hindi --MIN $FREQ2




# Run deepwalk to generate walks: just to save the walks of int nodes
cd $ROOT/deepwalk
$PYTHON -m deepwalk --input $EXP_DIR/english_$FREQ1/graph_int_${FREQ1}.english --format edgelist --walks-output $EXP_DIR/english_$FREQ1/english_int_${FREQ1}.walks --workers 30 --number-walks 1

$PYTHON -m deepwalk --input $EXP_DIR/hindi_$FREQ2/graph_int_${FREQ2}.hindi --format edgelist --walks-output $EXP_DIR/hindi_$FREQ2/hindi_int_${FREQ2}.walks --workers 30 --number-walks 1
cd $ROOT

# generate monolingual embedding 
$ROOT/word2vec/word2vec -train $EXP_DIR/english_$FREQ1/english_int_${FREQ1}.walks -output $EXP_DIR/english_$FREQ1/english_int_${FREQ1}.VEC  -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 30 1 -iter 15

$ROOT/word2vec/word2vec -train $EXP_DIR/hindi_$FREQ2/hindi_int_${FREQ2}.walks -output $EXP_DIR/hindi_$FREQ2/hindi_int_${FREQ2}.VEC  -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 30 1 -iter 15

# convert embedding from int to words
$PYTHON $SCRIPTS/convert_embedding.py $EXP_DIR/english_$FREQ1/english_int_${FREQ1}.VEC $EXP_DIR/english_$FREQ1/int2word_${FREQ1}.english --OUTPUT $EXP_R/english_$FREQ1/english_word_${FREQ1}.VEC

$PYTHON $SCRIPTS/convert_embedding.py $EXP_DIR/hindi_$FREQ2/hindi_int_${FREQ2}.VEC $EXP_DIR/hindi_$FREQ2/int2word_${FREQ2}.hindi --OUTPUT $EXP_DIR/hindi_$FREQ2/hindi_word_${FREQ2}.VEC


# convert walks from int to words
$PYTHON $SCRIPTS/convert_walks.py $EXP_DIR/english_$FREQ1/english_int_${FREQ1}.walks $EXP_DIR/english_$FREQ1/int2word_${FREQ1}.english --OUTPUT $EXP_DIR/english_$FREQ1/english_word_${FREQ1}.walks --OUT_DELIMITER ' '

$PYTHON $SCRIPTS/convert_walks.py $EXP_DIR/hindi_$FREQ2/hindi_int_${FREQ2}.walks $EXP_DIR/hindi_$FREQ2/int2word_${FREQ2}.hindi --OUTPUT $EXP_DIR/hindi_$FREQ2/hindi_word_${FREQ2}.walks --OUT_DELIMITER ' '

# filter graphs (was hoping to remove some amount of data because it's not available in both languages, Not much effect though)
#$PYTHON $SCRIPTS/filter_walks.py $EXP_DIR/english_${FREQ1}/english_word_${FREQ1}.walks $DICTIONARY $EXP_DIR/english_$FREQ1/filtered_english_word_${FREQ1}.walks

#$PYTHON $SCRIPTS/filter_walks.py $EXP_DIR/hindi_${FREQ2}/hindi_word_${FREQ2}.walks $DICTIONARY $EXP_DIR/hindi_$FREQ2/filtered_hindi_word_${FREQ2}.walks --POSITION 1

# merge walks
$PYTHON $SCRIPTS/mergeWalks.2.2.py $EXP_DIR/english_$FREQ1/english_word_${FREQ1}.walks $EXP_DIR/hindi_${FREQ2}/hindi_word_${FREQ2}.walks $DICTIONARY $EXP_DIR/merged_walks_${FREQ1}_${FREQ2}.txt --DELIMITER1 ' ' --DELIMITER2 ' '

$ROOT/word2vec/word2vec -train $EXP_DIR/merged_walks_${FREQ1}_${FREQ2}.txt -output $EXP_DIR/merged_walks_${FREQ1}_${FREQ2}.VEC  -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 30 1 -iter 15

$PYTHON $SCRIPTS/splitEmbeddings.py $EXP_DIR/merged_walks_${FREQ1}_${FREQ2}.VEC $DICTIONARY $EXP_DIR/english_${FREQ1}_${FREQ2}.cross_emb $EXP_DIR/hindi_${FREQ1}_${FREQ2}.cross_emb

$PYTHON $SCRIPTS/changeDelimiter.py $DICTIONARY $EXP_DIR/test_dict.txt --out_dlim ' '

$PYTHON $ROOT/vecmap/eval_translation.py $EXP_DIR/english_${FREQ1}_${FREQ2}.cross_emb $EXP_DIR/hindi_${FREQ1}_${FREQ2}.cross_emb -d $EXP_DIR/test_dict.txt
