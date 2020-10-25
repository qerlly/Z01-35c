import sys
import os
from pathlib import Path
space =  '    '
branch = '│   '
tee =    '├── '
last =   '└── '

def tree(dir_path: Path, prefix: str=''):  
    contents = [d for d in dir_path.iterdir() if d.is_dir()]
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir(): 
            extension = branch if pointer == tee else space 
            yield from tree(path, prefix=prefix+extension)

if __name__ == "__main__":
    path = Path(sys.argv[1])
    for line in tree(path):
        print(line)