''' 
adapted from https://oeis.org/ 
'''

from sympy import totient, gcd

from math import gcd as bltin_gcd

def coprime2(a, b):
    return bltin_gcd(a, b) == 1

def primfac(n):
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
       primfac.append(n)
    return primfac

def A020653(n):
    """
	Denominators in a certain bijection from positive integers to positive rationals.

    Parameters
    ----------
    n : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    s=0
    k=2

    while s<n:
        s+=totient(k)
        k+=1
    s-=totient(k - 1)
    j=1

    while s<n:
        if gcd(j, k - 1)==1: s+=1
        j+=1

    return k - j

def A038566(n):
    """
    Numerators in canonical bijection from positive integers to positive rationals <= 1: arrange fractions by increasing denominator then by increasing numerator.

    Parameters
    ----------
    n : TYPE
        DESCRIPTION.

    Returns
    -------
    arow : TYPE
        DESCRIPTION.

    """

    if n == 1: return 1
    
    arow = []
    for k in range(n):
        if coprime2(k, n):
            arow.append(k)
    return arow

# def A038566_flat(n):
#     j = 2
#     idx = 1
#     a = A038566(j)
#     while idx != n:
#         idx = idx + 1
#         if len(a) <= idx:
#             a = a + A038566(j)
#             j = j + 1
#         k = a[idx]
#     return k

def A038567(n):
    """
    Denominators in canonical bijection from positive integers to positive rationals <= 1.

    Parameters
    ----------
    n : TYPE
        DESCRIPTION.

    Returns
    -------
    s : TYPE
        DESCRIPTION.

    """

    s=1

    while sum(totient(i) for i in range(1, s + 1))<n: s+=1

    return s

if __name__ == '__main__':
    
    # for k in range(50):
    #     print("{}/{}".format(A038566(k), k))
        
    # for d in range(2,20):
    #     numerators = A038566(d)
    #     for j, nr in enumerate(numerators):
    #         print(f"{nr}/{d}")
    
    for d in range(2,20):
        numerators = A038566(d)
        for j, nr in enumerate(numerators):
            facn = primfac(nr)
            facd = primfac(d)
            
            if nr == 1:
                facn = [1]
    
            facnsl = list(map(str, facn))
            facdsl = list(map(str, facd))
    
            facns = '*'.join(facnsl)
            facds = '*'.join(facdsl)
            
            maxprimen = max(facn)
            maxprimed = max(facd)
            maxprime = max((maxprimen, maxprimed))
            # print(f"{nr}/{d}" + '\t\t' + facns + '/' + facds + '\t\t'
            #       + str(maxprimen) + '\t\t' + str(maxprimed) + '\t\t'
            #       + str(maxprime))
            # print(f"{nr}/{d} {facn}/{facd} {maxprimen} {maxprimed} {maxprime}")
            print(f"{nr:>4}/{d:<4} {facns:>10}/{facds:<10} {maxprimen:<5} {maxprimed:<5} {maxprime}")
            
    