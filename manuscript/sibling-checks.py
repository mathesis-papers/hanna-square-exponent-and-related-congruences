import argparse
from fractions import Fraction
from functools import reduce
import json
from math import factorial, gcd, isqrt
from pathlib import Path
from verify import integral_recurrence, rational_product, sigma_power


def divisors(number):
    return [divisor for divisor in range(1, number + 1) if number % divisor == 0]


def radical(number):
    remaining = number
    result = 1
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            result *= prime
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    return result * remaining


def radical_numerator_from_factors(number, exponent):
    remaining = number
    result = 1
    prime = 2
    while prime * prime <= remaining:
        power = 0
        while remaining % prime == 0:
            remaining //= prime
            power += 1
        if power:
            length = exponent * power + exponent
            result *= (prime ** length - 1) // (prime - 1)
        prime += 1
    if remaining > 1:
        result *= (remaining ** (2 * exponent) - 1) // (remaining - 1)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    pairs = 0
    for number in range(1, 129):
        root = radical(number)
        for exponent in range(1, 9):
            left = sum(divisor ** exponent for divisor in divisors(number))
            denominator = 1
            for prime in divisors(root):
                if prime > 1 and all(prime % candidate for candidate in range(2, isqrt(prime) + 1)):
                    denominator *= sum(prime ** power for power in range(exponent))
            numerator = radical_numerator_from_factors(number, exponent)
            assert left * denominator == numerator
            pairs += 1
    for number in range(1, 513):
        value = sigma_power(number)
        square_or_twice_square = isqrt(number) ** 2 == number or (
            number % 2 == 0 and isqrt(number // 2) ** 2 == number // 2)
        assert bool(value % 2) == square_or_twice_square
        assert 0 <= (value - number ** number) * 2 ** number <= number ** (number + 1)
        geometric_coefficient = sum(divisor ** number for divisor in divisors(number))
        assert geometric_coefficient == value
    examples = 0
    for linear in [-3, -1, 0, 1, 2]:
        for second in [-5, -1, 0, 2, 5]:
            terms = [(1, Fraction(linear)), (4, Fraction(second, 4))]
            terms += [(index ** 2, Fraction((-1) ** index * (index + 2), index ** index))
                      for index in range(3, 9)]
            sequence = integral_recurrence(terms, 64)
            assert all((value - linear ** index) % 6 == 0 for index, value in enumerate(sequence))
            assert all((value - linear ** index) % 30 == 0
                       for index, value in enumerate(sequence)) == (second % 5 == 0)
            assert rational_product([(degree, value) for degree, value in terms if degree <= 24], 24) == sequence[:25]
            examples += 1
    for linear in [-2, 0, 3]:
        inner = [linear] + [6 * ((degree * degree + 3 * degree) % 11 - 5) for degree in range(2, 33)]
        terms = [(degree, Fraction(value, factorial(degree)))
                 for degree, value in enumerate(inner, start=1)]
        sequence = integral_recurrence(terms, 32)
        assert reduce(gcd, inner[1:], 0) == reduce(
            gcd, [value - linear ** index for index, value in enumerate(sequence)][2:], 0)
    limit = 24
    sigma = [0] + [sum(divisors(number)) for number in range(1, limit + 1)]
    partitions = [1] + [0] * limit
    for part in range(1, limit + 1):
        for number in range(part, limit + 1):
            partitions[number] += partitions[number - part]
    for number in range(1, limit + 1):
        assert number * partitions[number] == sum(
            sigma[degree] * partitions[number - degree] for degree in range(1, number + 1))
    expanding = [Fraction(1)]
    for number in range(1, limit + 1):
        expanding.append(sum(sigma_power(degree) * expanding[number - degree]
                             for degree in range(1, number + 1)) / number)
    product = [Fraction(1)] + [Fraction(0)] * limit
    for degree in range(1, limit + 1):
        coefficients = [Fraction(1)]
        for multiplicity in range(1, limit // degree + 1):
            coefficients.append(coefficients[-1] * (Fraction(1, degree) + multiplicity - 1)
                                * degree ** degree / multiplicity)
        updated = [Fraction(0)] * (limit + 1)
        for multiplicity, coefficient in enumerate(coefficients):
            for position in range(limit - multiplicity * degree + 1):
                updated[position + multiplicity * degree] += product[position] * coefficient
        product = updated
    assert product == expanding
    assert expanding[:12] == [1, 1, 3, 12, 82, 725, 8811, 128340, 2257687,
                              45658174, 1052672116, 27108596725]
    result = {'status': 'pass', 'arithmetic': 'exact integers and fractions.Fraction',
              'scope': 'Finite identities and examples; all-index statements have written proofs in note.tex.',
              'radical_identity': {'n': [1, 128], 'r': [1, 8], 'pairs': pairs},
              'divisor_parity_and_asymptotic_bound': {'n': [1, 512]},
              'weighted_square_examples': {'linear_coefficients': [-3, -1, 0, 1, 2],
                  'second_weights': [-5, -1, 0, 2, 5], 'examples': examples,
                  'integer_recurrence_indices': [0, 64], 'rational_product_indices': [0, 24]},
              'transfer_gcd_examples': {'linear_coefficients': [-2, 0, 3], 'indices': [0, 32]},
              'partition_and_expanding_product': {'indices': [0, limit], 'A023881_prefix_terms': 12}}
    text = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
