# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 01:06:19 2015

@author: Lawortsmann
"""

from operator import itemgetter
from random import randint

def fitness(individual):
    e = 2.71828182845905
    pi = 3.14159265358979
    summate = sum([((e**(float(k)/10000.0))-1) for k in individual])
    fitness = abs(summate - pi)
    return fitness 

class simulation:
    
    def __init__(self, popSize = 100, threadGen = 50, initThreadPop = 100):

        print 'Starting Evolution...'
        
        self.genomeSet = []
        self.popSize = popSize
        self.threadGen = threadGen    
        self.initThreadPop = initThreadPop
        
    def initiateThread(self):
        workingGenome = []  
        
        for _ in xrange(self.popSize):        
            
            generation0 = []
            for _ in xrange(self.initThreadPop):
                genome0 = [randint(1,14200) for _ in xrange(4)]
                generation0.append(genome0)

            generation = 0 
            while generation < self.threadGen:
                initalgenome = genetics()
                for indvgene in generation0:
                    indvfitness = fitness(indvgene)
                    initalgenome.addindiviual([indvfitness, indvgene])
                generation0 = initalgenome.matingalgo()
                generation += 1
                winner = min(initalgenome.phylogenome, key=itemgetter(0))
            workingGenome.append(winner[1])
        
        self.genomeSet.append(workingGenome)
        
    def evolveAlgo(self):
        workingGenome = []
        
        for _ in xrange(self.popSize):
            generation = 0  
            populationGenome = self.genomeSet[-1]
    
            while generation < self.threadGen:
                populationgenome = genetics()
                for genome in populationGenome:
                    indvfitness = fitness(genome)
                    populationgenome.addindiviual([indvfitness, genome])
                populationGenome = populationgenome.matingalgo()
                winner = min(populationgenome.phylogenome, key=itemgetter(0))
                generation += 1
                
            workingGenome.append(winner[1])
            
        self.genomeSet.append(workingGenome)

    def control(self, Threads = 10):
        from time import time
        
        start = time()
        
        print ''
        
        self.initiateThread()
        print 'Initial population complete'
        for gen in xrange(Threads):
            self.evolveAlgo()
            print 'Done with thread: %s'%(gen+1)
        
        winners = []

        for ind in self.genomeSet[-1]:
            winners.append([fitness(ind),ind])
            
        winner = min(winners, key = itemgetter(0))
        
        end = time()
        
        print 'Winning Genome:'
        print winner[1]
        print 'Fitness:'
        print winner[0]
        print 'Computation time:'
        print end-start
        
class genetics:         
        
    def __init__(self):
        self.phylogenome = []
    
    def addindiviual(self, individual):
        self.phylogenome.append(individual)
        
    def matingalgo(self, MUTATIONPROB = .5, MUTATIONFACTOR = .5, SURVIVORRATIO = .1, BINS = 10):
        from operator import itemgetter
        from random import random, choice, gauss
        import operator
        
        # MUTATIONPROB = .5 probability a gene will mutate
        # MUTATIONFACTOR = .5 factor of maximum mutation a gene can have
        # SURVIVORRATIO = .1 ratio of population that will be cloned - i.e winners
        
        self.phylogenome = sorted(self.phylogenome, key=itemgetter(0))

        length = len(self.phylogenome)
        itemsperbin = length//BINS

        population = []
        weights = []
        
        for n,item in enumerate(self.phylogenome):
            binnumber = (n//itemsperbin)+1
            if binnumber > BINS:
                binnumber += -1
            
            weight = (float(-binnumber + 1) / float(BINS)) + 1
            weights.append(weight)
            population.append(item[1])

        def accumulate(iterable, func=operator.add):
            it = iter(iterable)
            total = next(it)
            yield total
            for element in it:
                total = func(total, element)
                yield total        
        
        def randmating(population, weights):
            total = sum(weights)
            normedcdf = accumulate([val/total for val in weights])
            set0 = zip(*[normedcdf,weights,population])
            
            chance0 = random()
            sortingset0 = [(abs(indv[0]-chance0), n) for n, indv in enumerate(set0)]
            mn0 = min(sortingset0, key=itemgetter(0))
            mate1 = set0.pop(mn0[1])
            
            chance1 = random()
            sortingset1 = [(abs(indv[0]-chance1), n) for n, indv in enumerate(set0)]
            mn1 = min(sortingset1, key=itemgetter(0))
            mate2 = set0.pop(mn1[1])
            return (mate1[2], mate2[2])
            
        def sex(pair):
            geneset = zip(*pair)
            offspring = []
            for male, female in geneset:
                childGene = choice([male,female])
                if random() <= MUTATIONPROB:
                    childGene = int(gauss(childGene, childGene*MUTATIONFACTOR))%14300
                offspring.append(childGene)
            return offspring
        
        popsize = len(population)
        survivors = int(popsize * SURVIVORRATIO)
        matingPairs = [randmating(population, weights) for _ in xrange(popsize-survivors)]
        
        generationbeta = [population[n] for n in xrange(survivors)]
        
        for pair in matingPairs:
            offspring = sex(pair)
            generationbeta.append(offspring)

        return generationbeta