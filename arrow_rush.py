import math
import pygame
from pygame.locals import *

WIDTH = 480
HEIGHT = 360
BLACK = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("data\\" + "background.jpg")

class Title(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.font = pygame.font.SysFont("comicsansms", 50)
        self.original = self.font.render("Arrow Rush", True, BLACK)

        self.theta = 0

    def update(self):
        self.theta += 0.05

        self.image = pygame.transform.rotate(self.original, math.sin(self.theta) * 5)
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/4))

        screen.blit(self.image, self.rect)

clock = pygame.time.Clock()

title = Title()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

    screen.blit(background, (0,0))
    
    title.update()

    pygame.draw.polygon(screen, BLACK, 3)

    pygame.display.update()
    clock.tick(60)
