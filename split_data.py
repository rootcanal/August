# This code splits a dataset of the form:
#       Question
#       Equation
#       Answer
# into 5 randomly split folds in the data directory
import sys
import random

import utils



if __name__=='__main__':
    q,aas,ees = utils.parse_inp(sys.argv[1])
    idx = list(range(len(q)))
    random.shuffle(idx)
    fold = len(q)//5
    for i in range(4):
        fn = "data/indexes-1-fold-"+str(i)+".txt"
        thisfold = idx[i*fold:(i+1)*fold]
        with open(fn,'w') as f:
            for x in thisfold:
                f.write(str(x+1)+"\n")
    lastfold = idx[(i+1)*fold:]
    fn = "data/indexes-1-fold-"+str(i+1)+".txt"
    with open(fn,'w') as f:
        for x in lastfold:
            f.write(str(x+1)+"\n")


