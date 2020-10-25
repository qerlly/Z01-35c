import sys
import os

def files(path,extention):
    array = [f for f in os.listdir(path) if f.endswith(extention)]
    for i in array:
        print(i, end = ' ')

if __name__ == "__main__":
    path = str(sys.argv[1])
    extention = str(sys.argv[2])
    files(path, extention)