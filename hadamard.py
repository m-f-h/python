"""Hadamard.py - May 31 2022 by M.F.Hasler

SYNOPSIS: Provide functions Hadamard(n) and Jacobsthal(n)
    which return an n x n Hadamard resp. Jacobsthal matrix.
    Uses the Paley construction of Hadamard matrices of size (q+1)*2^k
    for prime powers q (k > 0 if q == 1 mod 4).
    cf. https://en.wikipedia.org/wiki/Paley_construction

Remarks:
    A Hadamard matrix of size n is an n × n matrix with entries in {+-1}
    such that any two distinct rows or columns are orthogonal.
    One can multiply any row or column by -1 without changing the Hadamard property.

    It is known they exist only for n = 0, 1, 2, 4k.
    They cannot exist for odd n since the scalar product is a sum of n terms 
        in {+-1} which therefore has the same parity as n, nonzero if odd.
    They can't exist for even n = 4k+2 = 2(2k+1), k > 0, either:
        The set of indices E12 = {m | H[1,i] = H[2,i]} must have exactly
        2k+1 elements, and for m not in E12, H[1,i] = -H[2,i].
        But then, s = Sum(H[1,i]*H[3,i], i in E12) is nonzero since odd,
        Sum(H[1,i]*H[3,i], i not in E12) = -s if orthogonal, but then 
        Sum(H[2,i]*H[3,i], i=1..n) = Sum(H[1,i]*H[3,i], i in E12)
        - Sum(H[1,i]*H[3,i], i not in E12) = s - s' = 2s ≠ 0.
     
    There is Sylvester's simple construction of Hadamard matrices of size 2^k:
    If H(n) is a Hadamard matrix of size n, starting with H(1) = [1], then
    H(2n) = [ H(n)  H(n) ]
            [ H(n) -H(n) ]  is a Hadamard matrix of size 2n.

    Paley's construction fills gaps for n = q+1 where q is the power of a prime.
    Let Q be the Jacobsthal matrix for GF(q): Q[i,j] = chi(i - j) where i, j are
    the i-th and j-th element of GF(q) (see below), and the quadratic character 
    chi(0) = 0, chi(x²) = 1 (x ≠ 0), and chi(x) = -1 is x isn't a square in GF(q).
    NOTE: When q is a prime, one can simply use integers i, j and check whether i-j
    is a square in Z/qZ. But if q is not a prime, one must use arithmetics in GF(q)!
    If q == 3 (mod 4), let  H(q+1) = I + [ 0  U ]  where U = [1]*q = [1,...,1].
                                         [-U' Q ]  a skew Hadamard matrix: H + H' = 2I.
    If q == 1 (mod 4), H(2q+2) = [0, U; U', Q] ⊗ H(2) + I ⊗ [1, -1; -1, -1],
    i.e., replace the '1's (resp. '-1's) in the first expression by 2×2 matrices
    H(2) (resp. -H(2)), and the zeros on the diagonal by  [1, -1; -1, -1].
"""
import numpy as np # for matrices in Jacobsthal and Hadamard

# Define simple helper function isprime & isprimepower if not defined.
# (Size n is not expected to be huge, so this will do fine.)
if not 'isprime' in vars():
    def isprime(n):
        "Return True if n is a prime number, False otherwise."
        if not n & 1: return n == 2
        if n < 9: return n > 1
        return all(n%p for p in range(3, math.isqrt(n)+1, 2))
    if not 'math' in vars():
        import math # only needed for isqrt above.
if not 'isprimepower' in vars():
    def isprimepower(n):
        """Return a truthy value iff n is the power of a prime, else False.
        If n = (prime)^k, return the smallest prime factor of k or True if k = 1."""
        if isprime(n): return True
        for k in range(2,n):
            if not n >> k: return False
            if isprime(k) and n == (r := round(n**(1/k)))**k and isprimepower(r):
                return k
    #assert list(filter(isprimepower,range(30))) == [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29]

