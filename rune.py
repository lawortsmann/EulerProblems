# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 01:19:36 2015

@author: Lawortsmann
"""

from evolutionary import simulation

testsimulation = simulation(popSize = 100, threadGen = 50, initThreadPop = 100)
testsimulation.control(Threads = 10)