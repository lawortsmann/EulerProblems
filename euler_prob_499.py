# coding: utf-8

"""
Created on Mon Feb 17 17:29:12 2015

A simulation to generate statistics of a probability distribution of winning,
in a attempt to solve Project Euler 499. The St. Petersburg Lottery.

@author: Luke_Wortsmann
"""

from random import random
from numpy import histogram
import csv
from time import time


costPerRound = 15

# The following two blocks of code are the basis for the monte-carlo simulation,
# they provide for an efficient way to build a random sample.

# First, generate a PMF of the probability distribution

probabilitySet = []
payoutSet = []
probability = 1
k = 1
while probability != 0:
    probability = 2**(-k)
    payOut = 2**(k - 1) - costPerRound
    k += 1
    probabilitySet.append(probability)
    payoutSet.append(payOut)

# Then, define a function that returns payout for one game of the lottery

def selectF():
    rand = random()
    i = 0
    val = probabilitySet[i]
    while (rand - val) < 0:
        i += 1
        val = probabilitySet[i]
    return payoutSet[i]

# Function to generate statitics to build a probability distribution from a
# set of values created through simulation.

def calculateStats(valueSet):
    histData = histogram(valueSet, bins = 100)
    transformedData = zip(*map(list, histData))
    return transformedData

# Run simulation for n trials, only playing up to a maximum of maxGames games.
# Return the minimum value of your winnings in a set of games and add it to valueSet.
# Pass valueSet to calculateStats and return result.

def runSimulation(maxGames):
    trials = 10000000/maxGames
    valueSet = []

    for i in xrange(trials):
        summation = 0
        minValue = 0
        for _ in xrange(maxGames):
            summation += selectF()
            if summation < minValue:
                minValue = summation
        valueSet.append(minValue)

    return calculateStats(valueSet)

# Run simulation while writing to a .csv

with open('/Users/Lawortsmann/Desktop/CS_196/499/statData0.csv', 'wb') as csvfile:
    dataWriter = csv.writer(csvfile)
    for g in xrange(100):
        maxGames = (g+1)*1000
        simulationData = runSimulation(maxGames)
        dataWriter.writerow([maxGames])
        for point in simulationData:
            dataWriter.writerow(point[::-1])
        print 'Done with %s out of 100.'%(g+1)
