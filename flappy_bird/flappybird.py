import pygame
from pygame.locals import *
import sys
import os
from bird import Bird
from pipe import Pipe
import random

#Change, depending on your setup
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 820

def draw_text(text, font, text_col,screen, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def no_birds_left(bird_group):
    for bird in bird_group:
        if bird.gameOver == False:
            return False
    
    return True

def main():
    
    #define games variables
    ground_scroll = 0
    scroll_speed = 4
    pipe_frequency = 1500 
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    score = 0
    pass_pipe = False

    pygame.init()

    #define font
    font = pygame.font.SysFont(None, 60)

    #define color
    color = (255,255,255)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("flappy bird")

    bg = pygame.image.load('images/bg.png')
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ground_img = pygame.image.load('images/ground.png')

    bird_group = pygame.sprite.Group()

    pipe_group = pygame.sprite.Group()

    #single bird
    flappy = Bird(100, SCREEN_HEIGHT // 2)

    bird_group.add(flappy)

    clock = pygame.time.Clock()

    flappy.flying = True

    running = 1
    #gameOver = pipes and grounds doesnt scroll anymore, Flappy gameOver means that the bird is not allowed to jump anymore
    gameOver = False

    while running:
        
        #draw background
        screen.blit(bg, (0,0))

        #draw pipes
        pipe_group.draw(screen)

        #draw the ground
        screen.blit(ground_img, (ground_scroll, 912))

        #draw bird
        bird_group.draw(screen)

        #handle the velocity for the bird
        bird_group.update()
        
        '''
        This is to visualize the the distance from the bird to the next pipe
        '''
        # closest_pipe = 0

        # if len(bird_group) > 0:
        #     if len(pipe_group) > 1 and bird_group.sprites()[0].rect.right - pipe_group.sprites()[0].rect.right > 0:
        #         closest_pipe = 2

        # if len(pipe_group) > 0:
        #     #draw line from bird to the bottom of top pipe
        #     pygame.draw.line(screen, (170, 74, 68), (flappy.rect.center[0], flappy.rect.top), pipe_group.sprites()[closest_pipe + 1].rect.bottomright, 3)
        #     #draw line from bird to the bottom of top pipe
        #     pygame.draw.line(screen, (170, 74, 68), (flappy.rect.center[0], flappy.rect.bottom), pipe_group.sprites()[closest_pipe].rect.topright, 3)

        #check the score
        if len(pipe_group) > 0 and len(bird_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
                    pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_text(str(score), font, color, screen, int(SCREEN_WIDTH / 2), 20)

        #look for collisions - for a single bird
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: 
            gameOver = True
            flappy.gameOver = True 

        if gameOver == False and flappy.flying == True:
            #scroll the ground
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            #generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(850, SCREEN_HEIGHT // 2 + pipe_height, scroll_speed)
                top_pipe = Pipe(850, SCREEN_HEIGHT // 2 + pipe_height, scroll_speed, True)

                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            #scroll the pipes
            pipe_group.update()


        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and flappy.gameOver == False:
                    #single bird
                    flappy.flying = True
                    flappy.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN and flappy.flying == False and flappy.gameOver == True:
                pipe_group.empty()
                score = 0
                gameOver = False
                #single bird
                flappy.reset()

        pygame.display.update()

        # Limit the framerate
        clock.tick(70)


if __name__ == "__main__":
    main()