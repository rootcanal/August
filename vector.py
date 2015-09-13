from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')

import utils


def eqvector(a, b, problem, story, target, feats=False):
    vec = vector(a, b, problem, story, target)
    return vec


def vector(a, b, problem, story, target, feats=False):
    a = a[1]
    b = b[1]

    vec = []
    features = []
    features.append(" a role d ")
    vec.append(int(a.role == 'do'))
    vec.append(int(a.role == 'subj'))
    vec.append(int(a.role == 'other'))
    vec.append(int(b.role == 'do'))
    vec.append(int(b.role == 'subj'))
    vec.append(int(b.role == 'other'))

    #subset
    vec.append(a.subset)
    vec.append(b.subset)

    features.append("a compound?")
    vec.append(int(a.compound))

    features.append("b compound?")
    vec.append(int(b.compound))

    features.append("a subtype of b")
    vec.append(int(a.entity in b.subtypes))

    features.append("b subtype of a")
    vec.append(int(b.entity in a.subtypes))

    features.append("a contians b entity match")
    if a.contains is None and b.entity is None:
        vec.append(0)
    elif a.contains is None or b.entity is None:
        vec.append(-1)
    elif b.entity in a.contains:
        vec.append(1)
    else:
        vec.append(-1)

    features.append("b contains a entity match")
    if b.contains is None and a.entity is None:
        vec.append(0)
    elif b.contains is None or a.entity is None:
        vec.append(-1)
    elif a.entity in b.contains:
        vec.append(1)
    else:
        vec.append(-1)

    features.append("acontainer bentity match")
    if a.container is None and b.entity is None:
        vec.append(0)
    elif a.container is None or b.entity is None:
        vec.append(-1)
    elif b.entity in a.container:
        vec.append(1)
    else:
        vec.append(-1)

    features.append("bcontainer aentity match")
    if b.container is None and a.entity is None:
        vec.append(0)
    elif b.container is None or a.entity is None:
        vec.append(-1)
    elif a.entity in b.container:
        vec.append(1)
    else:
        vec.append(-1)

    features.append("b container a entity match")
    if b.container is None and a.container is None:
        vec.append(0)
    elif b.container is None or a.container is None:
        vec.append(-1)
    else:
        #bcont = b.container.split(" ")[-1]
        #acont = a.container.split(" ")[-1]
        bcont = b.container
        acont = a.container
        if bcont in acont or acont in bcont:
            vec.append(1)
        else:
            vec.append(-1)

    features.append("entity match")
    if b.entity is None and a.entity is None:
        vec.append(0)
    elif b.entity == a.entity:
        vec.append(1)
    else:
        vec.append(-1)

    features.append("adj match")
    if b.adjs is None and a.adjs is None:
        vec.append(0)
    elif b.adjs == a.adjs:
        vec.append(1)
    else:
        vec.append(-1)

    features.append("loc match")
    if b.location is None and a.location is None:
        vec.append(0)
    elif b.location == a.location:
        vec.append(1)
    else:
        vec.append(-1)

    features.append('number distances')
    try:
        distance = abs(int(a.idx)-int(b.idx))
        distance = 1 / (10000 - distance)
    except:
        distance = 1
    vec.append(distance)

    asidx = a.idx//1000
    bsent = b.idx//1000

    features.append('x is operand')
    if a.num == 'x' or b.num == 'x':
        vec.append(1)
    else:
        vec.append(0)
    features.append('x is not operand')
    if a.num == 'x' or b.num == 'x':
        vec.append(0)
    else:
        vec.append(1)

    features.append('a target match')
    if a.entity == target:
        vec.append(1)
    else:
        vec.append(0)
    features.append('b target match')
    if b.entity == target:
        vec.append(1)
    else:
        vec.append(0)

    asidx = a.idx // 1000
    bsidx = b.idx // 1000
    story = story['sentences']
    asent = [x[0] for x in story[asidx]['words']]
    bsent = [x[0] for x in story[bsidx]['words']]
    #words inbetween features
    allwords = []
    for j in range(len(story)):
        for i, x in enumerate(story[j]['words']):
            allwords.append((j * 1000 + i, x[0]))
    low = min(a.idx, b.idx)
    high = max(a.idx, b.idx)
    wordseg = [x[1] for x in allwords if x[0] > low and high > x[0]]
    for item in [',', 'and', 'but']:
        features.append(item)
        if item in wordseg:
            vec.append(1)
        else:
            vec.append(0)

    extenders = [
        "a times",
        'b times',
        "a total",
        'b total',
        "a together",
        'b together',
        "a more",
        'b more',
        "a less",
        'b less',
        "a add",
        'b add',
        "a divide",
        'b divide',
        "a split",
        'b split',
        "a equal",
        'b equal',
        "a equally",
        'b equally'
    ]
    features.extend(extenders)
    lis = [
        "times",
        "total",
        "together",
        "more",
        "less",
        "add",
        "divide",
        "split",
        "equal",
        "equally"
    ]
    for li in lis:
        if li in asent:
            vec.append(1)
        else:
            vec.append(0)
        if li in bsent:
            vec.append(1)
        else:
            vec.append(0)
    #target features
    problem = story[-1]['text'].lower()
    if " how " in problem:
        problem = problem.split(" how ")[-1]
    elif " what " in problem:
        problem = problem.split(" what ")[-1]

    if " , " in problem:
        problem = problem.split(" , ")[0]
    features.append("in all")
    if "in all" in problem:
        vec.append(1)
    else:
        vec.append(0)
    features.append("end with")
    if "end with" in problem:
        vec.append(1)
    else:
        vec.append(0)
    problem = problem.split()
    extenders = [
        "times",
        "total",
        "together",
        "more",
        "less",
        "add",
        "divide",
        "split",
        "left",
        "equal",
        "equally",
        "now",
        'left',
        'start'
    ]
    features.extend(extenders)
    lis = [
        "times",
        "total",
        "together",
        "more",
        "less",
        "add",
        "divide",
        "split",
        "left",
        "equal",
        "equally",
        "now",
        'left',
        'start'
    ]
    for li in lis:
        if li in problem:
            vec.append(1)
        else:
            vec.append(0)

    if a.verbs is None or b.verbs is None:
        dist = 1
    else:
        avl = a.verbs.split(" ")
        bvl = b.verbs.split(" ")

        if len([x for x in avl if x in bvl]) > 0:
            dist = 0
        else:
            dist = 1
            for aw in avl:
                asyns = wn.synsets(aw)
                for asyn in asyns:
                    for bw in bvl:
                        bsyns = wn.synsets(bw)
                        for bsyn in bsyns:
                            if asyn._pos == bsyn._pos:
                                try:
                                    sim = bsyn.res_similarity(asyn, brown_ic)
                                    sim = 1 / (1 + sim)
                                except:
                                    sim = 2
                                if sim < dist:
                                    dist = sim
    features.append("Verb distance")
    vec.append(dist)

    #verb similarity

    for v in utils.verbs:
        features.append(v)
        vsyns = wn.synsets(v, pos='v')

        dist = 1
        if b.verbs is not None:
            for verb in b.verbs.split(' '):
                bsyns = wn.synsets(verb, pos='v')
                if verb == v:
                    dist = 0
                else:
                    for vsyn in vsyns:
                        for bsyn in bsyns:
                            try:
                                sim = vsyn.lin_similarity(bsyn, brown_ic)
                                sim = 1 / (1 + sim)
                            except:
                                sim = 2
                            if sim < dist:
                                dist = sim
        vec.append(dist)
    if feats:
        return (features, vec)
    else:
        return vec
