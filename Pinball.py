#All Imports
import pygame
import pymunk
import math
import array
import random

#Addes the sound for the paddles
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)


#Global variables
score = 0
increaseScore = 5

#If the ball makes contact with multiple obsticles then it will begin to chain
chain_count = 0
chainMultiplier = 5  #each chain touch would add an additional +5 points
flipper_touched = False

game_over = False

#Paddle Variables
PADDLE_LENGTH = 100
PADDLE_RADIUS = 6
PADDLE_SPEED = 10.0
PADDLE_COLOR = (255, 80, 80)

#Bumber Variables
BUMPER_RADIUS = 20
BUMPER_COLOR = (255, 80, 80)
BUMPER_HIT_COLOR = (255, 255, 80)
BUMPER_HIT_FRAMES = 6

#For the sound of the flippers when they are clicked
left_was_pressed = False
right_was_pressed = False



#Start of the Game
pygame.init()

WIDTH, HEIGHT = 600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 300)
font = pygame.font.SysFont('Arial', 30)





#Ball Creation and Variables
ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
ball_body.position = (100, 500)
ball_shape = pymunk.Circle(ball_body, 20)
ball_shape.elasticity = 0.5
ball_shape.friction = 0.5
space.add(ball_body, ball_shape)
ball_body.apply_impulse_at_local_point((random.randint(-100, 100), -200))

#Adds collision for the ball
ball_shape.collision_type = 1



def create_paddle(pos, rest_angle, flip_angle):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = pos
    body.angle = rest_angle

    shape = pymunk.Segment(body, (0, 0), (PADDLE_LENGTH, 0), PADDLE_RADIUS)
    shape.elasticity = 1.2
    shape.friction = 0.5

    space.add(body, shape)
    return body, rest_angle, flip_angle


PIVOT_Y = 800
left_body,  left_rest,  left_flip  = create_paddle((165, PIVOT_Y), math.radians(35), math.radians(-0))
right_body, right_rest, right_flip = create_paddle((435, PIVOT_Y), math.radians(150), math.radians(180))


def create_wall(a, b):
    seg = pymunk.Segment(space.static_body, a, b, 5)
    seg.elasticity = 0.9
    seg.friction = 1.0
    space.add(seg)
    return seg


#Holds the positions for the walls on the board
walls = []
walls.append(create_wall((20, 20),   (20, 880)))
walls.append(create_wall((580, 20),  (580, 880)))
walls.append(create_wall((20, 20),   (580, 20)))
walls.append(create_wall((20, 680),  (165, PIVOT_Y)))   # bottom-left angled
walls.append(create_wall((580, 680), (435, PIVOT_Y)))   # bottom-right angled

#Bumper poistions on the board
bumper_positions = [
    (200, 250),
    (400, 250),
    (300, 380),
    (160, 430),
    (440, 430),
]

bumpers = []



def create_bumper(pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, BUMPER_RADIUS)
    shape.elasticity = 1.5  # very bouncy
    shape.friction = 0.3
    space.add(body, shape)
    return shape


for pos in bumper_positions:
    bumpers.append([create_bumper(pos), 0])


for entry in bumpers:
    entry[0].collision_type = 2

def check_bumper_hits():
    global score, chain_count, flipper_touched
    bx, by = ball_body.position
    vx, vy = ball_body.velocity

    next_bx = bx + vx * (1 / 60)
    next_by = by + vy * (1 / 60)

    for entry in bumpers:
        shape, hit_timer = entry
        px, py = shape.body.position

        dist_current = math.sqrt((bx - px) ** 2 + (by - py) ** 2)
        dist_next = math.sqrt((next_bx - px) ** 2 + (next_by - py) ** 2)

        threshold = BUMPER_RADIUS + 20

        if (dist_current < threshold or dist_next < threshold) and hit_timer == 0:
            chain_count += 1
            points = chain_count * chainMultiplier  # +5, +10, +15...
            score += points
            entry[1] = BUMPER_HIT_FRAMES
            flipper_touched = False  # reset flipper flag on bumper hit

            if chain_count > 1:
                    chain_sound.play()
            else:
                bumper_sound.play()


def check_flipper_touch():
    global chain_count, flipper_touched

    #Checks if the ball is near the flippers
    bx, by = ball_body.position
    left_px,  left_py  = left_body.position
    right_px, right_py = right_body.position

    near_left  = math.sqrt((bx - left_px)**2  + (by - left_py)**2)  < PADDLE_LENGTH + 10
    near_right = math.sqrt((bx - right_px)**2 + (by - right_py)**2) < PADDLE_LENGTH + 10

    if (near_left or near_right) and not flipper_touched:
        if chain_count > 0:
            flipper_reset_sound.play()
        chain_count = 0
        flipper_touched = True

