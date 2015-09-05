#!/bin/bash


python3 split_data.py $1 ;
for i in {0..4};
do
    python3 fold_train_test.py $i $1 ;
done

#python3 parseSdata.py $1
