import pygame

# Initialize the game
pygame.init()

pygame.display.set_caption("Hello World")

img = pygame.image.load("images1/prague.png")
img2 = pygame.image.load("images1/characters/yoda.png")

width = min(img.get_width(), img2.get_width())
height = min(img.get_height(), img2.get_height())
screen = pygame.display.set_mode((width, height))
green_threshold = 100

for y in range(0, height):
    for x in range(0, width):
        c1 = img.get_at((x, y))
        c2 = img2.get_at((x, y))

        if c2.g > green_threshold and c2.g > c2.r * 1.2 and c2.g > c2.b * 1.2:
            # If it's green, ignore img2 and keep img1
            newcolor = (c1.r, c1.g, c1.b)
        else:
            # Otherwise, blend the pixel
            newcolor = ((c1.r + c2.r) // 2, (c1.g + c2.g) // 2, (c1.b + c2.b) // 2)

        newcolor = ((c1.r + c2.r) // 2, (c1.g + c2.g) // 2, (c1.b + c2.b) // 2)
        img.set_at((x, y), newcolor)

screen.blit(img, (0, 0) )

pygame.display.flip()

pygame.image.save(img, "combined.png")

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True