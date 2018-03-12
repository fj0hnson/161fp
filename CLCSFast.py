#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 13:50:00 2018

@author: franklinjohnson
"""
import sys
import numpy as np



def main():
    if len(sys.argv) != 1:
        #print sys.argv
        sys.exit('Usage: `python LCS.py < input`')
	
    for l in sys.stdin:
        test = Dabber()
        A,B = l.split()
        print test.CLCS(A,B)
    return

class Dabber:
    
    def __init__(self):
        self.results = []
        self.arr = np.zeros((2048,2048),dtype=int)

    def makeZeros(self,A,B,l,h):
        n = len(B)
        for i in range(1,n+1):
            for j in range(h[i],l[i]+1):
                self.arr[j][i] = 0
                
    def InBounds(self,n,m,l,h): #given a position at (n,m), and the bounds lists l and h, say if it's in the bounds
        return m<=l[n] and m>=h[n]
    
    
    #returns (score,path) where path is an array of tuples, each tuple is a coord
    def SingleShortestPath(self,A,B,start,l,h): 
        self.makeZeros(A,B,l,h)   
        m = len(A)/2
        n = len(B)
        path,bp = [],{}
        #print 'NEW'
        for i in range(1,n+1): #make the table
            for j in range(max(start+1,h[i]),min(start+m+1,l[i]+1)):
              #  print j-1,i-1
                if A[j-1] == B[i-1] and self.InBounds(i-1,j-1,l,h):
                    self.arr[j][i] = self.arr[j-1][i-1]+1
                    bp[(j,i)]=(j-1,i-1)          
                else:
                    neighbors = []
                    if self.InBounds(i-1,j,l,h):
                        neighbors.append((self.arr[j][i-1],(j,i-1)))
                    if self.InBounds(i,j-1,l,h):
                        neighbors.append((self.arr[j-1][i],(j-1,i)))
                    val = max(neighbors)
                    self.arr[j][i] = val[0]
                    bp[(j,i)]=val[1]
        score = self.arr[start+m][n]
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
    
    def CLCS(self,A,B):
        #results = []
        #sys.stderr.write(A+'|||'+B+'\n')
        A = A+A
        h = {n:0 for n in range(0,len(B)+1)} #h is high boundary
        l = {n:len(A) for n in range(0,len(B)+1)} #l is low boundary
        h = self.SingleShortestPath(A,B,0,l,h)
        self.results.append(h[0])
        h = h[1]
        border = {}
        for pos in h:
            border[pos[1]] = border.get(pos[1],[]) + [pos[0]]
        hborder,lborder = {},{}
        for key in border:
            hborder[key] = min(border[key])
            lborder[key] = max(border[key])+len(A)/2
        self.FindShortestPath(A,B,hborder,lborder,0,len(A)/2)
        return max(self.results)
        
    def FindShortestPath(self,A,B,h,l,highStart,lowStart):
        if lowStart-highStart <=1: return
        start = (highStart+lowStart)/2
        mid = self.SingleShortestPath(A,B,start,l,h)
        self.results.append(mid[0])
        midPath = mid[1]
        border = {}
        for pos in midPath:
            border[pos[1]] = border.get(pos[1],[]) + [pos[0]]
        hborder,lborder = {},{}
        for key in border:
            hborder[key] = min(border[key])
            lborder[key] = max(border[key])#+len(A)/2
        self.FindShortestPath(A,B,h,lborder,highStart,start)
        self.FindShortestPath(A,B,hborder,l,start,lowStart)
        
    
    




if __name__ == '__main__':
    main()
'''
test = Dabber()

#print SingleShortestPath('ABA','ABBABA',3,{0:5,1:5,2:5,3:5,4:5,5:5},{0:,1:5,2:5,3:5,4:5,5:5})
#print CLCS('ABA','ABBABA',results)
print test.CLCS('BBAA','ABABB')
test = Dabber()
print test.CLCS('EBADAEEABBBCEDE','ACBAAABDCAEADCEEBBDADDCEBCADCAEBBCDCAEDAC')
test = Dabber()
print test.CLCS('ACBBBCDCEDBADBBEABBEDAEADEBAEB','AEBEEAEEABAEEBCACDBBAEABCEDCABEEDACEEC')
test = Dabber()
print test.CLCS('C','CDCCCEDBDEADEACDEBAEDDEAEAADCAEDAD')
test=Dabber()
print test.CLCS('ADCDEDC','AECBABBBBDABBDBBEBDBCACDADEEDCCCAACDC')
#'''
    