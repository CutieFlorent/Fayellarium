from sympy import *

EDO = 31

primes = [2, 3, 5, 7, 11, 13, 17, 19]
mapping = [round(log(i, 2) * EDO) for i in primes]
mapping_dict = {p: m for p, m in zip(primes, mapping)}


def steps(n, d):
    n, d = (lambda n: (n.numerator, n.denominator)) \
        (Rational(n, d))  # reduction
    res = 0
    # formula = ''
    n_dict, d_dict = (lambda f: (f(n), f(d))) \
        (factorint)  # prime dict for n and d
    for i in n_dict:
        if i > 19: return None
        res += mapping_dict[i] * n_dict[i]
        # formula += f'+ {mapping_dict[i]}*{n_dict[i]} '
        # steps of the prime * power of the prime
    for i in d_dict:
        if i > 19: return None
        res -= mapping_dict[i] * d_dict[i]
        # formula += f'- {mapping_dict[i]}*{d_dict[i]} '
        # steps of the prime * power of the prime
    # formula += f'= {res}'
    # if res<0 :print(formula)
    return res


neg_intervals = []
MAX_D = 3000

for d in range(2, MAX_D + 1):
    for n in range(d, round(d * (9 / 8))):
        s = steps(n, d)
        if s is None: continue
        if s < 0:
            # print(f'{n}/{d}', s)
            neg_intervals.append((n, d, s))

print(f'{EDO = }')
print(f'mapping: {mapping}')

for n, d, s in neg_intervals:
    print(f'{n}/{d} {s}', end='\t')
