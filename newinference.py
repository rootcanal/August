import sys

sys.path.insert(0, '/Users/rikka/libsvm-3.18/python')
import svmutils

import makesets
import utils


multi = None
glob = None

def make_eq(q,a,equations):
    wps = q #open(q).readlines()
    right = 0
    wrong = 0

    for k in range(len(wps)):
        answers = utils.get_k_eqs(equations[k],g=True,a=True)
        if answers == []: continue
        seeneq = []
        seen = []
        for x in answers:
            if x[1] not in seeneq:
                seen.append(x)
                seeneq.append(x[1])
        answers = seen
        answers = list(set(answers))
        


        #First preprocessing, tokenize slightly
        problem = utils.preprocess_problem(wps[k])
        print(problem)


        #make story
        #story = nlp.parse(problem)
        story = utils.read_parse(int(equations[k]))
        sets = makesets.makesets(story['sentences'])
        i = 0

        ######
        for x in sets:
            x[1].details()
        #continue

        xidx = [i for i,x in enumerate(sets) if x[1].num=='x']
        if not xidx:
            print("NO X WHY");continue

        #TODO look for 2 xes
        xidx = xidx[0]


        numlist = [(utils.cleannum(v.num),v) for k,v in sets]
        numlist = [x for x in numlist if x[0]!='']
        objs = {k:(0,v) for k,v in numlist}
        print(objs.items())
        consts = [x for x in answers[0][1].split(" ") if x not in ['(',')','+','-','/','*','=',]]
        present = [x for x in consts if x in objs]
        if consts!=present: print(present,consts);print("missing thing");continue
        if len([x for x in objs if x not in consts])>0: print("missing thing");continue
        scores = []


        for j,eq,cons,guess in answers:
            consts = [x for x in eq.split(" ") if x not in ['(',')','+','-','/','*','=',]]
            order = int(consts==[x[0] for x in numlist])
            if order == 0: continue
            #j = randint(0,len(answers)-1)
            #eq = answers[j]
            #print(j,eq)
            l,r = [x.strip().split(' ') for x in eq.split('=')]
            consts = " ".join([x for x in answers[0][1].split(" ") if x not in ['(',')','+','-','/','*',]])
            consts = consts.split(" = ")
             
            target = 'x'
            target = (target,objs[target])

            #find innermost parens?
            sides = []
            thisscore = []
            for i,compound in enumerate([l,r]):
                while len(compound)>1:
                    if "(" in compound:
                        rpidx = (len(compound) - 1) - compound[::-1].index('(')
                        lpidx = rpidx+compound[rpidx:].index(")")
                        subeq = compound[rpidx+1:lpidx]
                        substr = "("+''.join(subeq)+")"
                        compound = compound[:rpidx]+[substr]+compound[lpidx+1:]
                    else:
                        subeq = compound[0:3]
                        substr = "("+''.join(subeq)+")"
                        compound = [substr]+compound[3:]
                    p,op,e = subeq
                    p = objs[p]
                    e = objs[e]
                    op = op.strip()
                    pute = compute(p,op,e,target,problem,story,order)
                    objs[substr]=pute
                    if pute == -1:
                        exit()
                    score,c,vals = pute
                    thisscore.append(score)
                sides.append(objs[compound[0]])
            p = sides[0]; e = sides[1]
            score = 1
            for s in thisscore: score *= s
            score *= compute(p,'=',e,target,problem,story,order,score,cons)[0]
            scores.append((score,j,eq,guess))
        scores = sorted(scores,reverse=True)
        righties = [x for x in scores if x[1]==1]
        print(scores[:3])
        if not righties:
            wrong+=1
            print("TOP SCORING NO CORRECT SOLUTION \nINCORRECT")
            continue

        if len(scores)>0:
            if scores[0][1]==1:
                right += 1
                print("CORRECT")
            else:
                wrong += 1
                print("INCORRECT")
        else:
            wrong += 1
            print("INCORRECT")

    return (right,wrong)


def compute(p,op,e,target,problem,story,order,score=None,cons=None):
    if op == '=':
        vec = [order,score,cons]
        vec.extend(makesets.vector(p,e,problem,story,target))
        op_label, op_acc, op_val = svmutils.svm_predict([-1], [vec], glob ,'-q -b 1')
    else:
        vec = makesets.vector(p,e,problem,story,target)
        op_label, op_acc, op_val = svmutils.svm_predict([-1], [vec], multi ,'-q -b 1')

    op_val=op_val[0]
    if op == '+':
        val = op_val[0]
    if op == '-':
        val = op_val[1]
    if op == '*':
        val = op_val[2]
    if op == '/':
        val = op_val[3]
    if op == '=':
        val = op_val[0]


    c = makesets.combine(p[1],e[1],op)
    return (val,c,op_val)


if __name__=="__main__":
    inp, mfile, gfile = sys.argv[1:4]
    multi = svmutils.svm_load_model(mfile)
    glob = svmutils.svm_load_model(gfile)
    #q, a = sys.argv[1:3]
    inp = sys.argv[1]
    makesets.FOLD = sys.argv[1][-1]
    q,a,e = utils.parse_inp(inp)
    right, wrong = make_eq(q,a,e)
    print(right,wrong,right/len(q))


