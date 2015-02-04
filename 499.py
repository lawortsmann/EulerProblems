# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 15:08:18 2015

A quasi-Monte Carlo simulation to find the probability of a finite number of
games in the St. Petersburg Lottery given cost M and initial wealth W0.

NOTE:
does not work

@author: Lawortsmann
"""

from itertools import product

MAXK = 4
M = 2.0
W0 = 2.0
NETPROB = sum([2**(-(n+1)) for n in xrange(MAXK)])

def pospay(zpoint, winlist):
    winnings = 0
    for k, i in enumerate(winlist):
        payim = i * ((2**(k + zpoint)) - M)
        winnings += payim
    return winnings

def payoff(gameset):
    winnings = 0
    for k, i in enumerate(gameset):
        payim = i * ((2**(k)) - M)
        winnings += payim
    return winnings

def totalprob(winlist):
    prob = 1
    for n,val in enumerate(winlist):
        prob0 = ((2**(-(n+1)))/NETPROB)**val
        prob = prob*prob0
    return prob
            
def findzero(M):
    k = 0
    while (2**k)-M < 0:
        k += 1
    return k
    
zeroPoint = findzero(M)

sampleArray = [range(1+2**((MAXK-zeroPoint-1) - k)) for k in xrange((MAXK-zeroPoint))]
combos = list(product(*sampleArray))
zeroPoint = findzero(M)

pospayofflist = []
for poslist in combos:
    impay = pospay(zeroPoint, poslist)
    pospayofflist.append(impay+M)

uniquevals = [val for val in list(set(pospayofflist))]

maxlist = [-(W0+max(uniquevals)-M)/(2**(val) - M) for val in xrange(zeroPoint)]

negposArray = []
for val in maxlist:
    negposArray.append(range(int(val)))
negcombos = list(product(*negposArray))

matches = []
for val1 in negcombos:
    for val2 in combos:
        matches.append(val1+val2)

totalmovelist = map(sum,matches)
probConverge = {}
for n,move1 in enumerate(totalmovelist):
    compareset = zip(*[totalmovelist[:n]+totalmovelist[n+1:],matches[:n]+matches[n+1:]])
    for move2 in compareset:
        if move1+1 == move2[0] and W0 + payoff(matches[n]) >= M and W0 + payoff(move2[1]) < M:
            gamelength = sum(move2[1])
            try:
                probConverge[gamelength] += totalprob(move2[1])
            except KeyError:
                probConverge[gamelength] = totalprob(move2[1])
            
print probConverge