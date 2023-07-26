import pygame
from pygame.locals import *
import os
from bird import Bird
from pipe import Pipe
import neat
import random
import visualize

SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 550
GENERATION = 0

def draw_text(text, font, text_col,screen, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def no_birds_left(bird_group):
    for bird in bird_group:
        if bird.gameOver == False:
            return False
    
    return True

def main(genomes, config):

    global GENERATION
    GENERATION += 1
    
    #define games variables
    ground_scroll = 0
    scroll_speed = 5
    pipe_frequency = 1500 
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    score = 0

    pygame.init()

    #define font
    font = pygame.font.SysFont(None, 32)

    #define color
    color = (255,255,255)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("flappy bird")

    bg = pygame.image.load('images/bg.png')
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ground_img = pygame.image.load('images/ground.png')

    #start by creating lists holding the genome itself, the
    #neural network associated with the genome and the bird
    #object that uses that network to play
    nets = []
    bird_group = pygame.sprite.Group()
    ge = []

    pipe_group = pygame.sprite.Group()

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        bird = Bird(100, SCREEN_HEIGHT // 2)
        bird.flying = True
        bird_group.add(bird)
        ge.append(genome)

    count = len(bird_group)

    clock = pygame.time.Clock()

    running = 1
    #gameOver = pipes and grounds doesnt scroll anymore, Flappy gameOver means that the bird is not allowed to jump anymore
    gameOver = False

    while running and len(bird_group) > 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                pygame.quit()
                quit()
                break

        #check how many birds are still alive
        count = len(bird_group)

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

        if gameOver == False:
            #scroll the ground
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            #generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-110, 110)
                btm_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, scroll_speed)
                top_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, scroll_speed, True)

                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            #scroll the pipes
            pipe_group.update()

        closest_pipe = 0

        draw_text(f'Gen: {GENERATION}', font, color, screen, 10, 20)
        draw_text(f'Score: {bird_group.sprites()[0].score}', font, color, screen, 100, 20)

        if len(pipe_group) > 1 and bird_group.sprites()[0].rect.left - pipe_group.sprites()[0].rect.right > 0:
            closest_pipe = 2


        for x, bird in enumerate(bird_group):
            ge[x].fitness += 0.1

            #draw line from bird to the bottom of top pipe
            pygame.draw.line(screen, (170, 74, 68), (bird.rect.center[0], bird.rect.top), pipe_group.sprites()[closest_pipe + 1].rect.bottomright, 3)
            #draw line from bird to the bottom of top pipe
            pygame.draw.line(screen, (170, 74, 68), (bird.rect.center[0], bird.rect.bottom), pipe_group.sprites()[closest_pipe].rect.topright, 3)
            #bottom of top pipe y position
            top_pipe_y = pipe_group.sprites()[closest_pipe + 1].rect.bottom
            #top of bottom pipe y position
            bottom_pipe_y = pipe_group.sprites()[closest_pipe].rect.top

            #x distance from bird to closest pipe
            x_distance = abs(bird.rect.left - pipe_group.sprites()[closest_pipe].rect.right) / (SCREEN_WIDTH)

            output = nets[bird_group.sprites().index(bird)].activate((x_distance, (bird.rect.top - top_pipe_y) / 912, (bird.rect.bottom - bottom_pipe_y) / 912))

            if output[0] > 0.5:
                bird.jump()


        #check the score
        for bird in bird_group:
            if len(pipe_group) > 0:
                if bird.rect.left > pipe_group.sprites()[0].rect.left\
                    and bird.rect.right < pipe_group.sprites()[0].rect.right\
                    and bird.pass_pipe == False:
                        bird.pass_pipe = True
                if bird.pass_pipe == True:
                    if bird.rect.left > pipe_group.sprites()[0].rect.right:
                        bird.score += 1
                        ge[bird_group.sprites().index(bird)].fitness += 5
                        bird.pass_pipe = False

        draw_text(f'Number of Bird: {count}', font, color, screen, 300, 20)

        for bird in bird_group:
            if pygame.sprite.spritecollide(bird, pipe_group, False):
                nets.pop(bird_group.sprites().index(bird))
                ge.pop(bird_group.sprites().index(bird))
                bird_group.remove(bird)
            elif bird.rect.top < 0:
                nets.pop(bird_group.sprites().index(bird))
                ge.pop(bird_group.sprites().index(bird))
                bird_group.remove(bird)
            elif bird.rect.bottom >= 912:
                nets.pop(bird_group.sprites().index(bird))
                ge.pop(bird_group.sprites().index(bird))
                bird_group.remove(bird)


        pygame.display.update()

        if len(bird_group) > 0 and bird_group.sprites()[0].score >= 200:
            break

        # Limit the framerate
        clock.tick(60)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)

    visualize.draw_net(config, winner, True)

if __name__ == "__main__":
    # main()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)