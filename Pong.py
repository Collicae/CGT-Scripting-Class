import random
import pygame
import pymunk

#constants and globals
PADDLEMOVE = 0.5
STARTSPEED = 60
score = 0

leftScore = 0
rightScore = 0

done = False

#collision stuff
COLLTYPE_LEFT = 1
COLLTYPE_RIGHT = 2
COLLTYPE_BALL = 3
COLLTYPE_PADDLE = 4


#Keeps score of both left and right players
def collide_left(space, arbiter, data):
    global leftScore
    leftScore = leftScore+1
    return True
def collide_right(space, arbiter, data):
    global rightScore
    rightScore = rightScore+1
    return True

#paddle mover for the paddles
def MovePaddle(body, up, down):
    deltaY = 0
    pos = body.position
    if up:
        deltaY -= PADDLEMOVE
    if down:
        deltaY += PADDLEMOVE
    body.position = (pos.x, pos.y + deltaY)


# Initialize the game
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))
space = pymunk.Space()
space.gravity = (0, 0)
#load font
font = pygame.font.SysFont('Arial', 30)

#Left Paddle
leftPaddleBody = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
leftPaddleBody.position = (40, 300)
leftPaddleShape = pymunk.Poly.create_box(leftPaddleBody, (20, 100))
leftPaddleShape.elasticity = 1.0
space.add(leftPaddleBody, leftPaddleShape)

#Right Paddle
rightPaddleBody = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
rightPaddleBody.position = (760, 300)
rightPaddleShape = pymunk.Poly.create_box(rightPaddleBody, (20, 100))
rightPaddleShape.elasticity = 1.0
space.add(rightPaddleBody, rightPaddleShape)


#Creates the Body for the screen (So the ball does not go off screen
leftBody = pymunk.Body(1,100, pymunk.Body.STATIC)
leftBody.position = (10, 300)
leftShape = pymunk.Poly.create_box(leftBody, (20, 800))
leftShape.elasticity = 1.0
space.add(leftBody, leftShape)

rightBody = pymunk.Body(1,100, pymunk.Body.STATIC)
rightBody.position = (790, 300)
rightShape = pymunk.Poly.create_box(rightBody, (20, 800))
rightShape.elasticity = 1.0
space.add(rightBody, rightShape)

topBody = pymunk.Body(body_type=pymunk.Body.STATIC)
topBody.position = (400, 10)
topShape = pymunk.Poly.create_box(topBody, (800, 20))
topShape.elasticity = 1.0
space.add(topBody, topShape)

bottomBody = pymunk.Body(body_type=pymunk.Body.STATIC)
bottomBody.position = (400, 590)
bottomShape = pymunk.Poly.create_box(bottomBody, (800, 20))
bottomShape.elasticity = 1.0
space.add(bottomBody, bottomShape)

ballBody = pymunk.Body(1,100)
ballBody.position = (400,300)
ballShape = pymunk.Circle(ballBody, 10)
ballShape.elasticity = 1.0
ballShape.collision_type = COLLTYPE_BALL
ballBody.apply_impulse_at_local_point(
    (random.randint(-STARTSPEED, STARTSPEED), random.randint(0,STARTSPEED)))
space.add(ballBody, ballShape)

leftShape.collision_type = COLLTYPE_LEFT
rightShape.collision_type = COLLTYPE_RIGHT
space.on_collision(COLLTYPE_LEFT, COLLTYPE_BALL, begin=collide_left)
space.on_collision(COLLTYPE_RIGHT, COLLTYPE_BALL, begin=collide_right)





def drawBox(screen, body, shape):
    pos = body.position
    bb = shape.bb
    width = bb.right-bb.left
    height = bb.top - bb.bottom
    topLeft = (pos[0] - width / 2, pos[1] - height / 2)
    pygame.draw.rect(screen, (255, 255, 255),
                     (topLeft[0],topLeft[1],width,height))


wDown = False
sDown = False
upArrowDown = False
downArrowDown = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                wDown = True
            if event.key == pygame.K_s:
                sDown = True
            if event.key == pygame.K_UP:
                upArrowDown = True
            if event.key == pygame.K_DOWN:
                downArrowDown = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                wDown = False
            if event.key == pygame.K_s:
                sDown = False
            if event.key == pygame.K_UP:
                upArrowDown = False
            if event.key == pygame.K_DOWN:
                downArrowDown = False

    MovePaddle(leftPaddleBody, wDown, sDown)
    MovePaddle(rightPaddleBody, upArrowDown, downArrowDown)
    space.step(1/60.0)
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 255, 255), ballBody.position, 10)
    drawBox(screen, leftBody, leftShape)
    drawBox(screen, rightBody, rightShape)


    drawBox(screen, leftPaddleBody, leftPaddleShape)
    drawBox(screen, rightPaddleBody, rightPaddleShape)

    #Ending sequence for the game if either score reaches 5 it ends
    if rightScore == 5 or leftScore == 5:
        done = True

    #display score
    scoreSurface = font.render(str(rightScore) + " : " + str(leftScore), True, (255, 255, 255))
    textSize = scoreSurface.get_size()
    textX = int(400 - (textSize[0] / 2))
    screen.blit(scoreSurface, (textX, 20))
    pygame.display.update()

doneSurface = font.render("GameOver", True, (255, 255, 255))
textSize = doneSurface.get_size()
textX = int(400 - (textSize[0] / 2))
textY = int(300 - (textSize[1] / 2))
screen.blit(doneSurface, (textX, textY))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)