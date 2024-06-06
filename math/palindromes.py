''' palindromes.py - (c) 12 May 2024 by MFH

OEIS references:
  A002113		Palindromes in base 10.

TO DO:
  - add code for the n-th palindrome, cf. OEIS.
  - 
Explanations:
  The palindromes come in groups of given length:
  group 0 = { A2113(1) = 0 }, 1 element.
  group 1 = { A2113(2) = 1 .. A2113(10) = 9,
              A2113(11) = 11 .. A2113(19) = 99 } : 2 x 9 terms with stem 1..9, 
  group 2 = { A2113(20) = 101 .. A2113(109) = 999,
              A2113(110) = 1001 .. A2113(199) = 9999 } : 2 x 90 terms with stem 10..99,
            indices n = 20 .. 1 + 99*2,
  group 3 = { A2113(200) = 10001 .. A2113(1099) = 99999,
              A2113(1100) = 100001 .. A2113(1999) = 999999 }: 2 x 900 terms with stem 100..999, 
            indices 200 .. 1 + 999*2), ...
  We see that each integer n > 0 corresponds to two palindromes, of which it is the first half
  (including the middle digit in case of odd number of digits in the palindrome).
  So, dividing the index  n  by 2 tells us in which group it is (length of the stem):
  G = floor(log_10(n/2))+1 = 1 for 1 up to 99,
    = 2 for 101 - 9999,    = 3 for 10001 - 999_999,  etc.
  The index of the first palindrome in a given group G is 2*10^(G-1), except for 0.
  If we subtract that index from the index of the given palindrome, 
  we get the relative index of the palindrome in its group (starting at 0).
  It is in the second half (even number of digits) iff n >= 1.1*10^G.
'''
from math import log10
def A002113(n):
  if n < 2: return 0
  P = 10**int(log10(n//2)); M = 11*P  # or: floor(...), or: n/2
  s = str(n - (P if n < M else M-P))
  return int(s + s[-2 if n < M else -1::-1])
""" or:
A002113 = lambda n: int((s := str(n - (P if n < 11*(P := 10**int(log10(n/2))) else 10*P)))
                        + s[-2 if n < 11*P else -1::-1]) if n > 1 else 0
"""

def palindromes(max_length = 99, start_length = 0):
    """Generate all palindromes up to max_length, starting with start_length.
    (With start_length = 0 (resp. 1), start with 0 (resp. 1)."""
    if not start_length: yield 0 ; start_length = 1
    for L in range(start_length-1, max_length): # one less than the length
        for i in range(10**(L//2), 10**(L//2+1)):
            s = str(i)
            yield int(s + s[L%2-2::-1])

def is_palindrome(n):
    """Return `True` if n is palindromic (in base 10), `False` otherwise."""
    s = str(n)
    return s == s[::-1]
''' shorter but maybe not faster: (to do: timings)
is_palindrome = lambda n: (n := str(n))==reversed(n)
'''
