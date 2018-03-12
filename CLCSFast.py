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
    for i in range(1,n+1):
        for j in range(h[i],l[i]+1):
            arr[j][i] = 0
            
def InBounds(n,m,l,h): #given a position at (n,m), and the bounds lists l and h, say if it's in the bounds
    return m<=l[n] and m>=h[n]


#returns (score,path) where path is an array of tuples, each tuple is a coord
def SingleShortestPath(A,B,start,l,h): 
    makeZeros(A,B,l,h)   
    m = len(A)/2
    n = len(B)
    path,bp = [],{}
    #print 'NEW'
    for i in range(1,n+1): #make the table
        for j in range(max(start+1,h[i]),min(start+m+1,l[i]+1)):
          #  print j-1,i-1
            if A[j-1] == B[i-1] and InBounds(i-1,j-1,l,h):
                arr[j][i] = arr[j-1][i-1]+1
                bp[(j,i)]=(j-1,i-1)          
            else:
                neighbors = []
                if InBounds(i-1,j,l,h):
                    neighbors.append((arr[j][i-1],(j,i-1)))
                if InBounds(i,j-1,l,h):
                    neighbors.append((arr[j-1][i],(j-1,i)))
                val = max(neighbors)
                arr[j][i] = val[0]
                bp[(j,i)]=val[1]
    score = arr[start+m][n]
    currNode = (start+m,n)
    while currNode[0]!=start and currNode[1] != 0:
        #print currNode
        path.append(currNode)
        currNode = bp[currNode]
    path.append(currNode)
    if currNode[0] == start:
        while currNode[1] != 0:       
            currNode = (currNode[0],currNode[1]-1)
            path.append(currNode)
    if currNode[1] == 0:
        while currNode[0] != start:            
            currNode = (currNode[0]-1,currNode[1])
            path.append(currNode)
            
        
    return (score, path)

def CLCS(A,B,results):
    #results = []
    arr.fill(0)
    sys.stderr.write(A+'|||'+B+'\n')
    A = A+A
    h = {n:0 for n in range(0,len(B)+1)} #h is high boundary
    l = {n:len(A) for n in range(0,len(B)+1)} #l is low boundary
    h = SingleShortestPath(A,B,0,l,h)
    results.append(h[0])
    h = h[1]
    border = {}
    for pos in h:
        border[pos[1]] = border.get(pos[1],[]) + [pos[0]]
    hborder,lborder = {},{}
    for key in border:
        hborder[key] = min(border[key])
        lborder[key] = max(border[key])+len(A)/2
    FindShortestPath(A,B,hborder,lborder,0,len(A)/2)
    return max(results)
    
def FindShortestPath(A,B,h,l,highStart,lowStart):
    if lowStart-highStart <=1: return
    start = (highStart+lowStart)/2
    mid = SingleShortestPath(A,B,start,l,h)
    results.append(mid[0])
    midPath = mid[1]
    border = {}
    for pos in midPath:
        border[pos[1]] = border.get(pos[1],[]) + [pos[0]]
    hborder,lborder = {},{}
    for key in border:
        hborder[key] = min(border[key])
        lborder[key] = max(border[key])#+len(A)/2
    FindShortestPath(A,B,h,lborder,highStart,start)
    FindShortestPath(A,B,hborder,l,start,lowStart)
    
    
    


def main():
    if len(sys.argv) != 1:
        #print sys.argv
        sys.exit('Usage: `python LCS.py < input`')
	
    for l in sys.stdin:
        results = []
        A,B = l.split()
        print CLCS(A,B,results)
	return

if __name__ == '__main__':
    main()

#print SingleShortestPath('ABA','ABBABA',3,{0:5,1:5,2:5,3:5,4:5,5:5},{0:,1:5,2:5,3:5,4:5,5:5})
#print CLCS('ABA','ABBABA',results)
#print CLCS('BBAA','ABABB',results)
#print CLCS('EBADAEEABBBCEDE','ACBAAABDCAEADCEEBBDADDCEBCADCAEBBCDCAEDAC',results)
#print CLCS('ACBBBCDCEDBADBBEABBEDAEADEBAEB','AEBEEAEEABAEEBCACDBBAEABCEDCABEEDACEEC',results)
#print CLCS('C','CDCCCEDBDEADEACDEBAEDDEAEAADCAEDAD',results)
#print CLCS('ADCDEDC','AECBABBBBDABBDBBEBDBCACDADEEDCCCAACDC',results)

    