def Jacobsthal(q, **kwargs):
    """Return Jacobsthal matrix of size q x q, where q must be a prime power p^k:
    J[i,j] = chi(i - j), where indices i, j are identified with elements of GF(q), 
    and the quadratic character chi is defined as chi(0) = 0, chi(x) = 1 if x is
    a nonzero square in GF(q), and chi(x) = -1 if x is not a square in GF(q).
    When q = p^k with k > 1, this is not the same as quadratic residues in Z/qZ!
    For odd q, J has zero row & column sums, and  J * J.T = q*I + U.
    For q = 2^k,  chi(x) = 1 if  x ≠ 0.  kwargs are passed to numpy.array."""
    if q < 3 or q & 1 == 0 and q == 1 << (q.bit_length()-1):
        return np.array([[int(i != j) for j in range(q)] 
                                      for i in range(q)], **kwargs)
    if isprime(q):
        squares = {k*k % q for k in range(1,q//2+1)}
        issquare = lambda x,y: (x-y)%q in squares 
    elif isprimepower(q):
        import galois  # heavy artillery, but tedious to implement by hand
        GF = galois.GF(q)
        issquare = lambda x,y: (GF(x)-GF(y)).is_quadratic_residue()
    else:
        raise ValueError(f"q = {q} is not a prime power as required.")
    return np.matrix([[0 if i==j else 1 if issquare(i,j) else -1
                       for j in range(q)] for i in range(q)])

def Hadamard(n, **kwargs):
    """Return Hadamard matrix of size n × n, i.e., a matrix with entries
    in {+-1} such that any two distinct rows or columns are orthogonal.
    This exists only for n = 0, 1, 2, 4k. We construct the matrix using
    the Payley construction when q = n-1 or q = n/2 - 1 is a prime power,
    or else through Sylvester's construction if Hadamard(n/2) exists."""
    if n < 3:
        return np.matrix('1,1;1,-1'if n==2 else 1 if n else [])

    # odd or == 2 (mod 4) : impossible
    if n & 3:
        raise ValueError(f"There is no Hadamard matrix of size n = {n}.")

    # if n = q+1 where  q == 3 + 4k is a prime power
    if isprimepower(n-1):
        if getattr(Hadamard,'debug',0):
            print(f"Using Jacobsthal matrix of size q = {n-1} == 3 (mod 4).")
        Q = Jacobsthal(n-1)
        return np.array([[1 if i==j or i==0 else -1 if j==0 else Q[i-1,j-1] 
                            for j in range(n)] for i in range(n)], **kwargs)
    
    # if n = 2q+2 = 2(q+1) where q == 1 + 4k is a prime power
    if n % 8 == 4 and isprimepower(n//2-1): # n = 2q + 2
        if getattr(Hadamard,'debug',0):
            print(f"Using Jacobsthal matrix of size q = {n//2-1} == 1 (mod 4).")
        Q = Jacobsthal(n//2-1)
        H = Hadamard(2); M = -H; D = np.matrix('1,-1;-1,-1')
        return np.block([[D if r==c else H if r==0 or c==0 or Q[r-1,c-1]>0
                          else M for c in range(n//2)] for r in range(n//2)])
    try:
        H = Hadamard(n >> 1)
        return np.block([[H, H], [H, -H]])
    except:
        raise ValueError("Can only make Hadamard matrix of size "
                         f"n = (prime power + 1) x 2^k, got n = {n}.")

def check_Hadamard(n):
    """Return 1 if we can find a Hadamard matrix of size n."""
    if n < 3: return 1
    # odd or == 2 (mod 4) : impossible
    if n % 4: return 0
    if isprimepower(n-1) or (n % 8 == 4 and isprimepower(n//2-1)):
        return 1
    return check_Hadamard(n >> 1)

if __name__=='__main__: # Hadamard test':
    Hadamard.debug = 1
    for n in range(20):
        H = Hadamard(n*4)
        if (H*H.T - np.diag([n*4]*(n*4))).any():
            print("BAD for",n)
    # this gives BAD for n = 7, 13, 14, with "naive" implementation.
    # no BAD using galois
    print("Done up to",n)

if __name__=='__main__: # Hadamard test 2':
   for n in range(99):
  	 if not check_Hadamard(n*4): print(n,end=", ")
   # output:  (=> n = 23*4 is first where we can't find H(n))
   # 23, 29, 39, 43, 46, 47, 58, 59, 65, 67, 73, 81, 89, 93, 94,
    
if __name__=='__main__: # Jacobsthal test':
    for n in range(30):
        try:
            J = Jacobsthal(n)
            # check the relation Q*Q.T = q I - U
            # valid only for odd prime powers. 
            if (J*J.T - n*np.eye(n) + np.ones((n,n))).any():
            print("J * J' != n I - U  for",n)
            if n == 1 << (n.bit_length()-1):
                print("(but this is normal for n = 2^k !)") # always
        except ValueError as e:
            print(e) # happens for even n not 2^k and odd 15 & 21. 
    print("Done up to",n)

# eof
