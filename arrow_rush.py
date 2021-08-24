
import math
import random
import pygame
from pygame.locals import *

WIDTH = 480
HEIGHT = 360
BLACK = (0, 0, 0)
RED = (255, 0, 0)

game_active = False

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("data\\" + "background.jpg")


class Title(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.font = pygame.font.SysFont("comicsansms", 50)
        self.original = self.font.render("Arrow Rush", True, BLACK)
        self.theta = 0
        self.visible = True

    def update(self):
        if self.visible == True:
            self.theta += 0.05

            self.image = pygame.transform.rotate(
                self.original, math.sin(self.theta) * 5)
            self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/4))

            screen.blit(self.image, self.rect)


class PlayButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("data\\" + "play_button.png")
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT*3/4))
        self.width, self.height = self.rect.width, self.rect.height
        self.mask = pygame.mask.from_surface(self.image)
        self.brightness, self.brightness_cap = 0, 25
        self.size, self.size_cap = 1, 1.05
        self.visible = True

    def is_selected(self) -> bool:
        x, y = pygame.mouse.get_pos()
        pos_in_mask = x - self.rect.x, y - self.rect.y
        return self.rect.collidepoint((x, y)) and self.mask.get_at(pos_in_mask)

    def update(self):
        if self.visible == True:
            if self.is_selected():
                self.brightness += 3 if self.brightness < self.brightness_cap else 0
                self.size += (self.size_cap - self.size) / 5
            else:
                self.brightness -= 3 if self.brightness > 0 else 0
                self.size += (1 - self.size) / 5

            self.new_image = self.image.copy()
            self.new_image = pygame.transform.smoothscale(
                self.new_image, (round(self.width*self.size), round(self.height*self.size)))
            self.new_image.fill(
                tuple(num + self.brightness for num in BLACK), special_flags=BLEND_RGB_ADD)
            self.new_rect = self.new_image.get_rect(
                center=(WIDTH/2, HEIGHT*3/4))

            screen.blit(self.new_image, self.new_rect)


class Arrows(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.directions = [
            K_UP,
            K_DOWN,
            K_LEFT,
            K_RIGHT
        ]
        self.rotations = {
            K_UP: 90,
            K_DOWN: -90,
            K_LEFT: 180,
            K_RIGHT: 0
        }

    def new_arrow(self):
        self.color = "red" if random.randrange(0, 3) == 1 else "black"

        if self.color == "black":
            self.image = pygame.image.load("data\\" + "arrow.png")
        else:
            self.image = pygame.image.load("data\\" + "red_arrow.png")

        self.direction = self.directions[random.randrange(0, 4)]
        self.image = pygame.transform.rotate(
            self.image, self.rotations[self.direction] if self.color == "black" else self.rotations[self.direction] + 180)
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/2))

    def update(self):
        screen.blit(self.image, self.rect)

    def test_input(self, key):
        if self.direction == key:
            score.score += 1
            print(score.score)

            self.new_arrow()


class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0


class TimeMeter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.meter = 1

        self.rect = pygame.Rect([0, 0, 0, 0])
        self.rect.width = 400
        self.rect.height = 50
        self.rect.center = (WIDTH / 2, HEIGHT * 4 / 5)

        self.inner_rect = self.rect.copy()
        self.inner_rect = self.inner_rect.inflate(-10, -10)
        self.inner_rect_left = self.inner_rect.left

    def update(self):
        self.inner_rect.width = 390 * self.meter
        self.inner_rect.left = self.inner_rect_left
        self.meter -= 0.001 if self.meter > 0 else 0

        pygame.draw.rect(background, BLACK, self.rect, border_radius=5)
        pygame.draw.rect(background, RED, self.inner_rect, border_radius=5)


clock = pygame.time.Clock()

title = Title()
play_button = PlayButton()
arrows = Arrows()
score = Score()
time_meter = TimeMeter()

arrows.new_arrow()

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            if play_button.is_selected() and play_button.visible == True:
                play_button.visible = False
                title.visible = False

                game_active = True
        if event.type == KEYDOWN and game_active == True:
            arrows.test_input(event.key)

    screen.blit(background, (0, 0))

    title.update()
    play_button.update()
    arrows.update()
    time_meter.update()

    pygame.display.update()
    clock.tick(60)
