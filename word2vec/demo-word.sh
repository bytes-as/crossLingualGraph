
time ./word2vec -train $1 -output $2 -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 30 1 -iter 15
./distance vectors.bin
