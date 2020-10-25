import sys
import os

def sortList(array):
    n=len(array) 
    array=sys.argv[1][1:n-1] 
    array=array.split(',') 
    array.sort(key = int) 
    for i in array:
        print(i, end = ' ')

if __name__ == "__main__":
    array = list(sys.argv[1])
    sortList(array)