from cmu_graphics import *
import PIL.Image


# CITATION: I got the image bullet from https://www.bilibili.com/video/BV1bE411P7Uw/?spm_id_from=333.337.search-card.all.click&vd_source=428d71e073aa442b8cecdb51339301ce



class bullet():
    def __init__(self, cx, cy, attack, direction, being):
        self.direction = direction
        self.speed = 6
        self.cx = cx 
        self.cy = cy
        self.width = 4
        self.height = 6
        self.attack = attack
        self.being = being


    def __repr__(self):
        return f'{(self.cx, self.cy)}'


# draw bullet based on the tank's direction
    def drawBullet(self):
        bullet_up = PIL.Image.open("bullet.png")
        bullet_up = bullet_up.resize((self.width, self.height))
        bullet_up = CMUImage(bullet_up)
        if self.being:
            if self.direction == 'up':
                drawImage(bullet_up, self.cx, self.cy, align='center')
            elif self.direction == 'right':
                drawImage(bullet_up, self.cx, self.cy, align='center', rotateAngle = 90)
            elif self.direction == 'down':
                drawImage(bullet_up, self.cx, self.cy, align='center', rotateAngle = 180)
            elif self.direction == 'left':
                drawImage(bullet_up, self.cx, self.cy, align='center', rotateAngle = 270)


# bullet moves based on the tank's direction
    def move(self):
        bullet_up = PIL.Image.open("bullet.png")
        bullet_up = bullet_up.resize((4,6))
        bullet_up = CMUImage(bullet_up)
        if self.cx < 0 or self.cx > 600 or self.cy < 0 or self.cy > 800:
            self.being = False
        if self.being:
            if self.direction == 'up':
                self.cy -= self.speed
            elif self.direction  == 'right':
                self.cx += self.speed
            elif self.direction == 'down':
                self.cy += self.speed
            elif self.direction == 'left':
                self.cx -= self.speed

    def isBulletCollideWithBrick(self, brick):
        #for brick in brickList:
        brickLeft = brick.topleft_x
        brickRight = brick.topleft_x + brick.width
        brickTop = brick.topleft_y
        brickBottom = brick.topleft_y + brick.height

        bulletLeft = self.cx - self.width/2
        bulletRight = self.cx + self.width/2
        bulletTop = self.cy - self.height/2
        bulletBottom = self.cy + self.height/2

        if brick.being:  # only check the existing bricks
            if (bulletLeft < brickRight and bulletRight > brickLeft and
            bulletTop < brickBottom and bulletBottom > brickTop):
                return True # Collision detected
                
    def bulletDestroyTank(self, tankList):
        for tank in tankList:
            tankLeft = tank.topleft_x
            tankRight = tank.topleft_x + tank.width
            tankTop = tank.topleft_y
            tankBottom = tank.topleft_y + tank.height

            bulletLeft = self.cx - self.width/2
            bulletRight = self.cx + self.width/2
            bulletTop = self.cy - self.height/2
            bulletBottom = self.cy + self.height/2

            if tank.being and self.being:
                if (bulletLeft < tankRight and bulletRight > tankLeft and
                bulletTop < tankBottom and bulletBottom > tankTop):
                    print('collide')
                    tank.health -= 1
                    self.being = False
                if tank.health == 0:
                    tank.being = False
        return


"""     def drawBullet(self): 
        bullet_up = PIL.Image.open("bullet.png")
        bullet_up = bullet_up.resize((4,6))
        drawImage(bullet_up, self.cx, self.cy, align='center')
        if self.being:
            if self.direction == 'up':
                drawImage(self.bullet_up, self.cx, self.cy, align='center')
            elif self.direction == 'right':
                drawImage(self.bullet_up, self.cx, self.cy, align='center', rotateAngle = 90)
            elif self.direction == 'down':
                drawImage(self.bullet_up, self.cx, self.cy, align='center', rotateAngle = 180)
            elif self.direction == 'left':
                drawImage(self.bullet_up, self.cx, self.cy, align='center', rotateAngle = 270)
    
    def move(self):
        if 0 <= self.dx <= 600 or 0 <= self.xy <= 800:
            self.being = False
        if self.being:
            if self.direction == 'up':
                self.cx -= self.speed
            elif self.direction == 'right':
                self.cy += self.speed
            elif self.direction == 'down':
                self.cx += self.speed
            elif self.direction == 'left':
                self.cy -= self.speed """


        
