from json import loads
from os import listdir

class Maze:
    '''
    PyMaze Version 1.2.2.1
    '''
    def checkLevel(self, path: str = '.\\levels\\', level: str = None) -> list[bool, dict]:
        if not level: return None
        with open(f'{path}\\level{level}.json') as f:
            parsed = loads(f.read())
            valid = True
            if parsed.get('metadata') == None: valid = False
            if parsed['metadata'].get('minx') == None: valid = False
            if parsed['metadata'].get('maxx') == None: valid = False
            if parsed['metadata'].get('miny') == None: valid = False
            if parsed['metadata'].get('maxy') == None: valid = False
            if parsed['metadata'].get('startx') == None: valid = False
            if parsed['metadata'].get('starty') == None: valid = False
            if parsed['metadata'].get('endx') == None: valid = False
            if parsed['metadata'].get('endy') == None: valid = False
            if parsed.get('maze') == None: valid = False
            if not valid: parsed = None
            else: print ('valid')
            return [valid, parsed]
    
    def checkLevels(self, path: str = '.\\levels\\') -> dict[str: dict[str: str]]:
        valid = {}
        for name in listdir(path):
            if name.startswith('level') and name.endswith('.json'):
                lid = name.removeprefix('level').removesuffix('.json')
                check = self.checkLevel(path, lid)
                if check[0]: valid.update({lid: check[1]})
        return valid
    
    def __init__(self, level: str = '0', watchsize: int = 5):
        self.VERSION = '1.2.2.1'
        self.max_level = len(self.checkLevels())
        self.watchsize = watchsize if watchsize in [3,5] else 5
        check = self.checkLevel(level=level)
        if check[0]:
            self.minx = check[1]['metadata']['minx']
            self.maxx = check[1]['metadata']['maxx']
            self.miny = check[1]['metadata']['miny']
            self.maxy = check[1]['metadata']['maxy']
            self.playerx = check[1]['metadata']['startx']
            self.playery = check[1]['metadata']['starty']
            self.endx = check[1]['metadata']['endx']
            self.endy = check[1]['metadata']['endy']
            self.level = level
            self.maze = check[1]['maze']
        else:
            self.minx = 1
            self.maxx = 11
            self.miny = 1
            self.maxy = 11
            self.playerx = 6
            self.playery = 11
            self.endx = 6
            self.endy = 0
            self.level = '0'
            self.maze = [
                [['#'],['#'],['#'],['#'],['#'],['#'],[' '],['#'],['#'],['#'],['#'],['#'],['#']],
                [['#'],['#'],['#'],['#'],[' '],['#'],[' '],['#'],[' '],[' '],[' '],['#'],['#']],
                [['#'],['#'],['#'],['#'],[' '],['#'],[' '],[' '],[' '],['#'],[' '],['#'],['#']],
                [['#'],['#'],['#'],['#'],[' '],['#'],['#'],['#'],[' '],['#'],['#'],['#'],['#']],
                [['#'],['#'],['#'],['#'],[' '],[' '],[' '],['#'],[' '],[' '],[' '],[' '],['#']],
                [['#'],['#'],['#'],['#'],['#'],[' '],['#'],['#'],[' '],['#'],['#'],[' '],['#']],
                [['#'],['#'],['#'],['#'],[' '],[' '],[' '],['#'],[' '],['#'],[' '],[' '],['#']],
                [['#'],[' '],['#'],[' '],[' '],['#'],[' '],['#'],['#'],['#'],['#'],[' '],['#']],
                [['#'],[' '],['#'],[' '],['#'],['#'],[' '],[' '],[' '],[' '],[' '],[' '],['#']],
                [['#'],[' '],[' '],[' '],['#'],[' '],[' '],['#'],['#'],['#'],[' '],['#'],['#']],
                [['#'],['#'],['#'],[' '],['#'],['#'],['#'],['#'],[' '],[' '],[' '],[' '],['#']],
                [['#'],['#'],[' '],[' '],[' '],[' '],[' '],['#'],['#'],['#'],[' '],['#'],['#']],
                [['#'],['#'],['#'],['#'],['#'],['#'],['#'],['#'],['#'],['#'],['#'],['#'],['#']]
            ]
    
    def movePlayer(self, bx: int, by: int) -> int:
        nx = self.playerx + bx
        ny = self.playery + by
        if nx == self.endx and ny == self.endy: return 1
        if nx < self.minx or nx > self.maxx: return 0
        if ny < self.miny or ny > self.maxy: return 0
        if self.maze[ny][nx][0] == '#': return 0
        self.playerx = nx
        self.playery = ny
        return 2
    
    def showArea(self) -> list[list[str]]:
        final = [chr(7356)*self.watchsize]
        exn, exp = (0 if self.playerx <= self.minx else 1, 0 if self.playerx >= self.maxx else 1)
        eyn, eyp = (0 if self.playery <= self.miny else 1, 0 if self.playery >= self.maxy else 1)
        if self.watchsize == 3: exn, exp, eyn, eyp = 0, 0, 0, 0
        
        for row in self.maze[self.playery-1-eyn:self.playery+2+eyp]: final.append(''.join(e[0] for e in row[self.playerx-1-exn:self.playerx+2+exp]))
        if len(final) == self.watchsize+1: del final[0]
        
        fcx = -1 if exn == 0 and exp == 1 else 0
        fcy = 1 if eyn == 1 and eyp == 0 else 0

        if self.watchsize == 3: final[1] = final[1][0] + 'x' + chr(8201) + final[1][2]
        elif self.watchsize == 5: final[2+fcy] = final[2+fcy][0:2+fcx] + 'x' + chr(8201) + final[2+fcy][3+fcx:5+fcx]
        return final
    
    def nextLevel(self) -> str:
        if self.checkLevels().get(str(int(self.level)+1)): return str(int(self.level)+1)
        return ''
    
    def putLevelData(self, mazeLevel: list[list[str]]) -> None:
        self.maze = mazeLevel #Validate this