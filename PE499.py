# -*- coding: utf-8 -*-
# PE499.py
"""
Solution to Project Euler 499

@version: 07.15.2016
@author: LukeWortsmann
"""
import numpy as np
from scipy.optimize import brentq


def PE499(m, s, tol=1e-50):
    """
    Fast and stable solution to Project Euler 499. Runtime effectively O(1).
    Given intial weath 's' and cost per game 'm', what is the probability game
    continues forever? Using a generalized gambler's ruin probability, see:
    http://arxiv.org/abs/1209.4203v4 and http://projecteuler.net/problem=499

    Parameters
    ----------
    m : number
        cost per game
    s : number
        initial wealth
    tol : number
        working tolerance

    Returns
    -------
    p : float
        probability game continues indefinitely
    """
    # Precompute P.G.F. for root finding
    i = np.arange(1, 2 * int(-np.log2(tol)), dtype=np.float128)
    p = np.power(2, -i)
    w = np.power(2, i) / m
    # Find P.G.F. root: z^2 = phi(z)
    z = brentq(lambda z: (z * z) - np.sum(p * np.power(z, w)), tol, 1, xtol=tol)
    # Compute solution:
    return 1 - np.power(z, (2 * s / m) - 1)


if __name__ == '__main__':
    print '====  SOLUTIONS  ===='
    print 'p_2(2) =    ', round(PE499(2, 2), 7)
    print 'p_2(5) =    ', round(PE499(2, 5), 7)
    print 'p_6(10000) =', round(PE499(6, 10000), 7)
    print 'p_15(1e9) = ', round(PE499(15, 1e9), 7)
