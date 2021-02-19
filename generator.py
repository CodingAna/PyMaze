from PIL import Image
from os.path import isdir, isfile

class File:
    def __init__(self, filename: str, filepath: str = '.\\') -> None:
        self.filename = filename
        self.filepath = filepath if filepath.endswith('\\') else filepath + '\\'
    
    def getFilepath(self) -> str: return self.filepath
    def getFilename(self) -> str: return self.filename
    def getLongPath(self) -> str: return self.filepath + '\\'
    
    def content(self) -> bytes:
        if not isdir(self.filepath) or not isfile(self.filepath + self.filename): raise FileNotFoundError(f'The file {self.filename} does not exist in {self.filepath}')
        with open(self.filepath + '\\' + self.filename, 'rb') as f: return f

class LevelGen:
    '''
    Level generator for PyMaze
    Version 0.1
    '''
    def __init__(self, image = File or str) -> None:
        img = Image.open(image)
        limg = img.load()

        maze = []

        for y in range(img.height):
            row = []
            for x in range(img.width):
                p = limg[x, y]
                c = '#' if p == (0, 0, 0) else ' '
                row.append([c])
            maze.append(row)
