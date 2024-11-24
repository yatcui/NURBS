"""Support for B-Splines

    Author:
        Wolfgang Funk <wofunk@web.de>
        
"""

def bspline_basis(p, U, i, u):
    """Computation of B-Spline basis function value at a parameter value.

    Straight-forward implementation of OneBasisFun from
    The NURBS Book, 1st ed., p. 74 f.
    
    Example:
        # Calculate B-Spline basis of degree 7 for 4th segment at u = 0.43.
        # This is effectively a Bezier curve (only multiple end knots).
        p = 7
        U = [0.]*8 + [1.]*8
        i = 3
        u = 0.43
        bu = bspline_basis(p, U, i, u)
    
    Args:
        p (int): Degree of basis function.
        U (list of float): Knot vector.
        i (int): Segment to calculate basis function for (zero-indexed)
        u (float): Parameter value to calculate basis function value for.
        
    Returns:
        float: basis function value.

    """
    m = len(U) - 1
    # Special cases
    if (i == 0 and u == U[0]) or (i == m-p-1 and u == U[m]):
        return 1.
    if u < U[i] or u >= U[i+p+1]:
        return 0.
    N = []
    # Initialize zeroth-degree functions
    for j in range(p+1):
        if u >= U[i+j] and u < U[i+j+1]:
            N.append(1.)
        else:
            N.append(0.)
    # Compute triangular table
    for k in range(1, p+1):
        if N[0] == 0.:
            saved = 0.
        else:
            saved = ((u-U[i]) * N[0]) / (U[i+k]-U[i])
        for j in range(p-k+1):
            U_left = U[i+j+1]
            U_right = U[i+j+k+1]
            if N[j+1] == 0.:
                N[j] = saved
                saved = 0.
            else:
                temp = N[j+1] / (U_right - U_left)
                N[j] = saved + (U_right-u) * temp
                saved = (u-U_left) * temp
    return N[0]


if __name__ == "__main__":
    p = 7
    U = [0.]*8 + [1.]*8
    i = 3
    u = 0.43
    bu = bspline_basis(p, U, i, u)
    
    q = 5
    V = [0.]*6 + [1.]*6
    k = 1
    v = 0.19
    bv = bspline_basis(q, V, k, v)
    
    buv = bu * bv
    print(f"Knots in U: {U}")
    print(f"Knots in V: {V}")
    print(f"Degree in u, v: {p}, {q}")
    print(f"u, v = {u}, {v}")
    print()
    print(f"N_{i},{k}({u}, {v}) = {buv:.6f}")
