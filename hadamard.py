"""Hadamard.py - May 31 2022 by M.F.Hasler

SYNOPSIS: Provide functions Hadamard(n) and Jacobsthal(n)
    which return an n x n Hadamard resp. Jacobsthal matrix.
    Uses the Paley construction of Hadamard matrices of size (q+1)*2^k
    for prime powers q (k > 0 if q == 1 mod 4).
    cf. https://en.wikipedia.org/wiki/Paley_construction

Remarks:
    A Hadamard matrix of size n is an n x n matrix with entries in {+-1}
    such that distinct rows and distinct columns are pairwise orthogonal.

    It is known they exist for n = 1, 2, 4k.
    It is clear they can't exist for n = 2k+1, nor for n = 2(2k+1), k > 0:
        WLOG one can assume one row = 1...1.
        To be orthogonal, any other row must have n/2 '1's and n/2 '-1's,
        so n must be even. If n = 2(2k+1),
        assume the second row has 2k+1 '1's followed by 2k+1 '-1's.
        If the the first 2k+1 elements of the 3rd row sum to m (necessarily odd)
        the other 2k+1 elements must sum to -m to be orthogonal to the 1st row.
        But then the scalar product with the 2nd row is 2m.
    There is the simple Sylvester's construction of H.matrices of size 2^k:
    If H(n) is a Hadamard matrix of size n, e.g., H(1) = [1], then
    H(2n) = [ H(n)  H(n) ]
            [ H(n) -H(n) ]  is a Hadamard matrix of size 2n.

    Paley's construction fills gaps for n = q+1 where q is the power of a prime.
    Let Q be the Jacobsthal matrix for GF(q): Q[i,j] = chi(i - j) where i, j are
    the i-th and j-th element of GF(q) (see below), and the quadratic character 
    chi(0) = 0, chi(x²) = 1 and chi(x) = -1 is x isn't a square in GF(q).
    NOTE: When q is a prime, one can simply use integers i, j and check whether i-j
    is a square in Z/qZ. But if q is not a prime, one must use arithmetics in GF(q)!
    If q == 3 (mod 4), let  H(q+1) = I + [ 0  U ]  where U = [1]*q.
                                         [-U' Q ]  a skew Hadamar matrix: H + H' = 2I.
    If q == 1 (mod 4), H(2q+2) = [0, U; U', Q] (x) H(2) + I (x) [1, -1; -1, -1],
    i.e., replace the '1's (resp. '-1's) in the first expression by 2x2 matrices
    H(2) (resp. -H(2)), and the zeros on the diagonal by  [1, -1; -1, -1].
"""
import numpy as np
import math
#from np.polynomial import Polynomial # don't use this
#issquare = lambda n: math.isqrt(n)**2==n

def isprime(n):
    "Return True if n is a prime number, False otherwise."
    if not n & 1: return n == 2
    if n < 9: return n > 1
    return all(n%p for p in range(3, math.isqrt(n)+1, 2))

def isprimepower(n):
    """Return a truthy value if n is the power of a prime, or False if not.
    Specifically, if n = p^k, this returns the smallest prime factor of k."""
    if isprime(n): return True
    for k in range(2,n):
        if not n >> k: return False
        if isprime(k) and n == (r := round(n**(1/k)))**k and isprimepower(r):
            return k
# list(filter(isprimepower,range(30))) # works!

def Jacobsthal(q):
    """Return Jacobsthal matrix of size q, J[i,j] = chi(i-j) with quadratic
    character of GF(q): chi(0) = 0, chi(x²) = 1 and chi(x) = -1 otherwise.
    Here  x in GF(q): when q = p^k with k > 1, one cannot just take x in Z/qZ.
    For q = 2^k, J = U - I, where  I = np.eye(q), U = np.ones(q,q).
    For odd q, J has zero row & column sums and  J * J.T = q.I + U."""
    if isprime(q):
        squares = {k*k % q for k in range(1,q//2+1)}
        issquare = lambda x,y: (x-y)%q in squares 
    elif isprimepower(q):
        import galois  # heavy artillery, but tedious to implement by hand
        GF = galois.GF(q)
        issquare = lambda x,y: (GF(x)-GF(y)).is_quadratic_residue()
    elif q < 2:
        return np.zeros((q,q),int)
    else:
        raise ValueError(f"q = {q} is not a prime power as required.")
    return np.matrix([[0 if i==j else 1 if issquare(i,j) else -1
                       for j in range(q)] for i in range(q)])

def Hadamard(n):
    """Return Hadamard matrix of size n."""
    if n < 3:
        return np.matrix('1,1;1,-1'if n>1 else 1)

    # odd or == 2 (mod 4) : impossible
    if n % 4:
        raise ValueError("Can't make Hadamard matrix of this size.")

    # if n = q+1 where  q == 3 + 4k is a prime power
    if isprimepower(n-1):
        if getattr(Hadamard,'debug',0):
            print(f"Using Jacobsthal matrix of size {n-1} (n = 3 mod 4).")
        Q = Jacobsthal(n-1) + np.eye(n-1, dtype=int)
        return np.vstack([[1]*n, np.vstack([[-1]*(n-1), Q.T]).T])
    
    # if n = 2q+2 = 2(q+1) where q == 1 + 4k is a prime power
    if n % 8 == 4 and isprimepower(n//2-1): # n = 2q + 2
        if getattr(Hadamard,'debug',0):
            print(f"Using Jacobsthal matrix of size {n//2-1} (n = 1 mod 4).")
        Q = Jacobsthal(n//2-1)
        H = Hadamard(2); M = -H; D = np.matrix('1,-1;-1,-1')
        return np.block([[D if r==c else H if r==0 or c==0 or Q[r-1,c-1]>0
                          else M for c in range(n//2)] for r in range(n//2)])
    try:
        H = Hadamard(n >> 1)
        return np.block([[H,H],[H,-H]])
    except:
        raise ValueError("Can only make Hadamard matrix of size "
                         f"n = (prime power + 1) x 2^k, got n = {n}.")

def check_Hadamard(n):
    """Return 1 if there exists a Hadamard matrix of size n."""
    if n < 3: return 1
    # odd or == 2 (mod 4) : impossible
    if n % 4: return 0
    if isprimepower(n-1): return 1
    if n % 8 == 4 and isprimepower(n//2-1): # n = 2q + 2
        return 1
    return check_Hadamard(n >> 1)

if __name__=='__main__1': # Hadamard test
    Hadamard.debug = 1
    for n in range(20):
        H = Hadamard(n*4)
        if (H*H.T - np.diag([n*4]*(n*4))).any():
            print("BAD for",n)
    # this gives BAD for n = 7, 13, 14, with "naive" implementation.
    # NO BAD using galois
    print("Done up to",n)

if __name__=='__main__2': # Hadamard test 2
   for n in range(99):
  	 if not check_Hadamard(n*4): print(n,end=", ")
   # output:
   # 23, 29, 39, 43, 46, 47, 58, 59, 65, 67, 73, 81, 89, 93, 94,
    
if __name__=='__main__2': # Jacobsthal test
    for n in range(30):
        try:
            J = Jacobsthal(n)
            # check the relation Q*Q.T = q I - U
            # valid only for odd prime powers. 
            if (J*J.T - n*np.eye(n) + np.ones((n,n))).any():
                print("BAD for",n)
        except ValueError as e:
            print(e)
    # this gives BAD for all even n > 0.
    print("Done up to",n)

