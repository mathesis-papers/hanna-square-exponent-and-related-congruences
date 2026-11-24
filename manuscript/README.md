# Hanna's square-exponent congruence and divisor-sum companions

`note.tex` is the main LaTeX source; its bibliography is embedded. `note.pdf`
is the readable note. The author order is Haobo Ma, then Wenlin Zhang.
The note and accompanying original explanatory material are licensed
CC BY 4.0 (`cc-by-4.0`).

## Build

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, run `pdflatex note.tex` twice with the standard packages
`geometry`, `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`, `fontenc`,
`lmodern`, and `hyperref` installed. No external bibliography tool, figures,
or data files are required.

## Exact finite checks

Python 3.10 or later and its standard library suffice:

```sh
python3 verify.py --output verification.json
python3 sibling-checks.py --output sibling-verification.json
```

The script checks A226838 modulo six, A226839 modulo three, and A226890
modulo thirty for indices 0 through 1024. It compares the integer recurrence
with a separate rational product-of-exponentials expansion through index 80,
compares every listed OEIS initial term, and checks the factorial-divisibility
and valuation calculations. These are finite checks, complementary to the
all-index written proofs in the note. It prints compact summaries, not large
integer tables. `verification.json` is the corresponding exact output.
Each sequence digest hashes its nonnegative terms in order, each term encoded
as minimal big-endian unsigned bytes preceded by its eight-byte big-endian
length; zero uses one zero byte.

## Mathematical sources and formal scope

- Paul D. Hanna, OEIS A226838, revision 14, FORMULA and COMMENTS:
  <https://oeis.org/A226838>.
- Paul D. Hanna, OEIS A226839, revision 11, FORMULA and COMMENTS:
  <https://oeis.org/A226839>.
- Paul D. Hanna, OEIS A226890, revision 5, FORMULA:
  <https://oeis.org/A226890>.
- The declaration `HannaA226838Congruence.result` proves the rational coefficient
  equality with an integer residue witness, for all natural indices:
  <https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S1/Recurrence/Residue/HannaA226838Congruence.lean>.
- The declaration `HannaA226839Congruence.result` proves the corresponding
  modulo-three equality for the triangular-exponent series:
  <https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S1/Recurrence/Residue/HannaA226839Congruence.lean>.

The general integral transfer lemma, integer-weighted square extensions,
modulo-thirty result, optimality witnesses, and identities at one are covered
by the written proofs. The Lean declaration links cover the two specifically
identified rational series, not these additional statements.

## Further mathematical coverage

The exponential coefficient recurrence is classical: L. Carlitz,
"Some congruences for the Bell polynomials", Pacific Journal of Mathematics
11(4) (1961), 1215–1222, Section 2, equations (2.1)–(2.2), page 1216:
<https://doi.org/10.2140/pjm.1961.11.1215>.
The arithmetic applications here use the explicitly proved factorial divisibilities.

The transfer criterion is necessary and sufficient. For arbitrary integer
linear coefficient and square weights, congruence modulo thirty holds at every
index exactly when the degree-four weight is divisible by five.

The linked A023887 formulas have written proofs: prime-power factorization,
parity, its ordinary generating function, its normalized logarithmic derivative,
and the asymptotic bound `1 <= sigma_n(n)/n^n <= 1+n/2^n`.
Yanev's radical identity holds for every positive exponent; exponent two is
Sela Fried's earlier Theorem 3 (2025), page 3:
<https://oeis.org/A001157/a001157.pdf>.
The declaration `YanevSigmaRadicalIdentity.result` proves its multiplied-out
natural-number form for positive arguments:
<https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Arith/YanevSigmaRadicalIdentity.lean>.
The quotient form follows because the ordinary divisor-sum denominator is positive.
The separate assertion that 5 is the only prime in A023887 is not covered.

`sibling-checks.py` checks 1024 positive argument/exponent pairs for the radical
identity, divisor parity and the asymptotic bound through 512, 25 signed-weight
examples through degree 64 with rational comparisons through degree 24,
three transfer-gcd examples through degree 32, and the partition and expanding
product identities through degree 24. These are exact finite checks;
`sibling-verification.json` records the ranges.
