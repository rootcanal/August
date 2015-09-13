import sys
import makesets
import pickle

import utils


def kill(signum, frame):
    raise Exception("end of time")


def training(trips, problem, story, target):
    # this function take the trips and creates positive
    # and negative training instances from them
    texamples = {x: ([], []) for x in ["+", "*", '/', '-', '=']}
    for op, a, b in trips:
        if op == '=':
            vec = makesets.eqvector(a, b, problem, story, target)
        else:
            vec = makesets.vector(a, b, problem, story, target)
        texamples[op][0].append(vec)

    return texamples


def make_eq(q, a, equations):
    bigtexamples = {x: ([], []) for x in ["+", "*", '/', '-', '=']}
    wps = q  # open(q).readlines()

    for k in range(len(wps)):

        # First preprocessing, tokenize slightly
        problem = utils.preprocess_problem(wps[k])
        print(k)
        print(problem)

        # story = nlp.parse(problem)
        story = utils.read_parse(int(equations[k]))
        eqs = utils.get_k_eqs(equations[k])
        answers = [x[1] for x in eqs if x[0] == 1]
        if answers == []:
            continue
        answers = list(set(answers))
        print(story["sentences"][0]["text"])
        print(answers)

        #make story
        #story = nlp.parse(problem)
        sets = makesets.makesets(story['sentences'])
        i = 0

        xidx = [i for i, x in enumerate(sets) if x[1].num == 'x']
        if not xidx:
            print("NO X WHY")
            continue

        numlist = [(utils.cleannum(v.num), v) for k, v in sets]
        numlist = [x for x in numlist if x[0] != '']
        objs = {k: (0, v) for k, v in numlist}
        print(objs.items())
        consts = [x for x in answers[0].split(" ")
                  if x not in ['(', ')', '+', '-', '/', '*', '=', ]]
        present = [x for x in consts if x in objs]
        if present != consts:
            print(present, consts)
            print("missing thing")
            exit()

        #simpleanswers = []
        for j, eq in enumerate(answers):
            trips = []
            print(j, eq)
            l, r = [x.strip().split(' ') for x in eq.split('=')]
            target = 'x'
            target = (target, objs[target])

            #find innermost parens?
            for i, compound in enumerate([l, r]):
                while len(compound) > 1:
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
                    if True:
                        p, op, e = subeq
                        p = objs[p]
                        e = objs[e]
                        op = op.strip()
                        trips.append((op, p, e))
                        pute = (0, makesets.combine(p[1], e[1], op))
                        objs[substr] = pute
                    if pute == -1:
                        exit()
            t = training(trips, problem, story, target)
            for op in t:
                bigtexamples[op][0].extend(t[op][0])
                bigtexamples[op][1].extend(t[op][1])
    pickle.dump(
        bigtexamples, open('data/' + sys.argv[1][-1] + ".local.training", 'wb')
    )


eqsdir = "ILP.out"


if __name__ == "__main__":
    #q, a = sys.argv[1:3]
    inp = sys.argv[1]
    #eqsdir = sys.argv[2]
    makesets.FOLD = sys.argv[1][-1]
    q, a, e = utils.parse_inp(inp)

    make_eq(q, a, e)
