import pygame
import random  # for random repspawn of enemies
import math  # for calcutaing the distance between the enemy and the bullet

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))
# screen is the surface of our game
# width(x)=800,height(y)=600
# here the game window is created but after a few second it went away
# this is because our python program executes through the 7th line and then exits the code
# event - all the things that is going on the game window
# if the close window is pressed,then we should make running=false.
# we are creating a game loop which will only close when we close the game window

# Title and Icon
# changing the title
pygame.display.set_caption("Space Wars")
# changing the logo
icon = pygame.image.load('spaceship.png')
# https://www.flaticon.com/   32px
pygame.display.set_icon(icon)

score = 0  # this will be the total score of the player
font = pygame.font.Font('freesansbold.ttf',
                        32)  # inbuilt font in pygame for the font to display it on (10,10) with 32 px
textX = 10
textY = 10


# function to show score
def show_score(x, y):
    score_value = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# create the player
playerImg = pygame.image.load('space_user.png')
playerX = 370  # as 400 is the middle ,but the image will also take some space
playerY = 480
playerX_change = 0  # change in x direction
playerY_change = 0  # change in y direction

# create the enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6  # we will have 6 number of enemies

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 800 - 64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# enemyImg = pygame.image.load('enemy.png')
# enemyX = random.randint(0, 800 - 64)  # for random repspawn of enemies
# enemyY = random.randint(50, 150)
# enemyX_change = 4  # change in x direction # for first movement of enemy
# enemyY_change = 40  # change in y direction # move down 40 when it hits the boundary

# background image
background = pygame.image.load('background.png')
# we need to add this background to our game loop

# create bullet
# ready state-we can't see the bullet on the screen
# fire state- the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def enemy(x, y, i):  # i for which enemy we want to create
    screen.blit(enemyImg[i], (x, y))


# here we have given the x and y values for the user spaceship
def player(x, y):
    screen.blit(playerImg, (x, y))  # blit is used to draw the playerImg on our screen


# for collision detection,calclutaing the distance between the bullet and the enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# we want this player to appear in every instant on our screen,so we need to call it inside the game loop

# now we need to have movement of the user..we need to modify our player function

# game loop
running = True
while running:
    # RGB = red,green,blue
    # red=255,0,0  we can create every color using red,green and blue

    # player func must be call after filling the screen as we add the player after the screen
    screen.fill((0, 0, 0))  # (0,0,0) is black
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # any keystroke pressed on the keyboard is actually an event
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is placed,check whether is left or right
        if event.type == pygame.KEYDOWN:  # KEYDOWN is pressing any key ,after KEYDOWN,we have to check for KEYUP for releasing that key
            # print("A Keystroke is pressed")
            if (event.key == pygame.K_LEFT):
                playerX_change = -5  # 5 is the pixel change where the new image will be on.
                # print("Left Arrow is Pressed")
            if (event.key == pygame.K_RIGHT):
                playerX_change = 5
                # print("Right Arrow is Pressed")
            if (event.key == pygame.K_SPACE):
                if (bullet_state is "ready"):
                    bulletX = playerX  # get the current x coordinate of the spaceship
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                # print("Keystroke is released")
                playerX_change = 0

    playerX = playerX + playerX_change
    # adding boundaries for our spaceship
    if (playerX <= 0):
        playerX = 0
    elif (playerX >= (800 - 64)):
        playerX = 800 - 64
    # enemy movement
    for i in range(num_of_enemies):
        # game over
        if (enemyY[i] > 440):
            for j in range(num_of_enemies):  # remove all the other enemies from the screen
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] = enemyX[i] + enemyX_change[i]
        if (enemyX[i] <= 0):
            enemyX_change[i] = 4
            enemyY[i] = enemyY[i] + enemyY_change[i]
        elif (enemyX[i] >= (800 - 64)):
            enemyX_change[i] = -4
            enemyY[i] = enemyY[i] + enemyY_change[i]
        # collison
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if (collision):
            bulletY = 480  # reset the bullet
            bullet_state = "ready"  # make it in ready state
            score = score + 1  # score will increase by one everytime we hit our enemy
            # print(score)
            enemyX[i] = random.randint(0, 800 - 64)  # for random repspawn of enemies
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # enemyX = enemyX + enemyX_change
    # if (enemyX <= 0):
    # enemyX_change = 4
    # enemyY = enemyY + enemyY_change
    # elif (enemyX >= (800 - 64)):
    #   enemyX_change = -4
    #  enemyY = enemyY + enemyY_change
    # bullet movement
    if (bulletY <= 0):
        bullet_state = "ready"  # for firing multiple bullets
        bulletY = 480
    if (bullet_state is "fire"):
        fire_bullet(bulletX, bulletY)
        bulletY = bulletY - bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # here we are making sure that our display is updated after every event

# now the game window will only close if i press the close window
# we are looping through all the events to find the QUIT event