#Displays the chain text at the top of board
def draw_chain():
    if chain_count > 1:
        intensity = min(255, 80 + chain_count * 20)
        chain_color = (255, intensity, 0)

        chain_font = pygame.font.SysFont('Arial', 24)
        chain_text = chain_font.render(
            f"x{chain_count} CHAIN!  +{chain_count * chainMultiplier}", True, chain_color
        )
        screen.blit(chain_text, (WIDTH//2 - chain_text.get_width()//2, 60))


def reset_game():
    global score
    score = 0
    ball_body.position = (100, 500)
    ball_body.velocity = (0, 0)
    ball_body.angle = 0
    ball_body.angular_velocity = 0
    ball_body.apply_impulse_at_local_point((random.randint(-100, 100), -200))


def generate_beep(frequency=220, duration=0.08, volume=0.4):
    sample_rate = 44100
    samples = int(sample_rate * duration)
    wave = array.array('h', [
        int(math.sin(2 * math.pi * frequency * t / sample_rate)
            * (1 - t / samples)  # fade out
            * volume * 32767)
        for t in range(samples)
    ])
    sound = pygame.mixer.Sound(buffer=wave)
    return sound

flipper_sound = generate_beep(frequency=220, duration=0.08)
bumper_sound = generate_beep(frequency=220, duration=0.08)
chain_sound = generate_beep(frequency=440, duration=0.12)
flipper_reset_sound = generate_beep(frequency=150, duration=0.06)



def draw_segment_body(body, color=(255, 255, 255)):
    for shape in body.shapes:
        if isinstance(shape, pymunk.Segment):
            a_world = body.local_to_world(shape.a)
            b_world = body.local_to_world(shape.b)
            pygame.draw.line(
                screen, color,
                (int(a_world.x), int(a_world.y)),
                (int(b_world.x), int(b_world.y)),
                PADDLE_RADIUS * 2,
            )
            # Draw circles at the endpoints for a rounded cap look
            pygame.draw.circle(screen, color, (int(a_world.x), int(a_world.y)), PADDLE_RADIUS)
            pygame.draw.circle(screen, color, (int(b_world.x), int(b_world.y)), PADDLE_RADIUS)


def draw_ball():
    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (int(ball_body.position.x), int(ball_body.position.y)),
        10,
    )


def draw_walls():
    for wall in walls:
        a, b = wall.a, wall.b
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (int(a.x), int(a.y)),
            (int(b.x), int(b.y)),
            10,
        )


def draw_bumpers():
    for entry in bumpers:
        shape, hit_timer = entry
        pos = (int(shape.body.position.x), int(shape.body.position.y))
        color = BUMPER_HIT_COLOR if hit_timer > 0 else BUMPER_COLOR
        pygame.draw.circle(screen, color, pos, BUMPER_RADIUS)
        pygame.draw.circle(screen, (255, 255, 255), pos, BUMPER_RADIUS, 2)  # white outline
        if hit_timer > 0:
            entry[1] -= 1

def ball_out():
    return ball_body.position.y > HEIGHT + 50

def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    big_font = pygame.font.SysFont('Arial', 60)
    msg = big_font.render("GAME OVER", True, (255, 80, 80))
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 300))

    #Shows the score and retry
    score_msg = font.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(score_msg, (WIDTH//2 - score_msg.get_width()//2, 380))

    #Retry Button
    button_rect = pygame.Rect(WIDTH//2 - 80, 450, 160, 50)
    pygame.draw.rect(screen, (255, 80, 80), button_rect, border_radius=10)
    btn_text = font.render("RETRY", True, (255, 255, 255))
    screen.blit(btn_text, (WIDTH//2 - btn_text.get_width()//2, 462))

    return button_rect






#Keeps the game in play until it quits
running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if retry_button.collidepoint(event.pos):
                game_over = False
                reset_game()

    if ball_out():
        game_over = True

    if not game_over:
        keys = pygame.key.get_pressed()

    keys = pygame.key.get_pressed()

    left_pressed = keys[pygame.K_a]
    right_pressed = keys[pygame.K_d]

    #Plays the sound when the A or D is pressed
    if left_pressed and not left_was_pressed:
        flipper_sound.play()
    if right_pressed and not right_was_pressed:
        flipper_sound.play()
    left_was_pressed = left_pressed
    right_was_pressed = right_pressed


    l_target = left_flip if left_pressed else left_rest
    r_target = right_flip if right_pressed else right_rest


    def drive_paddle(body, target):
        diff = target - body.angle
        max_delta = PADDLE_SPEED * dt
        if abs(diff) < max_delta:
            body.angle = target
            body.angular_velocity = 0
        else:
            body.angular_velocity = math.copysign(PADDLE_SPEED, diff)

    drive_paddle(left_body,  l_target)
    drive_paddle(right_body, r_target)

    space.step(dt)
    check_bumper_hits()

    screen.fill((0, 0, 0))

    #display the score
    scoreSurface = font.render("Current Score: " + str(score), True, (255, 255, 255))
    textSize = scoreSurface.get_size()
    textX = int(310 - (textSize[0] / 2))
    screen.blit(scoreSurface, (textX, 25))

    #Everything below adds to the board!!!!
    draw_walls()
    draw_bumpers()
    draw_ball()
    draw_segment_body(left_body, color=(44, 167, 212))
    draw_segment_body(right_body, color=(44, 167, 212))
    check_bumper_hits()
    check_flipper_touch()
    draw_chain()

    if game_over:
        retry_button = draw_game_over()

    pygame.display.flip()
pygame.quit()