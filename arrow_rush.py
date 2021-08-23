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

class PlayButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data\\" + "play_button.png")
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT*3/4))
        self.mask = pygame.mask.from_surface(self.image)
        self.brightness = 0
        # self.image.fill((50,50,50), special_flags=BLEND_RGB_ADD)

    def update(self):
        x, y = pygame.mouse.get_pos()
        pos_in_mask = x - self.rect.x, y - self.rect.y
        touching = self.rect.collidepoint((x, y)) and self.mask.get_at(pos_in_mask)

        self.new_image = self.image.copy()

        if touching:
            self.brightness += 3 if self.brightness < 25 else 0
        else:
            self.brightness -= 3 if self.brightness > 0 else 0

        self.new_image.fill(tuple(num + self.brightness for num in BLACK), special_flags=BLEND_RGB_ADD)
        screen.blit(self.new_image, self.rect)


clock = pygame.time.Clock()

title = Title()
play_button = PlayButton()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

    screen.blit(background, (0,0))
    
    title.update()
    play_button.update()

    pygame.display.update()
    clock.tick(60)
