import jsonrpclib
import pickle
import json


verbs = [
    'be', 'do', 'go', 'have', 'leave', 'keep', 'get', 'make',
    'tell', 'place', 'lose', 'change', 'give', 'hand', 'take',
    'buy', 'receive', 'put', 'set', 'like', 'want', 'call',
    'divide', 'split'
]


def cleannum(n):
    n = ''.join([x for x in n
                 if x.isdigit() or x == '.' or x == 'x' or x == 'x*'])
    return n


def parse_stanford_nlp(text, port=8080):
    server = jsonrpclib.Server("http://localhost:%d" % (port, ))
    return json.loads(server.parse(text))


def read_parse(k):
    with open('s_data/'+str(k)+'.pickle', 'rb') as f:
        return pickle.load(f)


def parse_inp(inp):
    q = []
    a = []
    e = []
    with open(inp) as f:
        f = f.readlines()
        i = 0
        while i < len(f):
            q.append(f[i])
            i += 1
            e.append(f[i])
            i += 1
            a.append(f[i])
            i += 1
    return (q, a, e)


def get_k_eqs(i, k=100, g=False, a=False, eqsdir='ILP.out'):
    digit = "{0:0=3d}".format(int(i))
    exprs = []
    with open(eqsdir + "/q" + digit + ".txt.out") as f:
        f = f.readlines()[3:-1]
        j = 0
        while j < k:
            if j >= len(f):
                break
            line = f[j]
            line = line.split(" | ")
            good = line[0].split(": ")[1]
            exp = line[6]
            for s in ['(', ')', '+', '-', '*', '/', '=']:
                exp = exp.replace(s, '  ' + s + ' ')
            exp = exp.replace('  ', ' ').strip()
            if g:
                cons = int(line[3])
                if cons == 0:
                    cons = 1
                else:
                    cons = 1 / (cons + 1)
                if a:
                    answ = line[5]
                    exprs.append((int(good), exp, cons, answ))
                else:
                    exprs.append((int(good), exp, cons))

            else:
                exprs.append((int(good), exp))
            j += 1
    return exprs


def preprocess_problem(problem):
    problem = problem.strip().split(" ")
    for i, x in enumerate(problem):
        if len(x) == 0:
            continue
        if x[-1] in [',', '.', '?']:
            problem[i] = x[:-1] + " " + x[-1]
    problem = ' '.join(problem)
    problem = " " + problem + " "
    return problem


def return_one(p, a, e, i):
    s = """{
"iIndex": %d,
"sQuestion": "%s",
"lEquations": [
"%s"
],
"lSolutions": [
%s
]
}""" % (i, p.strip(), e.strip(), a.strip())
    return s
