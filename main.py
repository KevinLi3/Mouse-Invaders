import pygame
import random
import math
from pygame import mixer
pygame.init()

#Create the screen
screen = pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load('output-onlinepngtools.png')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)
#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('output-onlinepngtools.png')
icon = pygame.image.load('rat.png')
pygame.display.set_icon(icon)

#Player

playerImg = pygame.image.load('cat.png')
playerX = 370
playerY = 480
playerX_change = 0

#Rat1
rat1Img = []
rat1X = []
rat1Y = []
rat1X_change = []
rat1Y_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    rat1Img.append(pygame.image.load('rat.png'))
    rat1X.append(random.randint(0,739))
    rat1Y.append(random.randint(0,150))
    rat1X_change.append(10)
    rat1Y_change.append(40)

#Ball
#Ready - Bullet can't be seen on the screen
#Fire - The bullet is moving
ballImg = pygame.image.load('tennis.png')
ballX = 0
ballY = 480
ballX_change = 0
ballY_change = 10
ball_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score = font.render("Score :"+ str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text(x,y):
    over_text= over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(over_text, (200,250))

def player(x,y):
    screen.blit(playerImg, (x, y))

def rat1(x,y,i):
    screen.blit(rat1Img[i], (x, y))

def fire_ball(x,y):
    global ball_state
    ball_state = "fire"
    screen.blit(ballImg,(x + 16, y + 10))


def isCollision(rat1X, rat1Y, ballX, ballY):
    distance = math.sqrt((math.pow(rat1X-ballX,2))+(math.pow(rat1Y-ballY,2)))
    if distance < 50:
        return True
    else:
        return False


#Game loop
running = True
while running:
    #RGB of the screen
    screen.fill((0,0,0))
    #Background
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE:
                if ball_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    #Get current x-coordinate of the cat
                    ballX = playerX
                    fire_ball(ballX,ballY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    #Checking boundaries of cat
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 740:
        playerX = 740

    # Rat1 movement
    for i in range (num_of_enemies):

        #Game Over
        if rat1Y[i] > 400:
            for j in range(num_of_enemies):
                rat1Y[j] = 2000
            game_over_text(0,0)
            break

        rat1X[i] += rat1X_change[i]
        if rat1X[i] <= 0:
            rat1X_change[i] = 10
            rat1Y[i] += rat1Y_change[i]
        elif rat1X[i] >= 740:
            rat1X_change[i] = -10
            rat1Y[i] += rat1Y_change[i]
        # Collision
        collision = isCollision(rat1X[i], rat1Y[i], ballX, ballY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            ballY = 480
            ball_state = "ready"
            score_value += 1
            rat1X[i] = random.randint(0, 739)
            rat1Y[i] = random.randint(50, 150)

        rat1(rat1X[i], rat1Y[i], i)

    #Bullet movement
    if ballY <= 0 :
        ballY =480
        ball_state = "ready"
    if ball_state is "fire":
        fire_ball(ballX,ballY)
        ballY -= ballY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

#rat.png made by Flat Icons from www.flaticon.com
#cat.png made by Freepik from www.flaticon.com
