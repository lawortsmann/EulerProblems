# coding: utf-8
"""
Created on Sun Feb 22 14:51:12 2015

Sum of digits in a factorial

@author: Luke_Wortsmann
"""

def factorial(number):
    factorial = reduce(lambda a, b: a * b, range(1, number))
    return factorial

summation = 0
factorial100 = factorial(100)
for d in str(factorial100):
    summation += int(d)

print summation
