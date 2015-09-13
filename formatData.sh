#!/bin/bash

python_exists ()
{
    type $1 &> /dev/null;
}

if python_exists python3
then
    PYTHON=python3
elif python_exists python3.4
then
    PYTHON=python3.4
else
    print "must have python3 or python3.4 in PATH" >&2
    exit 1
fi

$PYTHON split_data.py $1 ;
for i in {0..4};
do
    $PYTHON fold_train_test.py $i $1 ;
done

#python3 parseSdata.py $1
