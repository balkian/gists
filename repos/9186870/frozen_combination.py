def frozen_combination(*args):
    combinations = set([frozenset(),])
    for arg in args:
        tempcomb = set(frozenset(),)
        for i in set(arg):
            tempcomb.update(set([frozenset(list(c)+[i]) for c in combinations if i not in c]))
        if len(tempcomb) > 0:
            combinations = tempcomb
    return combinations
#    return [set(comb) for comb in combinations] # for sets instead of frozensets
res = frozen_combination(a,b)
print res
print len(res)