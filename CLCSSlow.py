#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 23:41:42 2018

@author: franklinjohnson
"""

import sys
import numpy as np


arr = np.zeros((2048, 2048), dtype=int)

def LCS(A,B):
	m = len(A)
	n = len(B)

	for i in range(1,m+1):
		for j in range(1,n+1):
			if A[i-1] == B[j-1]:
				arr[i][j] = arr[i-1][j-1]+1
			else:
				arr[i][j] = max(arr[i-1][j], arr[i][j-1])

	return arr[m][n]

def Cut(word,i):
    return word[i:]+word[:i]

def CLCS(A,B):
    sys.stderr.write(A+'|||'+B+'\n')
    smaller = ''
    if len(A)>len(B):
        smaller,larger = B,A
        
    else: smaller,larger = A,B
    larger = larger
    return max(LCS(larger,Cut(smaller,i)) for i in range(len(smaller)))

def main():
	if len(sys.argv) != 1:
            #print sys.argv
            sys.exit('Usage: `python LCS.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		print CLCS(A,B)
	return

if __name__ == '__main__':
    main()
    