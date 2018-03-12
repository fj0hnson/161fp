#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 13:50:00 2018

@author: franklinjohnson
"""
import sys
import numpy as np

results = [] #array of ints
arr = np.zeros((2048, 2048), dtype=int)

def makeZeros(A,B,l,h):
    n = len(B)
    for i in range(0,n):
        for j in range(h[i],l[i]+1):
            arr[j][i] = 0
            
def checkIfInBounds(n,m,l,h): #given a position at (n,m), and the bounds lists l and h, say if it's in the bounds
    return m<l[n] and m>h[n]


#returns (score,path) where path is an array of tuples, each tuple is a coord
def SingleShortestPath(A,B,start,l,h): 
    A = A+A
    makeZeros(A,B,l,h)   
    m = len(A)
    n = len(B)
    path,bp = [],{}
    for i in range(1,n+1):
        for j in range(max(start,h[i]),min(start+m+1,l[i]+1)):
            if A[j-1] == B[i-1]:
                arr[j][i] = arr[j-1][i-1]+1
                bp[(j,i)]=(j-1,i-1)          
            else:
                val = max((arr[j-1][i], (j-1,i)), (arr[j][i-1], (j,i-1)))
                arr[j][i] = val[0]
                bp[(j,i)]=val[1]
    score = arr[start+m][n]
    currNode = (start+m,n)
    while currNode != (start,0):
        path.append(currNode)
        currNode = bp[currNode]
    return (score, path)

def CLCS(A,B,results):
    h = {n:1 for n in range(len(B))} #h is high boundary
    l = {n:2*len(A) for n in range(len(B))} #l is low boundary
    h = SingleShortestPath(A,B,0,l,h)
    results.append(h[0])
    h = h[1]
    border = {}
    for pos in h:
        border[pos[1]] = border.get(pos[1],[]) + [pos[0]]
    hborder,lborder = {},{}
    for key in border:
        hborder[key] = min(border[key])
        lborder[key] = max(border[key])+len(A)
    FindShortestPath(A,B,hborder,lborder)
    return max(results)
    
def FindShortestPath(A,B,h,l):
    if l[1]-h[1] <=1: return
    start = (h[1]+l[1])/2
    mid = SingleShortestPath(A,B,start,l,h)
    results.append(mid[0])
    midPath = mid[1]
    border = {}
    for pos in midPath:
        border[pos[1]] = border.get(pos[1],[]) + [pos[0]]
    hborder,lborder = {},{}
    for key in border:
        hborder[key] = min(border[key])
        lborder[key] = max(border[key])+len(A)
    FindShortestPath(A,B,h,lborder)
    FindShortestPath(A,B,hborder,l)
    
    
    


def main():
	if len(sys.argv) != 1:
            #print sys.argv
            sys.exit('Usage: `python LCS.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		print CLCS(A,B,results)
	return

#if __name__ == '__main__':
#    main()

#print SingleShortestPath('ABA','ABBABA',3,{0:5,1:5,2:5,3:5,4:5,5:5},{0:,1:5,2:5,3:5,4:5,5:5})
print CLCS('ABA','ABBABA',results)
    