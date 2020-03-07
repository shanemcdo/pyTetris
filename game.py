import pygame
from coord import coord
from time import sleep
from random import randint

class game:

    peices = [
	[
		".I..",
		".I..",
		".I..",
		".I..",
	],
	[
		".S..",
		".SS.",
		"..S.",
		"....",
	],
	[
		"..Z.",
		".ZZ.",
		".Z..",
		"....",
	],
	[
		"..T.",
		".TT.",
		"..T.",
		"....",
	],
	[
		"....",
		".OO.",
		".OO.",
		"....",
	],
	[
		".L..",
		".L..",
		".LL.",
		"....",
	],
	[
		"..J.",
		"..J.",
		".JJ.",
		"....",
	],
        ]

    def __init__(self, sz=(450,600), scl=30):
        pygame.display.init()
        self.screen = pygame.display.set_mode(size=sz)
        self.running = False
        self.scl = scl
        self.pos = coord(4,0)
        self.holdready = True
        self.hold = [
                ['.','.','.','.'],
                ['.','.','.','.'],
                ['.','.','.','.'],
                ['.','.','.','.'],
                ]
        self.grid = [
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.','.','.'],
                ]
        self.peice = [
                ".T..",
                ".TT.",
                ".T..",
                "....",
                ]
        self.queue = [
            [
                    "....",
                    "....",
                    "....",
                    "....",
            ],
            [
                    "....",
                    "....",
                    "....",
                    "....",
            ],
            [
                    "....",
                    "....",
                    "....",
                    "....",
            ],
            [
                    "....",
                    "....",
                    "....",
                    "....",
            ],
            [
                    "....",
                    "....",
                    "....",
                    "....",
            ],
            ]

    def realpos(self, x=0, y=0):
        return coord((self.pos.x + x) * self.scl, (self.pos.y + y) * self.scl)

    def printblock(self, real, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(real.x, real.y, self.scl, self.scl))    

    def printpeice(self):
        for i, line in enumerate(self.peice):
            for j, ch in enumerate(line):
                if ch != '.':
                    real = self.realpos(j, i)
                    color = self.selectcolor(ch)
                    self.printblock(coord(real.x, real.y), color)

    def collision(self):
        for i, line in enumerate(self.peice):
            for j, ch in enumerate(line):
                if ch != '.':
                    if self.pos.x + j < 0 or self.pos.x + j > 9 or self.pos.y + i > 19:
                        return True
                    elif self.grid[self.pos.y + i][self.pos.x + j] != '.':
                        return True
        return False

    def move(self, change):
        down = False
        if change == coord(0,1):
            down = True
        self.pos.x += change.x
        self.pos.y += change.y
        if self.collision():
            self.pos.x -= change.x
            self.pos.y -= change.y
            if down:
                self.lock()
            return False
        return True

    def rotate(self, ch, recur=True):
        temp = [
                ['.','.','.','.'],
                ['.','.','.','.'],
                ['.','.','.','.'],
                ['.','.','.','.'],
                ]
        if ch == 'r':
            for i in range(4):
                for j in range(4):
                    temp[i][j] = self.peice[3 - j][i]
            self.peice = temp
            if self.collision() and recur:
                self.rotate('l', False)
        elif ch == 'l':
            for i in range(4):
                for j in range(4):
                    temp[i][j] = self.peice[j][3 - i]
            self.peice = temp
            if self.collision() and recur:
                self.rotate('r', False)

    def getnextpeice(self):
        self.peice = self.queue.pop(0)
        self.queue.append(self.getrandpeice())

    def getrandpeice(self):
        return self.peices[randint(0,6)]                
    
    def fillqueue(self):
        new_queue = []
        for item in self.queue:
             new_queue.append(self.getrandpeice())
        self.queue = new_queue

    def lock(self):
        self.holdready = True
        for i, line in enumerate(self.peice):
            for j, ch in enumerate(line):
                if ch != '.':
                    self.grid[i + self.pos.y][j + self.pos.x] = ch
        self.getnextpeice()
        self.pos = coord(4,0)
        if self.collision():
            self.running = False

    def printgrid(self):
        for i, line in enumerate(self.grid):
            for j, ch in enumerate(line):
                if ch != '.':
                    color = self.selectcolor(ch)
                    self.printblock(coord(j * self.scl, i* self.scl), color)

    def selectcolor(self, ch):
        if ch == 'I':
            return (64, 207, 255)
        elif ch == 'S':
            return (4, 255, 0)
        elif ch == 'Z':
            return (255, 0, 0)
        elif ch == 'T':
            return (174, 0, 255)
        elif ch == 'O':
            return (238, 255, 0)
        elif ch == 'L':
            return (255, 153, 0)
        elif ch == 'J':
            return (0, 13, 255)
        return (0, 0, 0)

    def instadrop(self):
        while self.move(coord(0,1)):
            pass

    def printqueue(self):
        pygame.draw.line(self.screen, (255,255,255), (300, 0), (300,600), 3)
        for n, item in enumerate(self.queue):
            for i, line in enumerate(item):
                for j, ch in enumerate(line):
                    point = coord(315 + j * self.scl,15 + 150 * (n+1) + i * self.scl)
                    color = self.selectcolor(ch)
                    self.printblock(point, color)

    def swaphold(self):
        if self.holdready:
            self.peice, self.hold = self.hold, self.peice
            self.pos = coord(4,0)
            self.holdready = False
            empty = True
            for line in self.peice:
                for ch in line:
                    if ch != '.':
                        empty = False
            if empty:
                self.getnextpeice()

    def printhold(self):
        pygame.draw.line(self.screen, (255,255,255), (300, 135), (450, 135), 3)
        for i, line in enumerate(self.hold):
            for j, ch in enumerate(line):
                point = coord(315 + j * self.scl,14 + i * self.scl)
                color = self.selectcolor(ch)
                self.printblock(point, color)

    def clearlines(self):
        for i, line in enumerate(self.grid):
            full = True            
            for ch in line:
                if ch == '.':
                    full = False
            if full:
                _ = self.grid.pop(i)
                self.grid.insert(0, ['.','.','.','.','.','.','.','.','.','.',])

    def play(self):
        #game loop
        pygame.key.set_repeat(80)
        self.fillqueue()
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.unicode == 'w':
                        self.instadrop()
                    elif event.unicode == 'a':
                        self.move(coord(-1,0))
                    elif event.unicode == 's':
                        self.move(coord(0,1))
                    elif event.unicode == 'd':
                        self.move(coord(1,0))
                    elif event.unicode == 'q':
                        self.rotate('l')
                    elif event.unicode == 'e':
                        self.rotate('r')
                    elif event.unicode == ' ':
                        self.swaphold()
            self.screen.fill((0,0,0)) #clear screen
            self.clearlines()
            self.printgrid()
            self.printqueue()
            self.printhold()
            self.printpeice()
            pygame.display.update()
            sleep(0.02)
