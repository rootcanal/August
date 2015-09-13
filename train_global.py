import sys

sys.path.insert(0, '/Users/rikka/libsvm-3.18/python')
import svmutil

import makesets
import utils


multi = None


def compute(p, op, e, target, problem, story, order):
    vec = makesets.vector(p, e, problem, story, target)
    op_label, op_acc, op_val = svmutil.svm_predict(
        [-1], [vec], multi, '-q -b 1'
    )
    op_val = op_val[0]
    if op == '+':
        val = op_val[0]
    if op == '-':
        val = op_val[1]
    if op == '*':
        val = op_val[2]
    if op == '/':
        val = op_val[3]
    if op == '=':
        val = op_val[1]

    c = makesets.combine(p[1], e[1], op)
    return (val, c, op_val)


def kill(signum, frame):
    raise Exception("end of time")


def training(a, b, problem, story, target, j, order, score, constraints):
    #this function take the trips and creates positive and negative training
    # instances from them
    if j == 0:
        j = -1
    vec = [j, order, score, constraints]
    vec.extend(makesets.eqvector(a, b, problem, story, target))

    return vec


def make_eq(q, a, equations):
    tdata = []
    wps = q  # open(q).readlines()

    for k in range(len(wps)):
        print(k, equations[k])
        answers = utils.get_k_eqs(equations[k], g=True)
        good = list(set([x for x in answers if x[0] == 1]))
        bad = list(set([x for x in answers if x[0] == 0]))[:len(good)]
        '''
        if len(bad)>len(good):
            bad = sample(bad,len(good))
        '''
        answers = good + bad
        if answers == []:
            continue
        answers = list(set(answers))

        # First preprocessing, tokenize slightly
        problem = utils.preprocess_problem(wps[k])
        print(problem)

        #make story
        #story = nlp.parse(problem)
        story = utils.read_parse(int(equations[k]))
        sets = makesets.makesets(story['sentences'])
        i = 0

        xidx = [i for i, x in enumerate(sets) if x[1].num == 'x']
        if not xidx:
            print("NO X WHY")
            continue

        #TODO look for 2 xes
        xidx = xidx[0]

        numlist = [(utils.cleannum(v.num), v) for k, v in sets]
        numlist = [x for x in numlist if x[0] != '']
        objs = {k: (0, v) for k, v in numlist}
        #print(numlist)
        consts = [x for x in answers[0][1].split(" ")
                  if x not in ['(', ')', '+', '-', '/', '*', '=', ]]
        #print(consts)
        present = [x for x in consts if x in objs]
        if present != consts:
            print(present, consts)
            print("missing thing")
            continue

        #print(answers)

        for j, eq, cons in answers:
            consts = [x for x in eq.split(" ")
                      if x not in ['(', ')', '+', '-', '/', '*', '=', ]]
            order = int(consts == [x[0] for x in numlist])
            if order == 0:
                continue
            print(j, eq)
            l, r = [x.strip().split(' ') for x in eq.split('=')]
            consts = " ".join([x for x in answers[0][1].split(" ")
                               if x not in ['(', ')', '+', '-', '/', '*', ]])
            consts = consts.split(" = ")
            target = 'x'
            target = (target, objs[target])

            #find innermost parens?
            sides = []
            thisscore = []
            for i, compound in enumerate([l, r]):
                while len(compound) > 1:
                    if "(" in compound:
                        rpidx = (len(compound) - 1) - compound[::-1].index('(')
                        lpidx = rpidx + compound[rpidx:].index(")")
                        subeq = compound[rpidx + 1:lpidx]
                        substr = "(" + ''.join(subeq) + ")"
                        compound = compound[:rpidx] + [substr]
                        compound += compound[lpidx + 1:]
                    else:
                        subeq = compound[0:3]
                        substr = "(" + ''.join(subeq) + ")"
                        compound = [substr] + compound[3:]
                    p, op, e = subeq
                    p = objs[p]
                    e = objs[e]
                    op = op.strip()
                    pute = compute(p, op, e, target, problem, story, order)
                    objs[substr] = pute
                    if pute == -1:
                        exit()
                    score, c, vals = pute
                    thisscore.append(score)
                sides.append(objs[compound[0]])
            p = sides[0]
            e = sides[1]
            score = 1
            for s in thisscore:
                score *= s
            #scores.append((score,j,eq))
            tdata.append(
                training(
                    sides[0],
                    sides[1],
                    problem,
                    story,
                    target,
                    j,
                    order,
                    score,
                    cons)
            )

    f = open("data/" + sys.argv[1][-1] + ".global.data", 'w')
    for v in tdata:
        f.write(str(v[0]) + " ")
        for i, j in enumerate(v[1:]):
            f.write(str(i + 1) + ":" + str(j) + " ")
        f.write("\n")


if __name__ == "__main__":
    #q, a = sys.argv[1:3]
    inp = sys.argv[1]
    multi = svmutil.svm_load_model(sys.argv[2])
    makesets.FOLD = sys.argv[1][-1]
    q, a, e = utils.parse_inp(inp)
    make_eq(q, a, e)
