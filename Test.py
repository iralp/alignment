# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 18:35:39 2016

@author: iralp
"""
import numpy

dict_ValRowCol_3 = {}
dict_ValRowCol_4 = {}

    
def getHammingDistanceHeuristic(matrx_):
    sumOfDistances = 0
    dict_ValRowCol = {}
    tp1 = ()
    size = 4
    if size == 3:
        dict_ValRowCol = dict_ValRowCol_3
    else:
        dict_ValRowCol = dict_ValRowCol_4
    for row in range(size):
        for col in range(size):
            noHere = matrx_[row][col]
            print("no : ",matrx_[row][col])
            tp1 = dict_ValRowCol[noHere]
            if row != tp1[0] or col != tp1[1]:
                sumOfDistances = sumOfDistances + 1
    return sumOfDistances
    
def initializeDict():
        noToCheck = 1
        size = 4
        if size == 3:
            dict_ValRowCol = dict_ValRowCol_3
        else:
            dict_ValRowCol = dict_ValRowCol_4
        for row in range(size):
            for col in range(size):
                dict_ValRowCol[noToCheck] = (row,col)
                noToCheck = noToCheck + 1                
                if noToCheck == size * size :
                    noToCheck = 0
initializeDict()
matrx = numpy.matrix('1 9 2 3; 6 10 11 4; 5 14 0 15; 13 12 8 7')
print(" returned ",getHammingDistanceHeuristic(matrx)) 