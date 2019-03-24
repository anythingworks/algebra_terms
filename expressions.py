from itertools import groupby
from functools import reduce
from copy import deepcopy


class Add:
    def __init__(self, a_input, b_input):
        self.a = a_input
        self.b = b_input

    def __str__(self):
        return "(" + str(self.a) + " + " + str(self.b) + ")"

    def evaluate(self):
        a = self.a.evaluate()
        b = self.b.evaluate()
        return a + b

    def commute(self):
        got_a = self.a
        got_b = self.b
        self.a = got_b
        self.b = got_a


class Mul:
    def __init__(self, a_input, b_input):
        self.left = a_input
        self.right = b_input

    def __str__(self):
        return "(" + str(self.left) + " * " + str(self.right) + ")"

    def evaluate(self):
        a = self.left.evaluate()
        b = self.right.evaluate()
        return a * b

    def apply_terms(self):
        left = deepcopy(self.left)
        right = deepcopy(self.right)
        return Term(left.coef * right.coef, left.base, left.expn + right.expn)

    def commute(self):
        left  = deepcopy(self.left)
        right = deepcopy(self.right)
        return Mul(right, left)

    def distribute(self):
        left = deepcopy(self.left)
        right = deepcopy(self.right)
        mapped = map(lambda term: Mul(left, term), right)
        return Sum(list(mapped))


class Sum:
    def __init__(self, ts):
        self.idx = 0
        self.terms = ts
        if len(ts) > 0 and isinstance(ts[0], Term):
            self.terms.sort(key=lambda t: t.expn, reverse=True)
            self.terms = list(filter(lambda term: term.coef != 0, self.terms))

    def __str__(self):
        sum = ' + '.join(map(str, self.terms))
        return '[ ' + sum + ' ]'

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx is len(self.terms):
            raise StopIteration
        else:
            nxt = self.terms[self.idx]
            self.idx += 1
            return nxt

    def __getitem__(self, idx):
        return self.terms.__getitem__(idx)

    def __setitem__(self, item):
        return self.terms.__setitem__(item)

    def __delitem__(self):
        return self.terms.__delitem__()

    def evaluate(self):
        acc = 0
        for term in self.terms:
            acc += term.evaluate()
        return acc

    def aggregate(self):
        aggregated_terms = []
        for key, group in groupby(self.terms, lambda tm: tm.expn):
            aggs = reduce(lambda a, b: a.aggregate(b), group)
            aggregated_terms.append(aggs)
        self.terms = aggregated_terms
        return deepcopy(self)

    def commute_terms(self):
        return Sum(list(map(lambda m: m.commute(), self)))

    def distribute_terms(self):
        return Sum(list(map(lambda m: m.distribute(), self)))

    def apply_muls(self):
        applied = list(map(lambda m: m.apply_terms(), self))
        return Sum(applied)

    def de_associate(self):
        acc = []
        for sum in self.terms:
            for term in sum:
                acc.append(term)
        return Sum(acc)


class Term:
    def __init__(self, c, b, e):
        self.coef = c
        self.base = b
        self.expn = e

    def __str__(self):
        if self.expn == 0:
            return str(self.coef)
        elif self.expn == 1:
            return str(self.coef) + "x"
        else:
            return str(self.coef) + "x^" + str(self.expn)

    def aggregate(self, t):
        return Term(self.coef + t.coef, self.base, self.expn)

    def evaluate(self):
        return self.coef * (self.base ** self.expn)


def number_to_sum(num):

    length = len(num)
    r = range(length)

    for idx in r:
        darget = num[idx]

        print(idx,',',darget)
    return



nummir = '345076099'
sum = number_to_sum(nummir)
print(">>>")
print(sum)

# print()
# print('two sum of terms:')
# num_num = "123"
# a_sum = number_to_sum(num_num)
# another_number = "456"
# another_sum = number_to_sum(another_number)
# print(num_num, ': ', a_sum)
# print(another_number, ': ', another_sum, '\n')
# print('multiply 2 sums of terms:')
# a_mul = Mul(a_sum, another_sum)
# print(a_mul, '\n')
# print('distribute left sum over right sum:')
# distributed = a_mul.distribute()
# print(distributed, '\n')
# print('commute each inner mul:')
# commuted = distributed.commute_terms()
# print(commuted, '\n')
# print('distribute term over sum:')
# re_distributed = commuted.distribute_terms()
# print(re_distributed, '\n')
# print('de associate inner sums:')
# de_associated = re_distributed.de_associate()
# print(de_associated, '\n')
# print('apply mul to terms:')
# applied_muls = de_associated.apply_muls()
# print(applied_muls, '\n')
# print('aggregate like terms:')
# aggregated_terms = applied_muls.aggregate()
# print(aggregated_terms, '\n')
# print('evaluate final sum of terms:')
# print(aggregated_terms.evaluate())