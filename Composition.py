import pygame

pygame.init()

pygame.display.set_caption("Hello World")

img = pygame.image.load("images1/backgrounds/prague.png")
img2 = pygame.image.load("images1/characters/yoda.png")

width = min(img.get_width(), img2.get_width())
height = min(img.get_height(), img2.get_height())
screen = pygame.display.set_mode((width, height))
green_threshold = 100

for y in range(height):
    for x in range(width):
        bg_color = img.get_at((x, y))
        fg_color = img2.get_at((x, y))


        if fg_color.g > green_threshold and fg_color.g > fg_color.r * 1.2 and fg_color.g > fg_color.b * 1.2:
            img.set_at((x, y), bg_color)
        else:
            img.set_at((x, y), fg_color)



screen.blit(img, (0, 0) )

pygame.display.flip()
screen.blit(img2, (0, 0))
pygame.image.save(img, "combined.png")

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True