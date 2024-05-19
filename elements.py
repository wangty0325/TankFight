from cmu_graphics import *
import PIL.Image

class Tree:
    def __init__(self, topleft_x, topleft_y):
        self.image = PIL.Image.open("tree4.png")
        self.image = self.image.resize((20, 20))
        self.image = CMUImage(self.image)
        self.being = True
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.row = int(topleft_y/20)
        self.col = int(topleft_x/20)
        self.width = 20
        self.height = 20


class Brick:
    def __init__(self, topleft_x, topleft_y):
        self.image = PIL.Image.open("brick.png")
        self.image = self.image.resize((20, 20))
        self.image = CMUImage(self.image)
        self.being = True
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.row = int(topleft_y/20)
        self.col = int(topleft_x/20)
        self.width = 20
        self.height = 20

class Iron:
    def __init__(self, topleft_x, topleft_y):
        self.image = PIL.Image.open("iron.png")
        self.image = self.image.resize((20, 20))
        self.image = CMUImage(self.image)
        self.being = True
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.width = 20
        self.height = 20



class Map:
    def __init__(self):
        self.pool = dict()
        self.brickList = []
        self.ironList = []
        self.board = [[0] * 30 for row in range(40)]
        # empty cell = 0
        # brick = 1
        # iron = 2

    def map1(self):

        for col in [2, 3, 6, 7, 22, 23, 26, 27]:
            for row in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]:
                topleft_x, topleft_y = col*20, row*20
                self.brick = Brick(topleft_x, topleft_y)
                self.pool[(topleft_x, topleft_y)] = self.brick
                self.brickList.append(self.brick)
                self.board[row][col] = 1


        for col in [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]:
            for row in [4, 5, 34, 35]:
                topleft_x, topleft_y = col*20, row*20
                self.brick = Brick(topleft_x, topleft_y)
                self.pool[(topleft_x, topleft_y)] = self.brick
                self.brickList.append(self.brick)
                self.board[row][col] = 1

        for col in [0, 1, 2, 3, 26, 27, 28, 29]:
            for row in [18, 19, 20, 21]:
                topleft_x, topleft_y = col*20, row*20
                self.iron = Iron(topleft_x, topleft_y)
                self.pool[(topleft_x, topleft_y)] = self.iron
                self.ironList.append(self.iron)
                self.board[row][col] = 2

        for col in [12,17]:
            for row in [18,21]:
                topleft_x, topleft_y = col*20, row*20
                self.iron = Iron(topleft_x, topleft_y)
                self.pool[(topleft_x, topleft_y)] = self.iron
                self.ironList.append(self.iron)
                self.board[row][col] = 2



        for col in [12,13,14,15,16,17]:
            for row in [8,9,10,11,28,29,30,31]:
                topleft_x, topleft_y = col*20, row*20
                self.brick = Brick(topleft_x, topleft_y)
                self.pool[(topleft_x, topleft_y)] = self.brick
                self.brickList.append(self.brick)
                self.board[row][col] = 1
        
        for col in [10,11,18,19]:
            for row in [14,15,16,17,22,23,24,25]:
                topleft_x, topleft_y = col*20, row*20
                self.brick = Brick(topleft_x, topleft_y)
                self.pool[(topleft_x, topleft_y)] = self.brick
                self.brickList.append(self.brick)
                self.board[row][col] = 1

        for col in [0,1,2,3,26,27,28,29]:
            for row in [38,39]:
                topleft_x, topleft_y = col*20, row*20
                self.brick = Brick(topleft_x, topleft_y)
                self.pool[(topleft_x, topleft_y)] = self.brick
                self.brickList.append(self.brick)
                self.board[row][col] = 1

        for col in range(4,26):
            for row in range(18, 22):
                topleft_x, topleft_y = col*20, row*20
                self.brick = Tree(topleft_x, topleft_y)
                self.pool[(topleft_x, topleft_y)] = self.brick
                self.brickList.append(self.brick)
                self.board[row][col] = 0

        return self
    
    def drawMap(self):
        for (topleft_x, topleft_y) in self.pool:
            tile = self.pool[(topleft_x, topleft_y)]
            # check does each exist
            if tile.being:
                drawImage(tile.image, topleft_x, topleft_y)


