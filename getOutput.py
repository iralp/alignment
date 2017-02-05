# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 20:36:57 2016

@author: iralp
"""
from random import randint
import os
import puzzleGenerator
#automate 20 random input and output generation

noOfIterations = 1
nSize = [3,5]

while noOfIterations != 0:
    n = randint(0,1)
    size = nSize[n]
    algo = 1
    noOfMoves = randint(40,60)
    #call puzzle generator to populate the input file
    os.system('puzzleGenerator.py '+ str(size) + ' '+ str(noOfMoves) +' F:/Anaconda3/AI/Input.txt')
    noOfIterations = noOfIterations  - 1
