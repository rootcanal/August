# import pickle
# import entity


def numclean(num):
    if num in ['each', 'every', 'per', 'an', 'a', 'one']:
        return num
    else:
        try:
            return float(''.join([x for x in num if x.isdigit() or x == '.']))
        except:
            pass
        #print(num)


def main(sets):
    conversions = createConversions()

    #simple solution: targets are things that come after the x
    xidx = [x[0] for x in sets if x[1].num == 'x']
    if not xidx:
        return sets
    xidx = xidx[0]
    target = [x[1] for x in sets if x[0] >= xidx]

    for targ in target:
        if targ.entity not in ['dollar', 'money', 'second', 'minute', 'hour']:
            continue
        for idx, entity in sets:
            if entity.num == 'x':
                continue
            if entity.entity == targ.entity:
                continue
            convertedVal = findConversion(
                [numclean(entity.num), entity.entity], targ.entity, conversions
            )
            if convertedVal is not None:
                #print("CONVERTING")
                #print(entity.entity,targ.entity)
                entity.entity = targ.entity
                entity.num = str(convertedVal)

    return sets


def findConversion(unit, target, conversions):
    for c in conversions.keys():
        con_i = conversions[c][c.index(unit[1])]
        con_t = conversions[c][c.index(target)]

        if (unit[1] in c) and (target in c):
            if unit[0] in ['each', 'every', 'per', 'an', 'a', 'one']:
                newVal = unit[0] + " " + str(con_i / con_t)
            else:
                try:
                    float(unit[0])
                except:
                    return None
                newVal = float(unit[0]) * con_i / con_t
            return newVal
    return None


def createConversions():
    conversions = dict([])

    # time
    time = ('second', 'minute', 'hour', 'day', 'week', 'month', 'year')
    # 30 days in a year
    t = [1, 60, 3600, 86400, 604800, 2592000, 31536000]
    # for years to minutes:
    # take number * years / minute
    conversions[time] = t

    # dozens
    # TODO: one egg
    '''
    dozens = ('half-dozen', 'dozen')
    d = [1, 6, 12]
    conversions[dozens] = d
    '''

    # money
    money = (
        '$', 'money', 'cent', 'penny', 'nickel',
        'dime', 'quarter', 'half-dollar', 'dollar', 'five-dollar bills'
    )
    m = [100, 100, 1, 1, 5, 10, 25, 50, 100, 500]
    conversions[money] = m

    # distance
    distance = ('inches', 'feet', 'yards')
    d = [1, 12, 36]
    conversions[distance] = d

    return conversions


if __name__ == "__main__":
    main()
