import sys
import pickle

import utils

OUT = None


def make_eq(q, a, VERBOSE, TRAIN):
    wps = q

    for k in range(len(wps)):
        if VERBOSE:
            for i in range(len(wps)):
                print(i, wps[i])
            k = int(input())
        print(k)
        #First preprocessing, tokenize slightly
        problem = utils.preprocess_problem(wps[k])
        print(problem)

        story = utils.parse_stanford_nlp(problem)
        with open("s_data/" + str(k) + ".pickle", 'wb') as f:
            pickle.dump(story, f)


if __name__ == "__main__":
    #q, a = sys.argv[1:3]
    inp = sys.argv[1]
    q, a, e = utils.parse_inp(inp)
    VERBOSE = False
    TRAIN = False
    '''
    if len(sys.argv)>3:
        if sys.argv[3]=='v':
            VERBOSE=True
        elif sys.argv[3]=='t':
            TRAIN = True
            OUT = sys.argv[4]
    '''
    make_eq(q, a, VERBOSE, TRAIN)
