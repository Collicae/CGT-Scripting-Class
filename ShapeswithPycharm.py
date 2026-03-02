import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing Shapes")

#keeps window open indefinitely
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #make background black
    screen.fill((0, 0, 0))

    #Adding the shapes with Pygame
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(250, 400, 300, 100))
    pygame.draw.arc(screen, (255, 255, 255), pygame.Rect(280, 330, 230, 150), 0, 5, width=10)
    pygame.draw.circle(screen, color=(255, 255, 255), center=(330, 540), radius=40)
    pygame.draw.circle(screen, color=(255, 255, 255), center=(480, 540), radius=40)
    pygame.display.flip()

pygame.quit()