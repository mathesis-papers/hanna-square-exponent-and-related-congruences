import argparse
from fractions import Fraction
import hashlib
import json
from math import comb, factorial, isqrt
from pathlib import Path


def sigma_power(number):
    return sum(divisor ** number for divisor in range(1, number + 1)
               if number % divisor == 0)


def sparse_terms(kind, limit):
    terms = []
    for index in range(1, limit + 1):
        degree = index * (index + 1) // 2 if kind == 'triangular' else index ** 2
        if degree > limit:
            break
        denominator = factorial(index) if kind == 'triangular' else index ** index
        numerator = sigma_power(index) if kind == 'weighted' else 1
        terms.append((degree, Fraction(numerator, denominator)))
    return terms


def integral_recurrence(terms, limit):
    normalized = []
    for degree, coefficient in terms:
        value = factorial(degree) * coefficient
        if value.denominator != 1:
            raise ValueError('Nonintegral normalized inner coefficient')
        normalized.append((degree, value.numerator))
    sequence = [1]
    for degree in range(1, limit + 1):
        value = sum(comb(degree - 1, support - 1) * coefficient
                    * sequence[degree - support]
                    for support, coefficient in normalized if support <= degree)
        sequence.append(value)
    return sequence


def rational_product(terms, limit):
    polynomial = [Fraction(1)] + [Fraction(0)] * limit
    for degree, coefficient in terms:
        factor = [(0, Fraction(1))]
        current = Fraction(1)
        for multiplicity in range(1, limit // degree + 1):
            current *= coefficient / multiplicity
            factor.append((degree * multiplicity, current))
        updated = [Fraction(0)] * (limit + 1)
        for offset, value in factor:
            for position in range(limit - offset + 1):
                updated[position + offset] += polynomial[position] * value
        polynomial = updated
    return [coefficient * factorial(degree)
            for degree, coefficient in enumerate(polynomial)]


def valuation(number, prime):
    exponent = 0
    while number % prime == 0:
        number //= prime
        exponent += 1
    return exponent


def exact_divisibility_checks(limit):
    factorials = [factorial(degree) for degree in range(limit + 1)]
    for index in range(2, isqrt(limit) + 1):
        quotient, remainder = divmod(factorials[index ** 2], index ** index)
        if remainder or quotient % 6:
            raise ValueError('Square factorial divisibility failed')
        if index >= 3 and quotient % 30:
            raise ValueError('Stronger square factorial divisibility failed')
    expected = {3: [7, 1, 1], 4: [7, 6, 3], 5: [22, 10, 1]}
    for index, row in expected.items():
        quotient = factorial(index ** 2) // index ** index
        if [valuation(quotient, prime) for prime in [2, 3, 5]] != row:
            raise ValueError('Valuation table failed')
    return expected


def sequence_digest(sequence):
    digest = hashlib.sha256()
    for value in sequence:
        data = value.to_bytes(max(1, (value.bit_length() + 7) // 8), 'big')
        digest.update(len(data).to_bytes(8, 'big'))
        digest.update(data)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    limit = 1024
    product_limit = 80
    expected_prefixes = {
        'square': [1, 1, 1, 1, 7, 31, 91, 211, 1681, 25537, 192361,
                   949081, 4830871, 85109311, 951416467, 6696998491,
                   119863554721, 0x1d2a7f31081, 0x170d1183f651,
                   0xd86aec60f1b1, 0xe9fde46f70f27, 0xe7f104f4cc54df,
                   0xc8b4055aa3f3ccb, 0x8c9debeb69dbb063,
                   0x8f6f3b09ad43b8731, 0x2152f7986b9faa5b541],
        'triangular': [1, 1, 1, 4, 13, 31, 271, 1576, 6049, 55693,
                       573661, 3839716, 36369301, 432793219, 3670898323,
                       47260464616, 758854978561, 0x76426d4e0b9,
                       0x60ab9a693159, 0x630cadd230164, 0x519f2f451aad3d,
                       0x64e6f5912828d67, 0x76150ce9ffa69f57,
                       0x68329733a11664988, 0x7f33470b120c7a9561],
        'weighted': [1, 1, 1, 1, 31, 151, 451, 1051, 33601, 663601,
                     5187001, 25905001, 254322751, 10408719751,
                     128046088171, 920598820051, 0x1a9a294acf81,
                     0x2925626b756e1, 0x2c334a8e0a4d71,
                     0x1ec66c96df92a51, 0x3d27877d0a7b32df,
                     0x510ede99ec45df977, 0x68c980e98831dbd193,
                     0x5e0021225c0a100b78b],
    }
    records = []
    for kind, modulus, identifier in [('square', 6, 'A226838'),
                                       ('triangular', 3, 'A226839'),
                                       ('weighted', 30, 'A226890')]:
        sequence = integral_recurrence(sparse_terms(kind, limit), limit)
        if any((value - 1) % modulus for value in sequence):
            raise ValueError(f'{identifier} congruence failed')
        prefix = expected_prefixes[kind]
        if sequence[:len(prefix)] != prefix:
            raise ValueError(f'{identifier} source prefix failed')
        rational = rational_product(sparse_terms(kind, product_limit), product_limit)
        if rational != sequence[:product_limit + 1]:
            raise ValueError(f'{identifier} rational expansion failed')
        records.append({'oeis': identifier, 'modulus': modulus,
                        'integer_recurrence_indices': [0, limit],
                        'rational_product_indices': [0, product_limit],
                        'source_prefix_terms': len(prefix),
                        'initial_eight_terms': sequence[:8],
                        'sequence_sha256': sequence_digest(sequence),
                        'status': 'pass'})
    special = exact_divisibility_checks(limit)
    result = {'arithmetic': 'exact Python integers and fractions.Fraction',
              'scope': 'Finite coefficient identities and congruences; all-index proofs are in note.tex.',
              'sequences': records,
              'factorial_square_indices': [2, isqrt(limit)],
              'valuation_table': special,
              'optimal_moduli_witnesses': {'A226838': [4, 7],
                                         'A226839': [3, 4],
                                         'A226890': [4, 31]},
              'status': 'pass'}
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
