import sys
import makesets
import EntityFileCreator as EF

import utils

OUT=None


def make_eq(q,a,VERBOSE,TRAIN):
    #wps = open(q).readlines()
    #answs = open(a).readlines()
    #VERBOSE=True
    wps = q


    


    for k in range(len(wps)):
        if VERBOSE:
            for i in range(len(wps)):
                print(i,wps[i])
            k = int(input())
        print(k)
        #First preprocessing, tokenize slightly
        problem = utils.preprocess_problem(wps[k])
        print(problem)

        story = utils.parse_stanford_nlp(problem)
        sets = makesets.makesets(story['sentences'])
        EF.main(sets,k,a[k],sys.argv[1])
        sets = [x for x in sets if makesets.floatcheck(x[1].num) or x[1].num == 'x']
        print(sets)
        for z in sets:
            z[1].details()



if __name__=="__main__":
    #q, a = sys.argv[1:3]
    inp = sys.argv[1]
    q,a,e = utils.parse_inp(inp)
    VERBOSE=False
    TRAIN=False
    '''
    if len(sys.argv)>3:
        if sys.argv[3]=='v':
            VERBOSE=True
        elif sys.argv[3]=='t':
            TRAIN = True
            OUT = sys.argv[4]
    '''
    make_eq(q,a,VERBOSE,TRAIN)


