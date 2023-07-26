import pygame

class Pipe(pygame.sprite.Sprite):

    pipe_gap = 150

    def __init__(self, x, y, scroll_speed, mirror=False):
        pygame.sprite.Sprite.__init__(self)

        self.scroll_speed = scroll_speed
        self.image = pygame.image.load('images/pipe.png')
        self.rect = self.image.get_rect()
        if mirror:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - int(self.pipe_gap // 2))
        else:
            self.rect.topleft = (x, y + int(self.pipe_gap // 2))

    def update(self):
        self.rect.x -= self.scroll_speed

        if self.rect.right < 0:
            self.kill()