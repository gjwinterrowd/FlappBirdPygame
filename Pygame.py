import sys
import pygame
import random
#This function places the floor and gives the side scrolling affect
def draw_floor():
    screen.blit(floor_surface,(floor_x_position,720))
    screen.blit(floor_surface,(floor_x_position + 576,720))
#This function spawns both pipes
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos -175))
    return bottom_pipe,top_pipe
#This function continues the spawning of the pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
#This function flips the image of the top pipe so they face each other
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.top <= 0:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
        else:
            screen.blit(pipe_surface,pipe)
#This function uses the rectangles and checks for collisions in order to end the game
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 720:
        return False
    return True
#This function displays the score and high score
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(238, 685))
        screen.blit(high_score_surface, high_score_rect)
#This function is used to update the high score
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

#This initializes the game, sets the screen dimensions, the clock, and the game's font
pygame.init()
screen = pygame.display.set_mode((576,800))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('comicsansms',40)

# These are the game variables
gravity = 0.15
bird_movement = 0
game_active = True
score = 0
high_score = 0
#This is the importing and assigning of all the images
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
#Starting position of floor
floor_x_position = 0
#Rectangle of bird to check for collision, as well as starting position
bird_rect = bird_surface.get_rect(center = (100,400))
#Empty list that fills with pipe spawns
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
#Determines how often pipes spawn
pygame.time.set_timer(SPAWNPIPE,1500)
#The five possible heights for the bottom pipe
pipe_height = [300,350,400,450,500]
#This is the condition for the running of the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        if event.type == pygame.KEYDOWN:
            #This is for the controls of the game
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and game_active == False:
                #This clears the bird, score, and pipes which is the preview screen and the game over screen
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,400)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
    #this is the locations of the background surface and the floor
    screen.blit(bg_surface,(0,-100))
    screen.blit(floor_surface,(floor_x_position,720))

    if game_active:
    # This determines bird location based on the effects of gravity and user input
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface,bird_rect)
        game_active = check_collision(pipe_list)

    # This spawns pipes, changes score, and displays score
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.006
        score_display('main_game')
    else:
        high_score = update_score(score,high_score)
        score_display('game_over')
    # This function calls the floor and keeps it moving
    floor_x_position -= .5
    draw_floor()
    if floor_x_position <= -576:
        floor_x_position = 0
    #This is how fast time passes in the game
    pygame.display.update()
    clock.tick(120)