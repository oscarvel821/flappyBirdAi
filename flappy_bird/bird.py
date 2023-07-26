import pygame

class Bird(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.initialPosition = (x, y)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1,4):
            img = pygame.image.load(f'images/bird{i}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = 0
        self.flying = False
        self.gameOver = False
        self.pass_pipe = False
        self.score = 0

    def update(self):
        #gravity
        if self.flying:
            self.vel += 0.5
            if self.vel > 20:
                self.vel = 20 

            #update the bird position
            if self.rect.bottom < 912:
                self.rect.y += int(self.vel)
            else: #bird hit the ground - Gameover
                self.flying = False
                self.gameOver = True

            self.birdAnimation(5)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

    #bird's jump function
    def jump(self):
        if self.gameOver == False:
            self.vel -= 10
            if self.vel < -10:
                self.vel = -10
            self.rect.y += int(self.vel)

    #Reset the bird
    def reset(self):
        self.index = 0
        self.counter = 0
        self.vel = 0
        self.rect.center = self.initialPosition
        self.flying = True
        self.gameOver = False
    
    #handle the animation
    def birdAnimation(self, flap_countdown):
        self.counter += 1

        if self.counter > flap_countdown:
            self.counter = 0
            self.index += 1
            self.index = self.index % 3
            self.image = self.images[self.index]
        
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        